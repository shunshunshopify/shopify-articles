---
description: KWから記事を全自動制作しGoogle Drive下書きまで保存する（Shopify下書きは明示依頼時のみ）
argument-hint: [キーワード（省略可：省略時はKW選定から）]
---

あなたはSOLSTARのSEO記事制作パイプラインの中央指揮役です。以下を順に実行し、Google Driveの下書き保存・readbackまで自動で進めてください。Shopify下書きは、ユーザーが明示的に依頼した場合だけ作成します。**公開は絶対にしない**（人間が管理画面で行う）。`AGENTS.md` のルールを全工程で遵守すること。

対象キーワード: $ARGUMENTS

## 実行手順

### 0. KW決定
- 引数でキーワードが指定されていれば、それを使う。
- 指定がなければ `keyword-strategist` サブエージェントを起動し、Ahrefsリスト×GSC×3Cで最有力KWを1つ自動選定する（候補と選定理由を簡潔に提示してから進む）。

### 1. 設計（③）
- `article-designer` サブエージェントを起動し、設計ブリーフ `drafts/<handle>-brief.md` を作らせる。
- ※今回は「公開のみ手動」方針のため、設計段階では停止しない。設計内容は要約だけ提示して次へ進む。
- 価格心理・EC・ブランディング系テーマなら、kolendaガイドを参考資料に（翻訳転載はせず原理を抽出・出典明記）。

### 2. 執筆（④）
- `fact-checker` を `pre-write` モードで起動し、公式情報・出典・変化しやすい情報を確認して `drafts/<handle>-sources.md` を作らせる。
- `article-writer` サブエージェントを起動。`article-template.html`・`company-facts.md`・ブリーフ・事実確認メモに沿って本文HTMLを `drafts/<handle>.html` に書かせる。
- `fact-checker` を `post-write` モードで再起動し、完成HTMLの主張・数値・比較・引用を出典メモと照合させる。
- SOLSTAR固有の事実は `company-facts.md` の範囲のみ。無い事実は創作せず `【要記入：…】` を残す。

### 2.5 素材・リンク提案
- 図解・画像などの素材設計が必要な記事だけ `content-asset-planner` を起動し、実制作仕様・挿入位置・参考文献・CWV注意点を `drafts/<handle>-assets.md` に整理させる。
- 未確認URLや未作成画像を本文に確定情報として混ぜない。

### 3. 校閲（④.5・日本語ネイティブ編集）
- `japanese-editor` サブエージェントを起動し、`drafts/<handle>.html` の **本文テキストのみ** を日本人が自然に読める文章へ編集させる。
- 構成・HTML・目次・JSON-LD・SEOキーワード・出典は変更しない（AI感・翻訳調の排除が目的）。

### 4. 品質ゲート（⑤・95点）
- `article-reviewer` を **1回起動して4観点をまとめて採点**させる（SEO / 読者・E-E-A-T / AI感・独自性 / UX・可読性）。結果は `drafts/<handle>-review.md` に保存させる。
- **総合95点未満、いずれかの観点が90点未満、または重大ブロッカーが1件でもあれば**、指摘を統合して `article-writer` に差し戻す。必要に応じ `fact-checker (post-write)`、`content-asset-planner`、`japanese-editor` を再実行する（最大3周）。
- 3周しても未達なら、残課題を添えて人間に報告して停止（公開には進まない）。
- 品質ゲートを通過してから、次の法務ゲート（公開前の最終）へ進む。

### 5. 法務ゲート（⑤.5・95点／公開前の最終）
- `legal-reviewer` サブエージェントを起動し、`drafts/<handle>.html` を日本の広告・表示関連法（景品表示法・ステマ規制・薬機法・特定商取引法・著作権法など）の観点で採点させる。
- **95点未満、または高リスク表現が1つでも残る場合は、指摘を `article-writer` に差し戻してRewrite**（表現の安全化に限定し、構成・SEOキーワード・論旨は変えない。表現変更で本文が変わるため必要に応じ `content-asset-planner` と `japanese-editor` を再実行）→ `legal-reviewer` で再審査。**95点以上になるまで繰り返す**（最大3周）。
- 3周しても未達なら、残った法的リスクを添えて人間に報告して停止（公開には進まない）。
- 法務ゲートを通過してから、次の公開前チェックへ進む。

### 5.5 Google Drive下書き保存
- `python3 scripts/article_validator.py --allow-draft-placeholders drafts/<handle>.html` を実行する。構造、TOC、JSON-LD、CSS、内部リンクの検証に失敗した場合は修正して再検証し、合格するまで次へ進まない。
- `drive-draft-saver` サブエージェントを `new_article` モードで起動し、合格記事をフォルダID `1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee` へ `[下書き] <記事タイトル>` のGoogle Docとして保存・readbackさせる。
- `drafts/<handle>-drive.md` が `passed` でない場合は、Drive URLと未解決事項を報告して停止する。Shopifyへは進まない。

### 6. Shopify下書き作成（明示依頼時のみ）
- ユーザーがShopify下書き作成を明示的に依頼した場合だけ、`drafts/<handle>-drive.md` が `passed` であることを確認し、`python3 scripts/article_validator.py drafts/<handle>.html` を通常モードで再実行する。合格後に `pre-publish-checker` サブエージェントを起動し、残プレースホルダ・JSON-LD・FAQ位置・数字タイトル整合・創作リスク・未確認リンクを確認させる。
- `pre-publish-checker` が不合格なら `article-publisher` へ進まず、修正点を報告して停止する。
- 合格を維持したら `article-publisher` サブエージェントを起動し、Shopifyに **isPublished:false の下書き** として作成。
- JSON-LDのプレースホルダ（HEADLINE/DESCRIPTION/PAGE_URL/DATE_PUBLISHED/DATE_MODIFIED/BLOG_NAME/BLOG_URL）を確定値に置換してから投稿（置換の最終責任は publisher。writer が先に埋めた HEADLINE/DESCRIPTION もブリーフの確定値で上書き確認する）。

### 7. 報告
- 最終の品質スコア・法務スコア、Google Drive URL、Shopify下書きを作成した場合だけそのadmin URL、`【要記入】`が残っていればその一覧、公開前に人間が確認すべき点を報告する。
- **公開はしていないこと**を明記し、人間に最終公開を委ねる。

## 重要な原則
- 公開は人間のみ。自動公開は禁止。
- 事実の創作禁止（company-facts.md の範囲＋一般論のみ）。
- kolenda等の他社コンテンツは翻訳転載しない（参考にしてオリジナル執筆＋出典明記）。
- このコマンドは `~/shopify-articles/` から実行する前提（サブエージェントが名前で解決される）。
