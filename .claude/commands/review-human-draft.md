---
description: 指定Google Drive記事をレビューし、レビュー済み版をDrive保存後にShopify下書きへ投入する
argument-hint: <Google DriveまたはGoogle Docsの個別記事URL>
---

`AGENTS.md` の `review-human-draft` ワークフローを実行する。

対象記事URL: $ARGUMENTS

- URLが空の場合、フォルダ内の記事を推測で選ばず停止する。
- 対象ファイルIDを固定し、原本を勝手に上書きしない。
- レビュー済み版をフォルダID `1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee` に別ファイル保存し、readbackする。
- 品質・法務・機械検証・公開前チェックをすべて通過した場合だけShopifyへ `isPublished:false` で下書き投入する。
- Google Drive URLとShopify管理URLを報告する。公開は行わない。
