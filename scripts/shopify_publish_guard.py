#!/usr/bin/env python3
"""Shopify mutation guard. Read hook JSON from stdin and return an allow/deny JSON.

Only a single explicit mutation is supported. Unsupported syntax fails closed;
this restricted input parser does not replace Shopify's schema validation.
Callers must read permissionDecision: exit status 0 only means the hook ran.
"""
import json
import re
import sys


class InvalidInput(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidInput('重複したキーがあります')
        result[key] = value
    return result


def valid_description(value):
    if not isinstance(value, str) or not value.strip() or '\n' in value or '\r' in value:
        return False
    if value.strip() in {'DESCRIPTION', 'META_DESCRIPTION', 'TODO', 'TBD', '仮', '未定'}:
        return False
    return not re.search(r'\{\{[^}]+\}\}|【(?:要記入|要確認|内部リンク要記入)[：:].*?】|<!--\s*要確認', value)


TOKEN = re.compile(r'\s+|,|\#[^\r\n]*|"(?:[^"\\\x00-\x1f]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*"|[_A-Za-z][_0-9A-Za-z]*|-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?|[!$():=@\[\]{}]')
NAME = re.compile(r'[_A-Za-z][_0-9A-Za-z]*\Z')


class MutationParser:
    def __init__(self, query, variables):
        if not isinstance(query, str) or not query.strip():
            raise InvalidInput('mutationが空または文字列ではありません')
        self.tokens = []
        pos = 0
        while pos < len(query):
            match = TOKEN.match(query, pos)
            if not match:
                raise InvalidInput('未対応または不正なGraphQL構文です')
            token = match.group()
            pos = match.end()
            if not token.isspace() and token != ',' and not token.startswith('#'):
                self.tokens.append(token)
        self.index = 0
        self.variables = variables

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def take(self, expected=None):
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise InvalidInput('GraphQL構文を確認できません')
        self.index += 1
        return token

    def name(self):
        token = self.take()
        if not NAME.fullmatch(token):
            raise InvalidInput('GraphQL名が不正です')
        return token

    def value(self):
        token = self.peek()
        if token == '$':
            self.take('$')
            name = self.name()
            if name not in self.variables:
                raise InvalidInput('実際のvariablesに必要な変数がありません')
            return self.variables[name]
        if token == '{':
            return self.mapping('{', '}')
        if token == '[':
            self.take('[')
            values = []
            while self.peek() != ']':
                values.append(self.value())
            self.take(']')
            return values
        token = self.take()
        if token.startswith('"') or token in {'true', 'false', 'null'} or re.match(r'-?\d', token):
            return json.loads(token)
        if NAME.fullmatch(token):
            return token
        raise InvalidInput('入力値を解析できません')

    def mapping(self, opening, closing):
        self.take(opening)
        pairs = []
        while self.peek() != closing:
            key = self.name()
            self.take(':')
            pairs.append((key, self.value()))
        self.take(closing)
        return unique_object(pairs)

    def skip_group(self):
        closing = {'(': ')', '{': '}', '[': ']'}
        end = closing[self.take()]
        while self.peek() != end:
            if self.peek() in closing:
                self.skip_group()
            elif self.peek() in {None, ')', '}', ']'}:
                raise InvalidInput('括弧が対応していません')
            else:
                self.take()
        self.take(end)

    def parse(self):
        self.take('mutation')
        if self.peek() not in {'(', '{'}:
            self.name()
        if self.peek() == '(':
            # Default values are never treated as supplied variables by this guard.
            self.skip_group()
        self.take('{')
        fields = []
        while self.peek() != '}':
            name = self.name()
            if self.peek() == ':':
                self.take(':')
                name = self.name()
            arguments = self.mapping('(', ')') if self.peek() == '(' else {}
            fields.append((name, arguments))
            if self.peek() == '{':
                self.skip_group()
        self.take('}')
        if self.peek() is not None or not fields:
            raise InvalidInput('複数operationまたは空のmutationは許可しません')
        return fields


def evaluate(data):
    if not isinstance(data, dict) or not isinstance(data.get('tool_input'), dict):
        raise InvalidInput('フック入力にはtool_inputオブジェクトが必要です')
    tool_input = data['tool_input']
    variables = tool_input.get('variables')
    if isinstance(variables, str):
        variables = json.loads(variables, object_pairs_hook=unique_object)
    if variables is None:
        variables = {}
    if not isinstance(variables, dict):
        raise InvalidInput('variablesはオブジェクトで指定してください')
    fields = MutationParser(tool_input.get('query'), variables).parse()
    for name, arguments in fields:
        if 'publish' in name.lower():
            raise InvalidInput('公開に関係するmutationは人間が行ってください')
        if name not in {'articleCreate', 'articleUpdate'}:
            if name.lower().startswith('article'):
                raise InvalidInput('未対応の記事mutationは許可しません')
            continue
        article = arguments.get('article')
        if not isinstance(article, dict) or article.get('isPublished') is not False:
            raise InvalidInput('各記事の実際のarticle入力にbooleanのisPublished:falseが必要です')
        # Publication timing is outside this automated draft-only workflow.
        if article.get('publishedAt') is not None:
            raise InvalidInput('公開日時の指定は許可しません')
        if name == 'articleCreate':
            metafields = article.get('metafields', [])
            if not isinstance(metafields, list) or not all(isinstance(field, dict) for field in metafields):
                raise InvalidInput('記事のmetafieldsはオブジェクトの配列で指定してください')
            descriptions = [field for field in metafields if field.get('namespace') == 'global' and field.get('key') == 'description_tag']
            if len(descriptions) != 1 or descriptions[0].get('type') != 'single_line_text_field' or not valid_description(descriptions[0].get('value')):
                raise InvalidInput('各articleCreateに有効なglobal.description_tagを1つ設定してください')
    return 'allow', '実際の各記事入力の下書き指定と記事作成時のMeta descriptionを確認しました。'


def main():
    try:
        decision, reason = evaluate(json.loads(sys.stdin.read(), object_pairs_hook=unique_object))
    except (ValueError, TypeError, RecursionError) as exc:
        decision, reason = 'deny', '入力を安全に確認できないため拒否します: ' + str(exc)
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'PreToolUse', 'permissionDecision': decision,
        'permissionDecisionReason': reason,
    }}, ensure_ascii=False))


if __name__ == '__main__':
    main()
