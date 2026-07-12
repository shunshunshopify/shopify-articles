# SOLSTAR Shopify 記事制作ルール

このフォルダは、株式会社SOLSTAR（www.solstar.co.jp / Shopify Basicプラン）のブログ記事を
Claude Code で半自動制作するためのワークスペースです。
記事を作るときは必ずこのルールに従ってください。

> Codexで実行する場合は `AGENTS.md` を正本とする。`CLAUDE.md` と `AGENTS.md` が衝突する場合は `AGENTS.md` を優先する。

## 制作フロー（厳守）

1. ユーザーから「キーワード／テーマ」を受け取る
2. 競合・既存記事と被らない切り口で構成案（H2/H3の見出し一覧）を作る
3. 変化しやすい情報・出典・公式情報を確認する
4. `article-template.html` をベースに本文HTMLを生成する
5. 事実照合、日本語校閲、品質・法務レビュー、機械検証を行う
6. Google DriveへGoogle Doc下書きを保存し、readbackする
7. Shopify下書きは明示依頼時だけ、`articleCreate` mutation で **`isPublished: false`** として保存する
8. 公開はしない。公開ボタンは必ず人間が管理画面で押す。

> 重要: いかなる場合も記事を自動公開しないこと。生成物は常に非公開の下書き。

## 投稿先ブログ

| ブログ | handle | gid | 用途 |
|---|---|---|---|
| Shopify | shopify | gid://shopify/Blog/96499761374 | Shopify構築・費用・運用などのSEOコラム（メイン） |
| Marketing | marketing | gid://shopify/Blog/96528236766 | SEO・マーケティング・心理学系コラム |
| News | news | gid://shopify/Blog/93445423326 | お知らせ（現在未使用） |

テーマに応じて適切なブログを選ぶ。SEOコラムは原則 Shopify か Marketing。

## 文体・トーン

- です・ます調。専門用語は初心者にもわかるよう噛み砕いて説明する。
- 読者は「Shopifyでの構築・運用・SEOに関心のある事業者／担当者」。
- 記事冒頭は「最終更新日」「監修者情報」「導入文」「この記事でわかること」「目次」の順にする。
- 導入文は読者の悩みへの共感から入り、結論・本記事の切り口・読了メリットを300文字程度で示す。
- 各セクションは結論→理由→具体例の順。表・箇条書きを適度に使い読みやすく。
- 記事の終盤で、押し付けがましくない形で SOLSTAR の伴走型サポート等へ自然に誘導してよい。
- 著者名は「島袋隼」を使用。

### 翻訳・専門用語の扱い（重要）

英語の研究・海外コンテンツを参考にする際、機械的な直訳をしない。次の3点を必ず判断する。

1. **直訳が日本語として自然か** — 読み下したときに違和感がないか。原語のままや訳調になっていないか。
2. **訳語が日本語圏で浸透しているか** — Webや書籍で広く使われ、想定読者にも通じるか。業界内・学術界・一般読者で通用度に差があれば、本記事の想定読者に合わせる。
3. **どちらのトーンが適切か** — 「平易な日常語で伝える」場面と「正式名称＋丁寧な噛み砕きで定義を正確に示す」場面を使い分ける。一般読者向けの実用記事は前者寄り、研究紹介・法律・規格説明は後者寄り。

判断基準：

- **浸透している学術語**（例: アンカリング効果、プロスペクト理論、左端桁効果）→ 用語をそのまま使い、初出で1文の噛み砕きを添える。
- **浸透が浅い／直訳が不自然な学術語**（例: 「価格品質ヒューリスティック」→「高いものほど良いものだと感じる心理」）→ **平易な日本語に置き換える**か、噛み砕き表現を主・原語をカッコ書きで補助にする。
- **迷う用語は必ず `WebSearch` で調査**する：日本語の主流訳、検索ボリューム、解説記事の量、業界内での揺れを確認してから決める。
- **同一記事内で同じ概念に複数の訳語を混在させない**。最初に決めた訳語を最後まで貫く（一貫性）。

## 構成・HTML

- `article-template.html` の CSS / TOC / JSON-LD 枠は**改変しない**。本文だけ差し替える。
- 見出しは H2（大セクション）→ H3（小見出し）の階層。本文の主要H2には連番（1. 2. 3.）を付ける。
- H2「この記事でわかること」「よくある質問」「まとめ」「参考文献」は連番なしでよい。
- 目次(`.toc`)のアンカー(`#sec-x`)と本文見出しの `id` を必ず一致させる。
- 大セクション間は `<hr class="section-divider">` で区切る。
- FAQは「まとめ」の直前に3〜5問程度で設置する。
- 文字数の目安は 3,000〜6,000字程度（テーマにより調整）。

