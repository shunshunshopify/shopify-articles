import re
import tempfile
import unittest
from pathlib import Path

from scripts.article_validator import lint_warnings, validate


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
        cls.source = re.sub(
            r'<p class="article-supervisor">.*?</p>',
            supervisor,
            article_source,
            count=1,
            flags=re.DOTALL,
        )

    def validate_source(self, source, allow_draft_placeholders=True):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "article.html"
            candidate.write_text(source, encoding="utf-8")
            return validate(
                candidate,
                self.template,
                self.published,
                allow_draft_placeholders=allow_draft_placeholders,
            )

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


if __name__ == "__main__":
    unittest.main()
