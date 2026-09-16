import json
import re
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
    def test_hook_matches_current_and_legacy_mutation_names(self):
        config = json.loads((SCRIPT.parent.parent / '.codex/hooks.json').read_text())
        matcher = config['hooks']['PreToolUse'][0]['matcher']
        for name in ['mcp__codex_apps__shopify_graphql_mutation', 'mcp__shopify__graphql_mutation']:
            self.assertIsNotNone(re.fullmatch(matcher, name))
        self.assertIsNone(re.fullmatch(matcher, 'mcp__codex_apps__shopify_graphql_query'))

    def safe_article(self):
        return {"isPublished": False, "metafields": [{
            "namespace": "global", "key": "description_tag",
            "type": "single_line_text_field", "value": "確定した説明文です。",
        }]}

    def test_unused_variables_cannot_authorize_article(self):
        query = 'mutation($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id } } }'
        self.assertEqual(decision(query, {"article": {"title": "x"}, "unused": self.safe_article()}), "deny")

    def test_each_article_in_batch_requires_own_description(self):
        query = 'mutation($safe: ArticleCreateInput!, $unsafe: ArticleCreateInput!) { a: articleCreate(article: $safe) { article { id } } b: articleCreate(article: $unsafe) { article { id } } }'
        self.assertEqual(decision(query, {"safe": self.safe_article(), "unsafe": {"isPublished": False}}), "deny")

    def test_comments_cannot_supply_false_flag(self):
        query = 'mutation { articleUpdate(article: {title: "isPublished:false"}) { article { id } } # isPublished:false\n }'
        self.assertEqual(decision(query), "deny")

    def test_string_false_is_not_boolean_false(self):
        self.assertEqual(decision('mutation { articleUpdate(article: {isPublished: "false"}) { article { id } } }'), "deny")

    def test_rejects_missing_runtime_variable_despite_default(self):
        self.assertEqual(decision('mutation($draft: Boolean = false) { articleUpdate(article: {isPublished: $draft}) { article { id } } }'), "deny")

    def test_aliased_publish_is_rejected(self):
        self.assertEqual(decision('mutation { safe: publishablePublish(id: "x") { userErrors { message } } }'), "deny")

    def test_rejects_empty_or_malformed_mutation(self):
        for query in ['', None, {}, 'mutation {}', 'query { article { id } }', 'mutation { articleUpdate(', 'mutation { tagsAdd(id:"x") {id} } mutation { tagsAdd(id:"x") {id} }']:
            with self.subTest(query=query):
                self.assertEqual(decision(query), "deny")

    def test_rejects_invalid_variables(self):
        for variables in ['{broken', [], 1]:
            with self.subTest(variables=variables):
                self.assertEqual(decision('mutation { tagsAdd(id: "x") { userErrors { message } } }', variables), "deny")

    def test_rejects_duplicate_input_keys(self):
        self.assertEqual(decision('mutation { articleUpdate(article: {isPublished: true, isPublished: false}) { article { id } } }'), "deny")

    def test_rejects_publication_date(self):
        self.assertEqual(decision('mutation { articleUpdate(article: {isPublished: false, publishedAt: "2030-01-01T00:00:00Z"}) { article { id } } }'), "deny")

    def test_allows_escaped_literal_and_alias(self):
        article = self.safe_article()
        article['metafields'][0]['value'] = '「例」と英語の"example"を含む説明文。'
        self.assertEqual(decision('mutation($article: ArticleCreateInput!) { draft: articleCreate(article: $article) { article { id } } }', {"article": article}), "allow")

    def test_rejects_todo_description(self):
        article = self.safe_article()
        article['metafields'][0]['value'] = 'TODO'
        self.assertEqual(decision('mutation($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id } } }', {"article": article}), "deny")

    def test_allows_literal_false_with_inline_meta_description(self):
        query = '''mutation Create($description: String!) {
          articleCreate(article: {
            isPublished: false
            metafields: [{namespace: "global", key: "description_tag", type: "single_line_text_field", value: $description}]
          }) { article { id } }
        }'''
        self.assertEqual(decision(query, {"description": "記事の内容と読了メリットが分かる説明文です。"}), "allow")

    def test_allows_variable_false_with_meta_description(self):
        query = "mutation Create($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id } } }"
        variables = {
            "article": {
                "isPublished": False,
                "metafields": [{
                    "namespace": "global",
                    "key": "description_tag",
                    "type": "single_line_text_field",
                    "value": "記事の内容と読了メリットが分かる説明文です。",
                }],
            }
        }
        self.assertEqual(decision(query, variables), "allow")

    def test_denies_missing_flag(self):
        self.assertEqual(decision("mutation { articleCreate(article: {title: \"x\"}) { article { id } } }"), "deny")

    def test_denies_missing_meta_description(self):
        query = "mutation { articleCreate(article: {isPublished: false, summary: \"説明文\"}) { article { id } } }"
        self.assertEqual(decision(query), "deny")

    def test_denies_empty_meta_description(self):
        query = "mutation Create($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id } } }"
        variables = {
            "article": {
                "isPublished": False,
                "metafields": [{
                    "namespace": "global",
                    "key": "description_tag",
                    "type": "single_line_text_field",
                    "value": "   ",
                }],
            }
        }
        self.assertEqual(decision(query, variables), "deny")

    def test_denies_placeholder_meta_description(self):
        query = "mutation Create($article: ArticleCreateInput!) { articleCreate(article: $article) { article { id } } }"
        variables = {
            "article": {
                "isPublished": False,
                "metafields": [{
                    "namespace": "global",
                    "key": "description_tag",
                    "type": "single_line_text_field",
                    "value": "DESCRIPTION",
                }],
            }
        }
        self.assertEqual(decision(query, variables), "deny")

    def test_denies_true(self):
        self.assertEqual(decision("mutation { articleUpdate(article: {isPublished: true}) { article { id } } }"), "deny")

    def test_allows_article_update_without_resending_existing_meta(self):
        self.assertEqual(decision("mutation { articleUpdate(article: {isPublished: false}) { article { id } } }"), "allow")

    def test_denies_publish_mutation(self):
        self.assertEqual(decision("mutation { publishablePublish(id: \"x\") { userErrors { message } } }"), "deny")

    def test_allows_unrelated_mutation(self):
        self.assertEqual(decision("mutation { tagsAdd(id: \"x\", tags: [\"a\"]) { userErrors { message } } }"), "allow")


if __name__ == "__main__":
    unittest.main()
