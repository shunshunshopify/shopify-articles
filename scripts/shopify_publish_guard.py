#!/usr/bin/env python3
"""
PreToolUse ガード（Shopify graphql_mutation 用）

記事の作成・更新は isPublished:false が明示された場合だけ許可し、
記事作成は有効なMeta description（global.description_tag）が含まれる場合だけ許可する。
公開操作やSEOメタフィールドが欠けた記事作成は拒否(deny)する。

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


def valid_description(value):
    """Shopify SEO欄へ保存できる、未解決でない説明文かを返す。"""
    if not isinstance(value, str) or not value.strip():
        return False
    text = value.strip()
    if text in {"DESCRIPTION", "META_DESCRIPTION"}:
        return False
    return not re.search(r"\{\{[^}]+\}\}|【(?:要記入|要確認)[：:].*?】|<!--\s*要確認", text)


def seo_descriptions(obj):
    """variablesを再帰走査し、global.description_tag の値と型を返す。"""
    found = []
    if isinstance(obj, dict):
        namespace = obj.get("namespace")
        key = obj.get("key")
        if namespace == "global" and key == "description_tag":
            found.append((obj.get("value"), obj.get("type")))
        for value in obj.values():
            found.extend(seo_descriptions(value))
    elif isinstance(obj, list):
        for value in obj:
            found.extend(seo_descriptions(value))
    return found


def inline_seo_descriptions(query, variables):
    """GraphQL内へ直接記述されたglobal.description_tagを抽出する。"""
    found = []
    for block in re.findall(r"\{[^{}]*\}", query, re.DOTALL):
        if not re.search(r'namespace\s*:\s*"global"', block):
            continue
        if not re.search(r'key\s*:\s*"description_tag"', block):
            continue
        type_match = re.search(r'type\s*:\s*"([^"]+)"', block)
        value_match = re.search(r'value\s*:\s*(?:"([^"]*)"|\$([A-Za-z_][A-Za-z0-9_]*))', block)
        if not value_match:
            found.append((None, type_match.group(1) if type_match else None))
            continue
        literal, variable_name = value_match.groups()
        value = literal
        if variable_name and isinstance(variables, dict):
            value = variables.get(variable_name)
        found.append((value, type_match.group(1) if type_match else None))
    return found


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

    # 新規記事はShopifyの検索結果用SEO欄を必須にする。summaryは代替にならない。
    is_article_create = bool(re.search(r"\barticleCreate\b", query, re.IGNORECASE))
    if is_article_create:
        descriptions = seo_descriptions(vars_obj)
        descriptions.extend(inline_seo_descriptions(query, vars_obj))
        valid = any(
            field_type == "single_line_text_field" and valid_description(value)
            for value, field_type in descriptions
        )
        if not valid:
            decide(
                "deny",
                "articleCreate には有効なMeta descriptionを metafields の "
                "global.description_tag（single_line_text_field）として必ず設定してください。"
            )

    decide(
        "allow",
        "公開操作ではなく、記事操作には isPublished:false が明示され、"
        "記事作成にはMeta descriptionが設定されています。"
    )


if __name__ == "__main__":
    main()
