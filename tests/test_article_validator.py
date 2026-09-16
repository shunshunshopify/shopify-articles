import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.article_validator import JSONLD_PATTERN, article_jsonld_nodes, lint_warnings, validate


class ArticleValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parent.parent
        cls.template = cls.root / "article-template.html"
        cls.published = cls.root / "data/published-articles.md"
        cls.article = cls.root / "drafts/shopify-product-page-improvement.html"
        template_source = cls.template.read_text(encoding="utf-8")
        article_source = cls.article.read_text(encoding="utf-8")
        supervisor = re.search(
            r'<p class="article-supervisor">.*?</p>', template_source, re.DOTALL
        ).group(0)
        source = re.sub(
            r'<p class="article-supervisor">.*?</p>',
            supervisor,
            article_source,
            count=1,
            flags=re.DOTALL,
        )
        template_style = re.search(r"<style>.*?</style>", template_source, re.DOTALL).group(0)
        cls.source = re.sub(
            r"<style>.*?</style>", template_style, source, count=1, flags=re.DOTALL
        )
        # Test fixture metadata is explicit; do not change the real draft or infer its author.
        cls.source = cls.source.replace("2026-07-21T10:00:00+09:00", "2026-07-12T10:00:00+09:00")
        cls.source = cls.source.replace('"@type": "Person",', '"@type": "Person", "name": "テスト著者",')
        article = article_jsonld_nodes(json.loads(JSONLD_PATTERN.search(cls.source).group(1)))[0]
        cls.meta = article["description"]
        cls.brief_text = '## 機械検証用メタデータ\n\n```json\n' + json.dumps(
            {"meta_description": cls.meta}, ensure_ascii=False
        ) + '\n```\n'

    def validate_source(self, source, allow_draft_placeholders=True, brief_text=None, original=None):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "article.html"
            candidate.write_text(source, encoding="utf-8")
            brief = candidate.with_name("article-brief.md")
            brief.write_text(self.brief_text if brief_text is None else brief_text, encoding="utf-8")
            original_path = None
            if original is not None:
                original_path = Path(directory) / "original.html"
                original_path.write_text(original, encoding="utf-8")
            return validate(
                candidate,
                self.template,
                self.published,
                allow_draft_placeholders=allow_draft_placeholders,
                source=original_path,
            )

    def change_article(self, **changes):
        document = json.loads(JSONLD_PATTERN.search(self.source).group(1))
        article = article_jsonld_nodes(document)[0]
        for key, value in changes.items():
            if value is None:
                article.pop(key, None)
            else:
                article[key] = value
        return JSONLD_PATTERN.sub(
            lambda _: '<script type="application/ld+json">' + json.dumps(document, ensure_ascii=False) + '</script>',
            self.source,
        )

    def test_internal_link_requires_correct_blog(self):
        source = self.source + '<a href="/blogs/marketing/shopify-theme-ranking">関連記事</a>'
        self.assertTrue(any('未公開または未登録の内部リンク' in error for error in self.validate_source(source)))

    def test_absolute_internal_link_is_checked(self):
        source = self.source + '<a href="https://solstar.co.jp/blogs/shopify/missing-article">関連記事</a>'
        self.assertTrue(any('未公開または未登録の内部リンク' in error for error in self.validate_source(source)))

    def test_registered_absolute_internal_link_is_allowed(self):
        source = self.source + '<a href="https://solstar.co.jp/blogs/shopify/shopify-theme-ranking?ref=article#section1">関連記事</a>'
        self.assertFalse(any('未公開または未登録の内部リンク' in error for error in self.validate_source(source)))

    def test_strict_mode_accepts_verified_metadata(self):
        self.assertEqual([], self.validate_source(self.source, allow_draft_placeholders=False))

    def test_meta_mismatch_fails_in_both_modes(self):
        source = self.change_article(description="内容と無関係なメタです")
        for draft in (False, True):
            with self.subTest(draft=draft):
                self.assertTrue(any("完全一致" in error for error in self.validate_source(source, draft)))

    def test_missing_malformed_or_duplicate_brief_meta_fails(self):
        for brief in ("# 古いブリーフ", self.brief_text * 2,
                      '## 機械検証用メタデータ\n```json\n{invalid}\n```',
                      '## 機械検証用メタデータ\n```json\n{"meta_description":"a","meta_description":"b"}\n```'):
            with self.subTest(brief=brief):
                self.assertTrue(any("取得できません" in error for error in self.validate_source(self.source, brief_text=brief)))

    def test_empty_placeholder_or_nonstring_meta_fails(self):
        for value in ("", "TODO", "DESCRIPTION", "【要記入: メタ】", 123, ["a", "b"], "前半\n後半", " 前後の空白 "):
            with self.subTest(value=value):
                brief = '## 機械検証用メタデータ\n```json\n' + json.dumps({"meta_description": value}) + '\n```'
                self.assertTrue(any("取得できません" in error for error in self.validate_source(self.source, brief_text=brief)))

    def test_meta_section_can_be_followed_by_other_sections(self):
        self.assertEqual([], self.validate_source(self.source, brief_text=self.brief_text + '\n## 用語計画\n本文'))

    def test_strict_rejects_publication_tokens_but_draft_allows_them(self):
        source = self.change_article(datePublished="DATE_PUBLISHED", dateModified="DATE_MODIFIED",
                                     mainEntityOfPage={"@id": "PAGE_URL#webpage"})
        self.assertEqual([], self.validate_source(source))
        self.assertTrue(any("公開用プレースホルダ" in error for error in self.validate_source(source, False)))
        for field, value in (("@id", "PAGE_URL#article"), ("name", "BLOG_NAME"), ("url", "BLOG_URL")):
            with self.subTest(field=field):
                candidate = self.change_article(**{field: value})
                self.assertTrue(any("公開用プレースホルダ" in error for error in self.validate_source(candidate, False)))

    def test_new_unpublished_article_can_omit_publication_date_and_author(self):
        self.assertEqual([], self.validate_source(self.change_article(datePublished=None, author=None), False))

    def test_invalid_iso_dates_fail_even_in_draft_mode(self):
        for value in ("2026-02-30", "2026/07/12", "2026-07-12T10:00:00", 123, ""):
            with self.subTest(value=value):
                self.assertTrue(any("ISO8601" in error for error in self.validate_source(self.change_article(dateModified=value))))

    def test_missing_modified_date_fails(self):
        self.assertTrue(any("dateModified" in error for error in self.validate_source(self.change_article(dateModified=None))))

    def test_modified_date_must_match_visible_date(self):
        self.assertTrue(any("最終更新日が一致" in error for error in self.validate_source(self.change_article(dateModified="2026-07-13"))))

    def test_dates_are_compared_in_jst(self):
        self.assertEqual([], self.validate_source(self.change_article(dateModified="2026-07-11T15:00:00Z"), False))

    def test_publication_date_cannot_follow_modified_date(self):
        self.assertTrue(any("より後" in error for error in self.validate_source(self.change_article(datePublished="2026-07-13"))))

    def test_visible_date_must_exist(self):
        source = self.source.replace("最終更新日：2026年07月12日", "最終更新日：2026年02月30日")
        self.assertTrue(any("実在しない" in error for error in self.validate_source(source)))

    def test_invalid_page_url_fails(self):
        for value in ("/relative", "javascript:alert(1)", "https://", "https://bad host/", 123, {}):
            with self.subTest(value=value):
                self.assertTrue(any("絶対HTTP(S)" in error for error in self.validate_source(self.change_article(mainEntityOfPage=value), False)))

    def test_url_and_id_must_be_strings(self):
        for field in ('url', '@id'):
            with self.subTest(field=field):
                source = self.change_article(**{field: 123})
                self.assertTrue(any("文字列で指定" in error for error in self.validate_source(source)))

    def test_author_requires_name_and_valid_type_when_provided(self):
        for author in ({"@type": "Person", "@id": "https://example.com/#person"},
                       {"@type": [], "name": "テスト"}, [], "テスト"):
            with self.subTest(author=author):
                self.assertTrue(any("author" in error for error in self.validate_source(self.change_article(author=author))))

    def test_duplicate_jsonld_keys_fail(self):
        source = self.source.replace('"dateModified":', '"dateModified": "2026-07-12", "dateModified":')
        self.assertTrue(any("重複したJSONキー" in error for error in self.validate_source(source)))

    def test_prepared_copy_accepts_only_jsonld_changes(self):
        original = self.change_article(dateModified="DATE_MODIFIED", datePublished="DATE_PUBLISHED")
        self.assertEqual([], self.validate_source(self.source, False, original=original))
        changed = self.source.replace("広告やSNSから", "変更した本文から", 1)
        self.assertNotEqual(changed, self.source)
        self.assertTrue(any("JSON-LD以外" in error for error in self.validate_source(changed, False, original=original)))

    def test_cli_requires_brief_and_accepts_explicit_brief_for_delivery_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            article = Path(directory) / "delivery.html"
            article.write_text(self.source, encoding="utf-8")
            command = [sys.executable, '-B', str(self.root / 'scripts/article_validator.py'), str(article)]
            missing = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(1, missing.returncode)
            self.assertIn("取得できません", missing.stdout)
            brief = Path(directory) / 'source-brief.md'
            brief.write_text(self.brief_text, encoding='utf-8')
            valid = subprocess.run(command + ['--brief', str(brief)], capture_output=True, text=True)
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)

    def test_latest_template_draft_to_delivery_flow(self):
        source = self.template.read_text(encoding='utf-8')
        source = re.sub(r'\{\{([^}]+)\}\}',
                        lambda m: '2026年09月16日' if m.group(1) == 'LAST_UPDATED' else '検証用の説明', source)
        # Resolve only JSON-LD; keep source comments, body, CSS and TOC untouched.
        def resolve_draft(match):
            document = json.loads(match.group(1))
            def fill(value):
                if isinstance(value, dict):
                    return {k: fill(v) for k, v in value.items()}
                if isinstance(value, list):
                    return [fill(v) for v in value]
                return {'HEADLINE': '検証用記事', 'DESCRIPTION': self.meta}.get(value, value)
            return '<script type="application/ld+json">' + json.dumps(fill(document), ensure_ascii=False) + '</script>'
        draft = JSONLD_PATTERN.sub(resolve_draft, source)
        self.assertEqual([], self.validate_source(draft))
        document = json.loads(JSONLD_PATTERN.search(draft).group(1))
        article_jsonld_nodes(document)[0].pop('datePublished')
        text = json.dumps(document, ensure_ascii=False)
        for token, value in (
            ('PAGE_URL', 'https://www.solstar.co.jp/blogs/marketing/test-article'),
            ('BLOG_URL', 'https://www.solstar.co.jp/blogs/marketing'),
            ('BLOG_NAME', 'Marketing'), ('DATE_MODIFIED', '2026-09-16'),
        ):
            text = text.replace(token, value)
        delivery = JSONLD_PATTERN.sub(lambda _: '<script type="application/ld+json">' + text + '</script>', draft)
        self.assertEqual([], self.validate_source(delivery, False, original=draft))

    def test_strict_mode_rejects_review_placeholder(self):
        errors = self.validate_source(
            self.source + "\n<!-- 要確認: test -->\n",
            allow_draft_placeholders=False,
        )
        self.assertIn("要確認コメントが残っています", errors)

    def test_draft_mode_allows_review_placeholder(self):
        errors = self.validate_source(self.source + "\n<!-- 要確認: test -->\n")
        self.assertNotIn("要確認コメントが残っています", errors)
        self.assertEqual([], errors)

    def test_rejects_faq_without_q_prefix(self):
        source = self.source.replace("<h3>Q. 商品ページ改善", "<h3>商品ページ改善", 1)
        errors = self.validate_source(source)
        self.assertTrue(any("FAQ質問は先頭" in error for error in errors))

    def test_rejects_unapproved_supervisor_copy(self):
        source = self.source.replace("Shopify開発歴8年以上", "Shopify開発歴9年以上", 1)
        errors = self.validate_source(source)
        self.assertIn("監修者情報が article-template.html の確認済み表記と一致しません", errors)

    def test_rejects_prohibited_dash(self):
        source = self.source.replace("広告やSNSから", "広告やSNSから—", 1)
        errors = self.validate_source(source)
        self.assertIn("禁止ダッシュ（──／—／―）が読者表示テキストに残っています", errors)

    def test_rejects_empty_article_meta_description(self):
        source = re.sub(
            r'("description"\s*:\s*)"[^"]*"',
            r'\1""',
            self.source,
            count=1,
        )
        errors = self.validate_source(source)
        self.assertIn("JSON-LDのArticle.descriptionに確定メタディスクリプションが必要です", errors)

    def test_rejects_missing_article_jsonld_node(self):
        source = self.source.replace('"@type": "Article"', '"@type": "WebPage"', 1)
        errors = self.validate_source(source)
        self.assertIn("JSON-LDにArticleノードがありません", errors)

    def test_rejects_learn_list_outside_required_range(self):
        block = re.search(
            r'(<h2 id="sec-learn">この記事でわかること</h2>\s*<ul>)(.*?)(</ul>)',
            self.source,
            re.DOTALL,
        )
        items = re.findall(r"<li>.*?</li>", block.group(2), re.DOTALL)
        short_block = block.group(1) + "\n".join(items[:3]) + block.group(3)
        source = self.source[:block.start()] + short_block + self.source[block.end():]
        errors = self.validate_source(source)
        self.assertTrue(any("4〜6項目必要" in error for error in errors))

    def test_warns_about_long_and_formulaic_intro(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "article.html"
            candidate.write_text(self.source, encoding="utf-8")
            warnings = lint_warnings(candidate)
        self.assertTrue(any("導入文は300字程度" in warning for warning in warnings))
        self.assertIn("導入文に固定的な「単に〜だけでなく」構文があります", warnings)

    def test_rejects_template_style_that_is_not_latest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = root / "article.html"
            candidate.write_text(self.source, encoding="utf-8")
            template = root / "article-template.html"
            template.write_text(
                self.template.read_text(encoding="utf-8").replace("#AB8C52", "#1a73e8", 1),
                encoding="utf-8",
            )
            theme_dir = root / "theme-css"
            theme_dir.mkdir()
            (theme_dir / "solstar-article.css").write_text(
                (self.root / "theme-css/solstar-article.css").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            errors = validate(candidate, template, self.published, allow_draft_placeholders=True)
        self.assertIn(
            "article-template.html のStyleが theme-css/solstar-article.css の最新版と一致しません",
            errors,
        )

    def test_rejects_missing_canonical_style(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = root / "article.html"
            candidate.write_text(self.source, encoding="utf-8")
            template = root / "article-template.html"
            template.write_text(self.template.read_text(encoding="utf-8"), encoding="utf-8")
            errors = validate(candidate, template, self.published, allow_draft_placeholders=True)
        self.assertIn("最新版Styleがありません: theme-css/solstar-article.css", errors)


if __name__ == "__main__":
    unittest.main()
