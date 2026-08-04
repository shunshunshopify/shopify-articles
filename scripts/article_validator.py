#!/usr/bin/env python3
"""SOLSTAR記事HTMLの決定論的な公開前検証。"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.toc_targets = []
        self.internal_links = []
        self.h2 = []
        self.h3 = []
        self.faq_questions = []
        self.learn_items = 0
        self.updated_texts = []
        self.supervisor_texts = []
        self.intro_paragraphs = []
        self.visible_text = []
        self.custom_content_roots = 0
        self._in_toc = 0
        self._suppressed = 0
        self._in_h2 = False
        self._h2_id = None
        self._h2_text = []
        self._current_h2_id = None
        self._in_h3 = False
        self._h3_text = []
        self._h3_section = None
        self._learn_list_depth = 0
        self._capture_updated = False
        self._capture_supervisor = False
        self._capture_intro = False
        self._paragraph_text = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag in {"style", "script"}:
            self._suppressed += 1
        if "id" in data:
            self.ids.append(data["id"])
        if tag == "div" and "toc" in data.get("class", "").split():
            self._in_toc += 1
        if tag == "div" and "custom-content" in data.get("class", "").split():
            self.custom_content_roots += 1
        if tag == "a":
            href = data.get("href", "")
            if self._in_toc and href.startswith("#"):
                self.toc_targets.append(href[1:])
            if href.startswith("/blogs/"):
                self.internal_links.append(href)
        if tag == "h2":
            self._in_h2 = True
            self._h2_id = data.get("id")
            self._current_h2_id = self._h2_id
            self._h2_text = []
        if tag == "h3":
            self._in_h3 = True
            self._h3_text = []
            self._h3_section = self._current_h2_id
        if tag == "ul" and self._current_h2_id == "sec-learn":
            self._learn_list_depth += 1
        if tag == "li" and self._learn_list_depth == 1:
            self.learn_items += 1
        if tag == "p" and not self._suppressed:
            classes = data.get("class", "").split()
            self._paragraph_text = []
            self._capture_updated = "article-updated" in classes
            self._capture_supervisor = "article-supervisor" in classes
            self._capture_intro = (
                self._current_h2_id is None
                and not self._capture_updated
                and not self._capture_supervisor
            )

    def handle_endtag(self, tag):
        if tag in {"style", "script"}:
            self._suppressed = max(0, self._suppressed - 1)
        if tag == "div" and self._in_toc:
            self._in_toc -= 1
        if tag == "h2" and self._in_h2:
            self.h2.append((self._h2_id, "".join(self._h2_text).strip()))
            self._in_h2 = False
        if tag == "h3" and self._in_h3:
            text = "".join(self._h3_text).strip()
            self.h3.append((self._h3_section, text))
            if self._h3_section == "sec-faq":
                self.faq_questions.append(text)
            self._in_h3 = False
        if tag == "ul" and self._learn_list_depth:
            self._learn_list_depth -= 1
        if tag == "p":
            text = "".join(self._paragraph_text).strip()
            if self._capture_updated:
                self.updated_texts.append(text)
            elif self._capture_supervisor:
                self.supervisor_texts.append(text)
            elif self._capture_intro and text:
                self.intro_paragraphs.append(text)
            self._capture_updated = False
            self._capture_supervisor = False
            self._capture_intro = False
            self._paragraph_text = []

    def handle_data(self, data):
        if not self._suppressed:
            self.visible_text.append(data)
        if self._in_h2:
            self._h2_text.append(data)
        if self._in_h3:
            self._h3_text.append(data)
        if self._capture_updated or self._capture_supervisor or self._capture_intro:
            self._paragraph_text.append(data)


def style_block(text):
    match = re.search(r"<style>(.*?)</style>", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


def normalized_css(text):
    """CSSの意味を変えない空白・コメント差を除いて比較できる形へ整える。"""
    if text is None:
        return None
    value = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    value = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"\s*([{}:;,>])\s*", r"\1", value)


def published_handles(path):
    if not path.exists():
        return set()
    handles = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and "| 公開 |" in line:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells:
                handles.add(cells[0])
    return handles


def contains_value(obj, expected):
    if isinstance(obj, dict):
        return any(contains_value(value, expected) for value in obj.values())
    if isinstance(obj, list):
        return any(contains_value(value, expected) for value in obj)
    return obj == expected


def article_jsonld_nodes(obj):
    """JSON-LDからArticle型のノードを再帰的に抽出する。"""
    nodes = []
    if isinstance(obj, dict):
        node_type = obj.get("@type")
        types = node_type if isinstance(node_type, list) else [node_type]
        if "Article" in types:
            nodes.append(obj)
        for value in obj.values():
            nodes.extend(article_jsonld_nodes(value))
    elif isinstance(obj, list):
        for value in obj:
            nodes.extend(article_jsonld_nodes(value))
    return nodes


def unresolved_description(value):
    if not isinstance(value, str) or not value.strip():
        return True
    text = value.strip()
    if text in {"DESCRIPTION", "META_DESCRIPTION"}:
        return True
    return bool(re.search(r"\{\{[^}]+\}\}|【(?:要記入|要確認)[：:].*?】", text))


def normalized_text(value):
    return re.sub(r"\s+", " ", value).strip()


def lint_warnings(article):
    parser = ArticleParser()
    parser.feed(article.read_text(encoding="utf-8"))
    warnings = []
    intro = normalized_text(" ".join(parser.intro_paragraphs))
    intro_length = len(re.sub(r"\s+", "", intro))
    if intro and not 220 <= intro_length <= 380:
        warnings.append(
            f"導入文は300字程度が目安です（現在{intro_length}字、推奨220〜380字）"
        )
    if re.search(r"単に.+?だけでなく", intro):
        warnings.append("導入文に固定的な「単に〜だけでなく」構文があります")

    visible = normalized_text(" ".join(parser.visible_text))
    for phrase, threshold in (
        ("重要です", 4),
        ("必要があります", 4),
        ("まずは", 5),
        ("一方で", 5),
        ("ではなく", 6),
    ):
        count = visible.count(phrase)
        if count > threshold:
            warnings.append(f"「{phrase}」が{count}回あります。文脈と構文の反復を確認してください")
    for phrase in ("いかがでしたか", "と言えるでしょう", "することができます", "ではないでしょうか"):
        if phrase in visible:
            warnings.append(f"定型的に見えやすい表現「{phrase}」を文脈に合わせて確認してください")
    return warnings


def validate(article, template, published, allow_draft_placeholders=False):
    errors = []
    text = article.read_text(encoding="utf-8")
    parser = ArticleParser()
    parser.feed(text)
    template_parser = ArticleParser()
    template_text = template.read_text(encoding="utf-8")
    template_parser.feed(template_text)

    canonical_style_path = template.parent / "theme-css" / "solstar-article.css"
    if not canonical_style_path.exists():
        errors.append("最新版Styleがありません: theme-css/solstar-article.css")
    elif normalized_css(style_block(template_text)) != normalized_css(
        canonical_style_path.read_text(encoding="utf-8")
    ):
        errors.append(
            "article-template.html のStyleが theme-css/solstar-article.css の最新版と一致しません"
        )

    if parser.custom_content_roots != 1:
        errors.append("custom-contentルートは1つ必要です")
    duplicates = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
    if duplicates:
        errors.append("重複ID: " + ", ".join(duplicates))
    missing_targets = sorted(set(parser.toc_targets) - set(parser.ids))
    if missing_targets:
        errors.append("TOCリンク先が存在しません: " + ", ".join(missing_targets))
    if len(set(parser.toc_targets)) != len(parser.toc_targets):
        errors.append("TOCリンク先が重複しています")

    h2_ids = [item[0] for item in parser.h2]
    h2_by_id = {item[0]: item[1] for item in parser.h2}
    if h2_by_id.get("sec-learn") != "この記事でわかること":
        errors.append("H2「この記事でわかること」がありません")
    elif not 4 <= parser.learn_items <= 6:
        errors.append(f"「この記事でわかること」は4〜6項目必要です（現在{parser.learn_items}項目）")
    if "sec-faq" not in h2_ids or "sec-summary" not in h2_ids:
        errors.append("FAQまたはまとめのH2がありません")
    elif h2_ids.index("sec-summary") - h2_ids.index("sec-faq") != 1:
        errors.append("FAQはまとめの直前に配置してください")
    if not 3 <= len(parser.faq_questions) <= 5:
        errors.append(f"FAQは3〜5問必要です（現在{len(parser.faq_questions)}問）")
    invalid_faq = [question for question in parser.faq_questions if not re.match(r"^Q\.\s*\S", question)]
    if invalid_faq:
        errors.append("FAQ質問は先頭を `Q. ` にしてください: " + " / ".join(invalid_faq))

    if len(parser.updated_texts) != 1 or not re.fullmatch(
        r"最終更新日：\d{4}年\d{1,2}月\d{1,2}日", parser.updated_texts[0] if parser.updated_texts else ""
    ):
        errors.append("最終更新日は `最終更新日：YYYY年MM月DD日` 形式で1件必要です")
    expected_supervisor = [normalized_text(value) for value in template_parser.supervisor_texts]
    actual_supervisor = [normalized_text(value) for value in parser.supervisor_texts]
    if actual_supervisor != expected_supervisor:
        errors.append("監修者情報が article-template.html の確認済み表記と一致しません")
    visible = normalized_text(" ".join(parser.visible_text))
    if re.search(r"──|—|―", visible):
        errors.append("禁止ダッシュ（──／—／―）が読者表示テキストに残っています")

    if not allow_draft_placeholders and re.search(r"【(?:要記入|内部リンク要記入)[：:].*?】", text):
        errors.append("要記入プレースホルダが残っています")
    if not allow_draft_placeholders and re.search(r"<!--\s*要確認", text):
        errors.append("要確認コメントが残っています")
    if re.search(r"\{\{[^}]+\}\}", text):
        errors.append("テンプレートプレースホルダ {{...}} が残っています")
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        text, re.DOTALL | re.IGNORECASE,
    )
    if not scripts:
        errors.append("JSON-LDがありません")
    article_nodes = []
    for index, source in enumerate(scripts, 1):
        try:
            data = json.loads(source)
            article_nodes.extend(article_jsonld_nodes(data))
            for value in ("HEADLINE", "DESCRIPTION"):
                if contains_value(data, value):
                    errors.append(f"{value} が未置換です")
        except json.JSONDecodeError as exc:
            errors.append(f"JSON-LD {index} の構文エラー: {exc.msg}")
    if scripts and not article_nodes:
        errors.append("JSON-LDにArticleノードがありません")
    elif article_nodes and any(unresolved_description(node.get("description")) for node in article_nodes):
        errors.append("JSON-LDのArticle.descriptionに確定メタディスクリプションが必要です")

    if style_block(text) != style_block(template_text):
        errors.append("article-template.html のCSS枠が変更されています")

    handles = published_handles(published)
    for href in parser.internal_links:
        parts = [part for part in urlparse(href).path.split("/") if part]
        if len(parts) >= 3 and parts[0] == "blogs" and parts[2] not in handles:
            errors.append(f"未公開または未登録の内部リンク: {href}")

    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("article", type=Path)
    ap.add_argument("--template", type=Path, default=root / "article-template.html")
    ap.add_argument("--published", type=Path, default=root / "data/published-articles.md")
    ap.add_argument(
        "--allow-draft-placeholders",
        action="store_true",
        help="Google Drive下書き保存時だけ、要記入・要確認の残存を警告扱いにする",
    )
    args = ap.parse_args()
    if not args.article.exists():
        print(f"ERROR: 記事がありません: {args.article}", file=sys.stderr)
        return 2
    errors = validate(
        args.article,
        args.template,
        args.published,
        allow_draft_placeholders=args.allow_draft_placeholders,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    for warning in lint_warnings(args.article):
        print(f"WARNING: {warning}")
    print(f"PASS: {args.article}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