## SEO

- タイトル: 狙うキーワードを前半に含め、32文字前後。`【徹底解説】` のような訴求語を適度に。
- メタディスクリプション（記事の `summary` / JSON-LD の DESCRIPTION）: 120字前後で記事要約＋CTA。
- handle（URL）: 内容を表す半角英小文字ハイフン区切り（例: `shopify-cross-border-ec`）。
- タグ: 既存運用に合わせる（例: `SEO` `費用相場` `全般` `UIUX` `価格` `心理学`）。新設は最小限に。
- JSON-LD の画像URLは**記事に実在する画像のみ**記載する（存在しない情報の偽装は禁止）。

## 既存記事（重複回避・内部リンクの正本）

公開済み記事の正確な handle・タイトル・タグ・公開状態・カニバリ注意は **`data/published-articles.md`** に集約（Shopify Admin APIのライブ取得で更新する正本）。KW選定の重複チェック・設計の内部リンク候補選定・執筆の内部リンク挿入は、すべてこのファイルを参照する。記事を新規公開したら正本も更新する。

## エージェント構成（中央指揮パイプライン）

人間ライター原稿は、ユーザーが指定した個別Google Drive URLを正本として `AGENTS.md` の `review-human-draft` を実行する。レビュー済み版はフォルダID `1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee` に別ファイル保存・readbackしてから、Shopifyへ `isPublished:false` で投入する。原本は明示依頼がない限り上書きしない。

このワークスペースは、Claude Code（中央指揮）が専門サブエージェントを順番に呼び出して
1記事を仕上げる構成。通常フローではGoogle Drive下書き保存・readbackまで自動進行し、Shopify下書きは明示依頼時だけ実施する。人間は最終公開のみ行う。

```
①KW選定 → ③設計 → ③.5事実確認(pre-write) → ④執筆 → ④.1事実照合(post-write) → ④.2素材設計(必要時) → ④.5校閲 → ⑤品質 → ⑤.5法務 → ⑤.7機械検証 → Google Drive下書き保存・readback → （Shopify下書きを明示依頼した場合のみ）⑤.8公開前チェック → ⑥Shopify下書き
```

サブエージェント（`.claude/agents/`）:
| 工程 | agent | 役割 |
|---|---|---|
| ①KW選定 | `keyword-strategist` | GSC実データ＋3C分析で勝てるKWを選定（→ `drafts/keyword-candidates.md`） |
| ③設計 | `article-designer` | 上位記事をWeb調査しアウトライン・差別化方針を設計（→ `drafts/<handle>-brief.md`） |
| ③.5/④.1事実確認 | `fact-checker` | 執筆前の出典確認と執筆後の主張照合（→ `drafts/<handle>-sources.md`） |
| ④執筆 | `article-writer` | テンプレートに沿って本文HTML執筆・AI感排除（→ `drafts/<handle>.html`） |
| ④.2素材仕様 | `content-asset-planner` | 必要な記事だけ、図解・画像の実制作仕様とCWV注意点を整理（→ `drafts/<handle>-assets.md`） |
| ④.5校閲 | `japanese-editor` | AIが書いた本文を日本人が自然に読める文章へ編集（本文テキストのみ・構成/HTML/SEOは不変更） |
| ⑤品質 | `article-reviewer` | 総合95点・各観点90点ゲート。重大ブロッカーは点数によらず不合格 |
| ⑤.5法務 | `legal-reviewer` | 95点かつ高リスクゼロの公開前法務ゲート |
| ⑤.7機械検証 | `article-validator` | Drive保存前は構造・TOC・JSON-LD・リンクを検証し、Shopify前は残プレースホルダを含む完全検証を行う |
| Drive保存 | `drive-draft-saver` | Google Doc下書きの新規保存・URL/file ID/readback（→ `drafts/<handle>-drive.md`） |
| ⑤.8公開前チェック | `pre-publish-checker` | 残プレースホルダ・JSON-LD・FAQ位置・創作リスク等を最終確認 |
| ⑥公開 | `article-publisher` | Shopifyに `isPublished:false` の下書き保存 |

