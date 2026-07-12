#!/usr/bin/env python3
"""
PreToolUse ガード（Shopify graphql_mutation 用）

記事の作成・更新は isPublished:false が明示された場合だけ許可し、
公開操作は拒否(deny)する。

判定が曖昧・パース不能な場合は安全側（deny）に倒す。
SOLSTARワークスペースの最重要ルール「自動公開は禁止」を機械的に担保する。

入力: stdin の JSON  { "tool_name": ..., "tool_input": { "query": ..., "variables": {...} } }
出力: stdout の JSON  { "hookSpecificOutput": { "hookEventName": "PreToolUse",
                        "permissionDecision": "allow"|"deny", "permissionDecisionReason": ... } }
"""
import sys
import re
import json


def decide(decision, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def published_values(obj):
    """variablesを再帰走査し、isPublished の値をすべて返す。"""
    values = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() == "ispublished":
                values.append(v)
            values.extend(published_values(v))
    elif isinstance(obj, list):
        for v in obj:
            values.extend(published_values(v))
    return values


def is_true(value):
    return value is True or (isinstance(value, str) and value.strip().lower() == "true")


def is_false(value):
    return value is False or (isinstance(value, str) and value.strip().lower() == "false")


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except Exception:
        decide("deny", "フック入力をパースできないため、Shopify mutationを拒否します。")

    tool_input = data.get("tool_input") or {}
    query = tool_input.get("query") or ""
    variables = tool_input.get("variables")

    if not isinstance(query, str):
        query = str(query)

    # variables を辞書として走査（文字列で来た場合はパースを試みる）
    vars_obj = variables
    if isinstance(variables, str):
        try:
            vars_obj = json.loads(variables)
        except Exception:
            vars_obj = None
            # 文字列のまま後段の文字列検査に回す

    # --- 公開を示す兆候の検査 ---

    # 1) variables 内に isPublished=true が含まれる
    values = published_values(vars_obj)
    if any(is_true(value) for value in values):
        decide("deny", "variables に isPublished=true が含まれるため、公開操作を拒否します。")

    # 2) query 文字列内で isPublished にリテラル true を代入している
    if re.search(r"isPublished\s*:\s*true", query, re.IGNORECASE):
        decide("deny", "mutation 内で isPublished:true が指定されているため、公開操作を拒否します。")

    # 3) 公開系 mutation 名・キーワード
    publish_markers = ["articlepublish", "publishablepublish", "publishpublish"]
    low = query.lower()
    for m in publish_markers:
        if m in low:
            decide("deny", f"公開系の操作（{m}）を検出したため拒否します。公開は管理画面で人間が行ってください。")

    # 4) variables が文字列でパースできず、その中に isPublished と true の両方が出現
    if isinstance(variables, str):
        vlow = variables.lower()
        if "ispublished" in vlow and "true" in vlow:
            decide("deny", "解析不能なvariablesに公開指定の可能性があるため拒否します。")

    # 記事作成・更新では、公開指定がないだけでは不十分。false の明示を必須にする。
    is_article_write = bool(re.search(r"\barticle(?:Create|Update)\b", query, re.IGNORECASE))
    literal_false = bool(re.search(r"isPublished\s*:\s*false", query, re.IGNORECASE))
    variable_false = any(is_false(value) for value in values)
    if is_article_write and not (literal_false or variable_false):
        decide("deny", "articleCreate/articleUpdate には isPublished:false の明示が必要です。")

    decide("allow", "公開操作ではなく、記事操作には isPublished:false が明示されています。")


if __name__ == "__main__":
    main()
