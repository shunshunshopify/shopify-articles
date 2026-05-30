#!/usr/bin/env python3
"""
PreToolUse ガード（Shopify graphql_mutation 用）

下書きの作成・更新（isPublished:false や isPublished 未指定）は自動許可(allow)し、
「公開」を示す操作だけは必ず人間に確認(ask)させる。

判定が曖昧・パース不能な場合は安全側（ask）に倒す。
SOLSTARワークスペースの最重要ルール「自動公開は禁止」を機械的に担保する。

入力: stdin の JSON  { "tool_name": ..., "tool_input": { "query": ..., "variables": {...} } }
出力: stdout の JSON  { "hookSpecificOutput": { "hookEventName": "PreToolUse",
                        "permissionDecision": "allow"|"ask", "permissionDecisionReason": ... } }
"""
import sys
import re
import json


def decide(allow, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow" if allow else "ask",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def has_published_true(obj):
    """variables(辞書/配列)を再帰的に走査し isPublished が真の値かを判定。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() == "ispublished":
                if v is True or (isinstance(v, str) and v.strip().lower() == "true"):
                    return True
            if has_published_true(v):
                return True
    elif isinstance(obj, list):
        for v in obj:
            if has_published_true(v):
                return True
    return False


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except Exception:
        decide(False, "フック入力をパースできなかったため、安全側で人間に確認します。")

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
    if has_published_true(vars_obj):
        decide(False, "variables に isPublished=true が含まれます（公開操作の可能性）。人間に確認します。")

    # 2) query 文字列内で isPublished にリテラル true を代入している
    if re.search(r"isPublished\s*:\s*true", query, re.IGNORECASE):
        decide(False, "mutation 内で isPublished: true を指定しています（公開操作）。人間に確認します。")

    # 3) 公開系 mutation 名・キーワード
    publish_markers = ["articlepublish", "publishablepublish", "publishpublish"]
    low = query.lower()
    for m in publish_markers:
        if m in low:
            decide(False, f"公開系の操作（{m}）を検出しました。人間に確認します。")

    # 4) variables が文字列でパースできず、その中に isPublished と true の両方が出現
    if isinstance(variables, str):
        vlow = variables.lower()
        if "ispublished" in vlow and "true" in vlow:
            decide(False, "variables 文字列に isPublished と true が含まれます（公開の可能性）。人間に確認します。")

    # --- ここまで該当なし＝下書き相当として自動許可 ---
    decide(True, "下書きの作成・更新（公開兆候なし）と判断し、自動許可します。")


if __name__ == "__main__":
    main()
