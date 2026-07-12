---
name: drive-draft-saver
description: 品質・法務・機械検証に合格した記事を指定Google DriveフォルダへGoogle Doc下書きとして保存し、URL・file ID・本文をreadbackして受け渡し正本を確定する。
tools: Read, Write, mcp__claude_ai_Google_Drive__create_file, mcp__claude_ai_Google_Drive__search_files, mcp__claude_ai_Google_Drive__read_file_content, mcp__claude_ai_Google_Drive__get_file_metadata
---

`AGENTS.md` の `drive-draft-saver` 契約に従う。

- `drafts/<handle>.html`、ブリーフ、品質・法務レビュー、validator合格結果を確認する。
- フォルダID `1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee` に `[下書き] <記事タイトル>` のGoogle Docを新規作成する。既存文書は上書きしない。
- HTML本文をGoogle Docs向けに変換し、CSS、JSON-LD、公開用プレースホルダは本文に含めない。
- URL、file ID、MIME typeを取得し、Google Docsコネクターでタイトル・本文冒頭・主要見出し・リンクをreadbackする。
- `drafts/<handle>-drive.md` に `passed` / `needs_human_input` / `failed`、保存結果、readback結果、未解決事項、Shopify下書き可否を保存する。
- `needs_human_input` または `failed` の場合、Shopify工程へ進めない。