### 実行方法（自動化）
`~/shopify-articles/` から `claude` を起動し、スラッシュコマンド **`/new-article <キーワード>`** を実行すると全工程が自動で走る（キーワード省略時はKW選定から）。手動でサブエージェントを個別起動することも可能。

### 自動化レベル: Google Drive下書きまで自動
KW選定・設計・執筆・品質・Google Drive保存は自動進行する。Shopify下書きは明示依頼時のみ、公開は人間が実施する。
1. KW決定（引数 or `keyword-strategist`）。
2. `article-designer` で設計（承認停止はしない。要約提示のみ）。
3. `fact-checker (pre-write)` で公式情報・出典・変化しやすい情報を確認。
4. `article-writer` で執筆（`company-facts.md` の事実のみ使用。なければ創作せず `【要記入】` を残す）。
5. `fact-checker (post-write)` で完成HTMLの主張を出典と照合。
6. 素材設計が必要な場合だけ `content-asset-planner` を実行。
7. `japanese-editor` で本文テキストのみを最小限校閲。
8. `article-reviewer` で総合95点・各観点90点・重大ブロッカーゼロを確認（最大3周）。
9. `legal-reviewer` で95点・高リスクゼロを確認（最大3周）。
10. `article-validator --allow-draft-placeholders` 合格後、`drive-draft-saver` が指定Google DriveフォルダへGoogle Docとして保存・readbackする。
11. Shopify下書きを明示依頼された場合だけ、`drafts/<handle>-drive.md` が `passed` であることを確認し、通常モードの `article-validator` を再実行してから `pre-publish-checker` を実行する。
12. 合格後だけ `article-publisher` で Shopify に **isPublished:false の下書き** を作成する。
13. Drive URL・Shopify下書きURL（作成時のみ）・要確認点を報告。**公開は人間が手動で行う（自動公開は禁止）**。

### KWソース（`data/keyword-sources.md` 参照）
1. Ahrefsリスト（Drive: EC=1EnCG1a2NEozHJ0VQSjpXcZ14wttjUTfkYpP7mh1KxK8 / Shopify=1dV_Un3QSZHVn3YP3QQhno5qdwp5KFuzytXjCpzkk7Fk）— Volume×Difficulty×Intent
2. GSC自社データ（週次エクスポート）— 伸びしろ・取りこぼし
3. kolenda（価格心理/EC/ブランディングの原理）

### コンテンツ方針（著作権）
kolenda等の他社コンテンツは **翻訳転載しない**。原理・研究（事実）を抽出し、SOLSTAR独自の日本語オリジナル記事として執筆、出典を明記する。価格心理系は自社最強ページ「価格の心理学」と同系統＝勝ち筋。

> フェーズ2（未実装）: ②リサーチ(X/YouTube) / ⑦分析(Indexing/KPI) / アイキャッチのAI画像生成。

## ファイル

- `article-template.html` … 再利用テンプレート（CSS＋TOC＋JSON-LD骨格）
- `.claude/agents/` … 専門サブエージェント定義（keyword-strategist / article-designer / article-writer / japanese-editor / legal-reviewer / article-reviewer / article-publisher）
- `data/published-articles.md` … 公開済み記事の正本（handle・タグ・公開状態・カニバリ注意）。内部リンク・重複回避の参照元。Shopify Admin APIのライブ取得で更新
- `data/keyword-sources.md` … KWソース定義
- `scripts/gsc_fetch.py` … GSC APIから検索クエリを取得（サービスアカウント認証, `.venv` 使用）
- `.secrets/gsc-service-account.json` … GSCサービスアカウント鍵（Git管理外。ユーザーが配置）
- `data/` … GSC取得CSV等の保存先（CSVはGit管理外）
- `drafts/` … KW候補・設計ブリーフ(`*-brief.md`)・生成記事HTML(`*.html`)の保存先

### GSCデータ取得メモ（手動エクスポート方式）
- GSC APIは組織ポリシー（サービスアカウント鍵の作成禁止）で使えないため、**手動エクスポート方式**を採用。
- 手順: Search Console →「検索結果のパフォーマンス」→ 期間を過去3〜6か月 →「クエリ」タブ → エクスポート。
- 受け渡し: 「Googleスプレッドシート」にエクスポート → `keyword-strategist` がGoogle Drive連携で直接読む（推奨）。
  または CSV/Excel を `data/` に配置して読む。
- `scripts/gsc_fetch.py` と `.venv` はAPI方式用に残置（現状は未使用。組織ポリシーが緩和されたら利用可）。
