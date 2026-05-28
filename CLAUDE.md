# SOLSTAR Shopify 記事制作ルール

このフォルダは、株式会社SOLSTAR（www.solstar.co.jp / Shopify Basicプラン）のブログ記事を
Claude Code で半自動制作するためのワークスペースです。
記事を作るときは必ずこのルールに従ってください。

## 制作フロー（厳守）

1. ユーザーから「キーワード／テーマ」を受け取る
2. 競合・既存記事と被らない切り口で構成案（H2/H3の見出し一覧）を出し、**ユーザー承認を得る**
3. 承認後、`article-template.html` をベースに本文HTMLを生成する
4. Shopify Admin API の `articleCreate` mutation で**下書き（`isPublished: false`）として保存**する
5. 公開はしない。公開ボタンは必ず人間が管理画面で押す。

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
- 導入文は読者の悩みへの共感から入り、「本記事で何がわかるか」を示す（2〜4文）。
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
- 見出しは H2（大セクション）→ H3（小見出し）の階層。H2には連番（1. 2. 3.）を付ける。
- 目次(`.toc`)のアンカー(`#sec-x`)と本文見出しの `id` を必ず一致させる。
- 大セクション間は `<hr class="section-divider">` で区切る。
- 文字数の目安は 3,000〜6,000字程度（テーマにより調整）。

## SEO

- タイトル: 狙うキーワードを前半に含め、32文字前後。`【徹底解説】` のような訴求語を適度に。
- メタディスクリプション（記事の `summary` / JSON-LD の DESCRIPTION）: 120字前後で記事要約＋CTA。
- handle（URL）: 内容を表す半角英小文字ハイフン区切り（例: `shopify-cross-border-ec`）。
- タグ: 既存運用に合わせる（例: `SEO` `費用相場` `全般` `UIUX` `価格` `心理学`）。新設は最小限に。
- JSON-LD の画像URLは**記事に実在する画像のみ**記載する（存在しない情報の偽装は禁止）。

## 既存記事（重複回避の参考）

- Shopifyのメリットとデメリット / Shopify構築費用 / フリーランス依頼の費用相場
- JSON-LDとは？SEO完全ガイド / 価格の心理学

## エージェント構成（中央指揮パイプライン）

このワークスペースは、Claude Code（中央指揮）が専門サブエージェントを順番に呼び出して
1記事を仕上げる構成。人間は意思決定（テーマ承認・構成承認・最終公開）のみ行う。

```
①KW選定(GSC×3C) → ③設計 → ④執筆 → ⑤品質(95点ゲート) → ⑥公開(Shopify下書き)
```

サブエージェント（`.claude/agents/`）:
| 工程 | agent | 役割 |
|---|---|---|
| ①KW選定 | `keyword-strategist` | GSC実データ＋3C分析で勝てるKWを選定（→ `drafts/keyword-candidates.md`） |
| ③設計 | `article-designer` | 上位記事をWeb調査しアウトライン・差別化方針を設計（→ `drafts/<handle>-brief.md`） |
| ④執筆 | `article-writer` | テンプレートに沿って本文HTML執筆・AI感排除（→ `drafts/<handle>.html`） |
| ⑤品質 | `article-reviewer` | 95点ゲート。SEO/読者・E-E-A-T/AI感・独自性 の3観点で審査 |
| ⑥公開 | `article-publisher` | Shopifyに `isPublished:false` の下書き保存 |

### 実行方法（自動化）
`~/shopify-articles/` から `claude` を起動し、スラッシュコマンド **`/new-article <キーワード>`** を実行すると全工程が自動で走る（キーワード省略時はKW選定から）。手動でサブエージェントを個別起動することも可能。

### 自動化レベル: 公開のみ手動
人間チェックは **最終公開の1点のみ**。KW選定・設計・執筆・品質はすべて自動進行する。
1. KW決定（引数 or `keyword-strategist`）。
2. `article-designer` で設計（承認停止はしない。要約提示のみ）。
3. `article-writer` で執筆（`company-facts.md` の事実のみ使用）。
4. `article-reviewer` を **3観点で並行起動** → 平均 **95点未満なら `article-writer` に差し戻し改稿** → 合格まで繰り返す（最大3周）。3周未達なら人間に報告して停止。
5. 合格後 `article-publisher` で Shopify に **isPublished:false の下書き** 作成。
6. 下書きURL・要確認点を報告。**公開は人間が手動で行う（自動公開は禁止）**。

### KWソース（`data/keyword-sources.md` 参照）
1. Ahrefsリスト（Drive: EC=1EnCG1a2NEozHJ0VQSjpXcZ14wttjUTfkYpP7mh1KxK8 / Shopify=1dV_Un3QSZHVn3YP3QQhno5qdwp5KFuzytXjCpzkk7Fk）— Volume×Difficulty×Intent
2. GSC自社データ（週次エクスポート）— 伸びしろ・取りこぼし
3. kolenda（価格心理/EC/ブランディングの原理）

### コンテンツ方針（著作権）
kolenda等の他社コンテンツは **翻訳転載しない**。原理・研究（事実）を抽出し、SOLSTAR独自の日本語オリジナル記事として執筆、出典を明記する。価格心理系は自社最強ページ「価格の心理学」と同系統＝勝ち筋。

> フェーズ2（未実装）: ②リサーチ(X/YouTube) / ⑦分析(Indexing/KPI) / アイキャッチのAI画像生成。

## ファイル

- `article-template.html` … 再利用テンプレート（CSS＋TOC＋JSON-LD骨格）
- `.claude/agents/` … 専門サブエージェント定義（keyword-strategist / article-designer / article-writer / article-reviewer / article-publisher）
- `scripts/gsc_fetch.py` … GSC APIから検索クエリを取得（サービスアカウント認証, `.venv` 使用）
- `.secrets/gsc-service-account.json` … GSCサービスアカウント鍵（Git管理外。ユーザーが配置）
- `data/` … GSC取得CSVの保存先（Git管理外）
- `drafts/` … KW候補・設計ブリーフ(`*-brief.md`)・生成記事HTML(`*.html`)の保存先

### GSCデータ取得メモ（手動エクスポート方式）
- GSC APIは組織ポリシー（サービスアカウント鍵の作成禁止）で使えないため、**手動エクスポート方式**を採用。
- 手順: Search Console →「検索結果のパフォーマンス」→ 期間を過去3〜6か月 →「クエリ」タブ → エクスポート。
- 受け渡し: 「Googleスプレッドシート」にエクスポート → `keyword-strategist` がGoogle Drive連携で直接読む（推奨）。
  または CSV/Excel を `data/` に配置して読む。
- `scripts/gsc_fetch.py` と `.venv` はAPI方式用に残置（現状は未使用。組織ポリシーが緩和されたら利用可）。
