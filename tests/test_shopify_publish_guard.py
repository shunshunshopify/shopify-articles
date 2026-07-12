import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/shopify_publish_guard.py"


def decision(query, variables=None):
    payload = {"tool_input": {"query": query, "variables": variables}}
    result = subprocess.run(
        [sys.executable, str(SCRIPT)], input=json.dumps(payload), text=True,
        capture_output=True, check=True,
    )
    return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"]


class PublishGuardTests(unittest.TestCase):
    def test_allows_literal_false(self):
        self.assertEqual(decision("mutation { articleCreate(article: {isPublished: false}) { article { id } } }"), "allow")

    def test_allows_variable_false(self):
        query = "mutation Create($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id } } }"
        self.assertEqual(decision(query, {"article": {"isPublished": False}}), "allow")

    def test_denies_missing_flag(self):
        self.assertEqual(decision("mutation { articleCreate(article: {title: \"x\"}) { article { id } } }"), "deny")

    def test_denies_true(self):
        self.assertEqual(decision("mutation { articleUpdate(article: {isPublished: true}) { article { id } } }"), "deny")

    def test_denies_publish_mutation(self):
        self.assertEqual(decision("mutation { publishablePublish(id: \"x\") { userErrors { message } } }"), "deny")

    def test_allows_unrelated_mutation(self):
        self.assertEqual(decision("mutation { tagsAdd(id: \"x\", tags: [\"a\"]) { userErrors { message } } }"), "allow")


if __name__ == "__main__":
    unittest.main()
