import tempfile
import unittest
from pathlib import Path

from scripts.article_validator import validate


class ArticleValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parent.parent
        cls.template = cls.root / "article-template.html"
        cls.published = cls.root / "data/published-articles.md"
        cls.article = cls.root / "drafts/shopify-product-page-improvement.html"

    def test_strict_mode_rejects_review_placeholder(self):
        source = self.article.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "article.html"
            candidate.write_text(source + "\n<!-- 要確認: test -->\n", encoding="utf-8")
            errors = validate(candidate, self.template, self.published)
        self.assertIn("要確認コメントが残っています", errors)

    def test_draft_mode_allows_review_placeholder(self):
        source = self.article.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "article.html"
            candidate.write_text(source + "\n<!-- 要確認: test -->\n", encoding="utf-8")
            errors = validate(
                candidate,
                self.template,
                self.published,
                allow_draft_placeholders=True,
            )
        self.assertNotIn("要確認コメントが残っています", errors)
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
