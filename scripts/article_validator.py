#!/usr/bin/env python3
"""Shopify記事HTMLの決定論的な公開前検証。"""

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
        self.custom_content_roots = 0
        self._in_toc = 0
        self._in_h2 = False
        self._h2_id = None
        self._h2_text = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
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
            self._h2_text = []

    def handle_endtag(self, tag):
        if tag == "div" and self._in_toc:
            self._in_toc -= 1
        if tag == "h2" and self._in_h2:
            self.h2.append((self._h2_id, "".join(self._h2_text).strip()))
            self._in_h2 = False

    def handle_data(self, data):
        if self._in_h2:
            self._h2_text.append(data)


def style_block(text):
    match = re.search(r"<style>(.*?)</style>", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


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


def validate(article, template, published, allow_draft_placeholders=False):
    errors = []
    text = article.read_text(encoding="utf-8")
    parser = ArticleParser()
    parser.feed(text)

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
    if "sec-faq" not in h2_ids or "sec-summary" not in h2_ids:
        errors.append("FAQまたはまとめのH2がありません")
    elif h2_ids.index("sec-summary") - h2_ids.index("sec-faq") != 1:
        errors.append("FAQはまとめの直前に配置してください")

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
    for index, source in enumerate(scripts, 1):
        try:
            data = json.loads(source)
            for value in ("HEADLINE", "DESCRIPTION"):
                if contains_value(data, value):
                    errors.append(f"{value} が未置換です")
        except json.JSONDecodeError as exc:
            errors.append(f"JSON-LD {index} の構文エラー: {exc.msg}")

    if style_block(text) != style_block(template.read_text(encoding="utf-8")):
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
    print(f"PASS: {args.article}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
