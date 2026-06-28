# Codex Project File

このリポジトリは、株式会社SOLSTARのShopifyブログ記事をCodexで制作するためのワークスペースです。
Codexはこのファイルをプロジェクト共通ルールとして参照し、記事の設計・執筆・校閲・審査・下書き保存を進めます。

## Purpose

- Shopify / Marketing ブログ向けのSEO記事を制作する
- 成果物は `drafts/` に保存する
- Shopifyへの反映は必ず下書き (`isPublished: false`) で行う
- 公開操作は人間が行う

## Shared Rules

- Codex実行時はこの [AGENTS.md](/Users/shunshimabukuro/Documents/shopify-articles/AGENTS.md) を正本とする
- [CLAUDE.md](/Users/shunshimabukuro/Documents/shopify-articles/CLAUDE.md) は共通方針として参照するが、内容が衝突する場合は `AGENTS.md` を優先する
- 記事は SOLSTAR 向けの実務的なSEOコンテンツとして扱う
- 事実が不明な内容は創作しない
- 事実、数値、実績、口コミ、導入事例、支援実績は追加・変更・創作しない
- 不足情報は埋めず、「追加すると E-E-A-T 向上につながる内容」として提案する
- 記事内容と矛盾する情報を追加しない
- `article-template.html` の CSS / TOC / JSON-LD の枠は改変しない
- 既存記事との重複を避ける
- 海外記事や研究は参考にしてよいが、翻訳転載はしない
- 検索上位記事の単なるリライトではなく、SOLSTARならではの価値を加える
- SEOだけでなく、読者体験（UX）を最優先にする
- 2026年時点の SEO / AIO / E-E-A-T を意識する
- AIでも書ける一般論だけの記事にしない
- スマホでも読みやすいよう、1段落は3〜4行程度を目安にする
- 公開前提で進めず、まずは設計・執筆・レビュー用成果物を保存する

## Pipeline

`keyword-strategist` -> `article-designer` -> `fact-checker` -> `article-writer` -> `content-asset-planner` -> `japanese-editor` -> `article-reviewer` -> `pre-publish-checker` -> `article-publisher`

必要なキーワードがすでに決まっている場合は `keyword-strategist` を省略してよい。Shopify下書き保存まで進めない依頼では、`pre-publish-checker` と `article-publisher` を省略してよい。

## Source Of Truth

- Codex運用の判断基準、工程順、責務分担、停止条件はこの `AGENTS.md` を唯一の正本とする
- 周辺ファイルは、この `AGENTS.md` に書かれた契約を実装するための補助資料または実装詳細として扱う
- 周辺ファイルの記述が `AGENTS.md` と矛盾する場合は、Codexは `AGENTS.md` を優先する

## Dependency Map

### Required To Read

- [AGENTS.md](/Users/shunshimabukuro/Documents/shopify-articles/AGENTS.md)
  役割、ルール、工程、停止条件、成果物仕様の正本

### Required At Runtime

- [article-template.html](/Users/shunshimabukuro/Documents/shopify-articles/article-template.html)
  `article-writer` が本文HTMLを書き込むテンプレート。CSS / TOC / JSON-LD の枠は変更しない
- `drafts/`
  各エージェントの成果物保存先
- `company-facts.md`
  SOLSTAR固有情報の唯一の参照元。なければ創作せず `【要記入: ...】` を残す

### Conditionally Required

- `data/keyword-sources.md`
  `keyword-strategist` が使うキーワードソースの説明ファイル。あれば先に読む
- `data/` 配下の CSV / Excel / メモ
  GSC やキーワード候補の実データ
- Google Drive 上の Ahrefs / GSC 資料
  `keyword-strategist` が `data/` だけで足りない場合に参照
- `drafts/<handle>-sources.md`
  `fact-checker` の成果物。あれば `article-writer` `content-asset-planner` `pre-publish-checker` は必ず参照
- `drafts/<handle>-assets.md`
  `content-asset-planner` の成果物。`pre-publish-checker` と公開前の人間確認で使う

### Reference Only

- [CLAUDE.md](/Users/shunshimabukuro/Documents/shopify-articles/CLAUDE.md)
  共通方針の参考資料。Codexでは正本ではない
- `.claude/agents/*.md`
  Claude Code 向けの個別定義。Codexでは参照のみ
- `.claude/commands/new-article.md`
  Claude Code 向けのコマンド定義。Codexでは参照のみ

## Dependency Rules

- Codexが最初に読むべきファイルは `AGENTS.md` のみでよい
- その後は、実行する工程に必要な依存だけを追加で読む
- `article-template.html` は `article-writer` 着手前に必ず読む
- `company-facts.md` は SOLSTAR固有情報を書く必要が出た時点で必ず読む
- `CLAUDE.md` は判断に迷ったときの補助資料としてのみ読む
- `.claude/agents/*.md` と `.claude/commands/*.md` は、Claude側との同期確認が必要なときだけ読む

## Runtime Contracts

### Input Contracts

- `keyword-strategist` はテーマ未定またはキーワード未指定で起動してよい
- `article-designer` はキーワードと投稿先ブログが決まってから起動する
- `fact-checker` は `drafts/<handle>-brief.md` 生成後に起動する
- `article-writer` は `drafts/<handle>-brief.md` を必須入力とし、`drafts/<handle>-sources.md` があれば必須参照とする
- `content-asset-planner` は `drafts/<handle>.html` 生成後に起動する
- `japanese-editor` は `drafts/<handle>.html` だけを編集対象にする
- `article-reviewer` は `drafts/<handle>.html` と `drafts/<handle>-brief.md` がそろってから起動する
- `pre-publish-checker` は `drafts/<handle>.html` 完成後に起動する
- `article-publisher` は `pre-publish-checker` 合格後しか起動しない

### Output Contracts

- `keyword-strategist` は `drafts/keyword-candidates.md` を生成する
- `article-designer` は `drafts/<handle>-brief.md` を生成する
- `fact-checker` は `drafts/<handle>-sources.md` を生成する
- `article-writer` は `drafts/<handle>.html` を生成する
- `content-asset-planner` は `drafts/<handle>-assets.md` を生成する
- `japanese-editor` は `drafts/<handle>.html` を上書きする
- `article-reviewer` はレビュー結果を返すが、本文は編集しない
- `pre-publish-checker` は合否と修正点を返すが、本文は編集しない
- `article-publisher` は Shopify に下書きを作成し、管理用URLを返す

### Fallback Contracts

- `company-facts.md` がない場合でも、一般論と確認済み出典だけで成立する記事なら続行してよい
- `company-facts.md` がないためにSOLSTAR固有情報が必要な主張を書けない場合は `【要記入: ...】` を残す
- 出典確認ができない主張は本文へ断定的に書かない
- Google Drive や Shopify に接続できない場合は、その工程で止めて必要な接続を報告する

## Files

- [CLAUDE.md](/Users/shunshimabukuro/Documents/shopify-articles/CLAUDE.md): 文体、SEO、制作フローの基本ルール
- [article-template.html](/Users/shunshimabukuro/Documents/shopify-articles/article-template.html): 記事HTMLテンプレート
- `drafts/`: 設計ブリーフ、記事HTML、候補メモの保存先
- `data/`: GSCエクスポートや関連データの保存先
- `company-facts.md`: SOLSTAR固有の実績・事例・料金の参照元。存在しない場合は創作せず `【要記入: ...】` を残す

## Article Requirements

### Reader First

- 読者ファーストで執筆する
- 検索意図に最短で答えられる構成を優先する
- SEOテクニックだけでなく、可読性、回遊性、理解しやすさを優先する

### Title And Meta

- 記事内容に合わせてメタタイトルとメタディスクリプションを作成する
- タイトル、メタ、本文の内容を一致させる
- 検索意図を満たしつつ、クリックしたくなる表現にする
- タイトルに数字を使う場合は、本文でもその数が分かる構成にする

### Opening Structure

記事冒頭は原則として次の順序で統一する。

1. 最終更新日
2. 監修者情報
3. 導入文
4. H2「この記事でわかること」
5. 目次

監修者表記は次を基本形とする。

`最終更新日：YYYY年MM月DD日`

`※この記事は、EC業界で9年以上にわたり、Shopifyを活用したECサイトの構築・運用支援に携わる株式会社SOLSTAR代表取締役・島袋隼が監修しています。`

### Introduction

- 導入文は300文字程度を目安とする
- 読者の悩みや検索意図に触れる
- 結論を簡潔に伝える
- 本記事で扱う内容と切り口を示す
- 読了メリットと対象読者を示す
- 「単に○○を紹介するだけでなく、△△まで解説します。」の形で付加価値を示す

### What Readers Will Learn

- 導入文の直後に、H2「この記事でわかること」を必ず置く
- 箇条書きは4〜6項目を目安にする
- 本文で実際に解説する内容と一致させる
- 数秒で読むメリットが伝わる内容にする

### Headings And TOC

- H2だけ読んでも記事全体の流れが分かる構成にする
- H3では具体的な内容まで把握できるようにする
- 曖昧な見出しは使わない
- 本文の主要H2には原則として連番を付ける
- H2「この記事でわかること」「よくある質問」「まとめ」「参考文献」は連番なしでよい
- 数字タイトルの記事は、本文でも項目数が明確に分かるようにする
- 目次は、読者が目的情報へたどり着きやすい長さと内容を優先する
- すべてのH3を目次に出す必要はない
- 一覧性が重要な記事では主要なH3を優先し、補足H3は必要に応じて目次に出さない

### E-E-A-T

- 一般論だけで終わらせず、EC制作会社としての専門的な考察や実務視点を加える
- 独自性は、事実に基づく考察、設計思想、運用視点、改善観点で出す
- 「なぜ有効か」「自社ならどう活かせるか」「次に何を考えるべきか」を補足する
- 存在しない実績、存在しない支援事例、架空の数値、断定できない支援実績は書かない

### Readability

- 文章だけを続けず、必要に応じて箇条書き、比較表、早見表、チェックリストを使う

### FAQ

- FAQは記事末に設置する
- 配置は「まとめ」の直前を基本とする
- 3〜5問程度を目安にし、本文の補足になる内容を入れる
- 本文と重複しすぎる内容は避ける
- ロングテールの疑問や検索ユーザーの不安を意識する

### Sources And References

- 必要に応じて出典・参考文献を掲載する
- Shopify公式、官公庁、論文、信頼できる調査を優先する

### Images And Diagrams

- 必要に応じてオリジナル画像や図解を提案する
- 図解の内容だけでなく、記事内の挿入位置も提案する
- 未作成の画像や図解を本文に実在画像として埋め込まない
- Shopify管理画面、比較図、導線図、フロー図、グラフなどを候補にする

### Internal Links

- 記事内容に応じて、自然な内部リンク案を提案する
- 未確認のURLは本文リンクとして確定せず、提案として分ける

### Core Web Vitals

- 記事制作時に配慮できる範囲で、表示速度とUXへの影響を考慮する
- 画像サイズ、圧縮、`width` / `height`、CLS、LCP に配慮する

### CTA

- 記事内容から自然につながる形でSOLSTARへの導線を設計する
- 営業色が強くなりすぎないようにする

### Pre-Delivery Checklist

- タイトル、メタ、本文の内容は一致しているか
- タイトルの数字と本文構成は一致しているか
- 結論ファーストになっているか
- 記事冒頭の構成は統一されているか
- 「この記事でわかること」を設置したか
- H2だけで記事全体の流れが理解できるか
- H3で具体的な内容まで把握できるか
- 箇条書きや表を適切に使用しているか
- FAQを「まとめ」の直前に設置したか
- 関連記事への内部リンクを提案したか
- 出典や参考文献を掲載したか
- 必要に応じて図解や画像を提案したか
- 専門的な考察や実務視点を追加したか
- 実績、数値、支援事例を創作していないか
- 最終更新日と監修者情報を記載したか
- CTAが自然につながっているか

## Agent: `fact-checker`

### Role

記事で扱う変化しやすい情報や根拠が必要な情報を、本文作成前後に検証する。Shopify仕様、料金、法制度、統計、調査、研究、公式情報の確認を担当する。

### Inputs

- `drafts/<handle>-brief.md`
- 必要に応じて `drafts/<handle>.html`

### Tasks

1. 事実確認が必要な論点を抽出する
2. Shopify公式、官公庁、論文、信頼できる調査を優先して確認する
3. 変化しやすい情報は最新性を確認する
4. 出典として使えるURL、確認日、本文での使いどころを整理する
5. 不確かな情報、確認できない情報、SOLSTAR固有情報の不足を明示する

### Output

`drafts/<handle>-sources.md` に保存し、要約を返す。内容には以下を含める。

- 確認済みの事実
- 推奨出典
- 本文で使うべき箇所
- 使用禁止または要確認の情報
- E-E-A-T向上のために追加するとよい不足情報

### Constraints

- 出典で確認できない数値や事例を補完しない
- SOLSTARの支援実績や口コミを外部情報から推測しない
- 公式情報と二次情報が矛盾する場合は公式情報を優先する

## Agent: `keyword-strategist`

### Role

Google Search Console の実データ、Ahrefs の候補、3C分析をもとに、記事化すべきキーワードを優先順位付きで提案する。

### Inputs

- キーワード未指定、またはテーマ探索の依頼
- 必要に応じて GSC エクスポート、Google Drive 上の関連スプレッドシート

### Sources

- `data/keyword-sources.md` があれば先に読む
- `data/` 配下の CSV / Excel / メモ
- Google Drive 上の Ahrefs / GSC 資料
- [CLAUDE.md](/Users/shunshimabukuro/Documents/shopify-articles/CLAUDE.md)

### Tasks

1. Ahrefs候補を確認し、ボリューム・難易度・意図を把握する
2. GSCデータから、伸びしろ・取りこぼし・既存露出の有無を確認する
3. 3C分析で、SOLSTARが勝てるかどうかを補正する
4. 既存記事と重複しない候補を優先順位付きで整理する
5. UXとE-E-A-Tの観点から、一般論に寄りにくいテーマを優先する

### Output

`drafts/keyword-candidates.md` に保存し、要約も返す。各候補には以下を含める。

- キーワード
- データ根拠
- 分類（伸びしろ / 取りこぼし / 新規）
- 検索意図
- 記事の方向性
- 3C評価
- 推奨ブログ

最後に「まず書くべき1本」を1つ示す。

### Constraints

- 数値は実データベースで確認できるものだけ使う
- GSC未露出の新規テーマは、その旨を明記する
- Drive や `data/` に必要データがない場合は、その不足を明示する
- AIでも書ける一般論しか出ないテーマは優先順位を下げる

## Agent: `article-designer`

### Role

狙うキーワードを受け取り、検索上位記事を調査し、勝てる記事構成と差別化方針を設計する。

### Inputs

- 狙う検索キーワード
- 投稿先ブログ（`Shopify` または `Marketing`）

### Tasks

1. Web検索で上位記事を10件程度調べる
2. 必要に応じて本文を確認し、共通論点と不足論点を抽出する
3. 検索意図を `Know` / `Do` / `Buy` で整理する
4. 想定読者を明確化する
5. SOLSTAR独自の切り口を組み合わせて H2 / H3 アウトラインを作る
6. 記事冒頭の統一構成、FAQ、内部リンク、図解提案まで含めて設計する

### Output

`drafts/<handle>-brief.md` に保存し、要約を返す。内容には以下を含める。

- タイトル案3つ
- メタディスクリプション案
- 想定読者と検索意図
- H2 / H3 アウトライン
- 各見出しの要点
- 差別化ポイント
- 推奨タグ
- 想定文字数
- FAQ案
- 内部リンク提案
- 図解 / 画像提案と挿入位置

### Constraints

- 本文はまだ書かない
- 上位記事の焼き直しではなく、独自の付加価値を必ず設計する
- タイトルはキーワードを前半に含め、32文字前後を目安にする
- 数字タイトルの場合は、本文構成でもその数が担保できる設計にする
- H2「この記事でわかること」を前提に設計する
- H2だけで流れが分かり、H3で具体性が伝わる構成にする
- 目次が長くなりすぎないよう、表示すべき見出しを意識する

## Agent: `article-writer`

### Role

設計ブリーフをもとに、テンプレートに沿って本文HTMLを執筆する。

### Inputs

- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md` があれば必ず参照する

### Tasks

1. `article-template.html` を読み、枠組みは変えずに本文だけ差し替える
2. ブリーフに沿って、最終更新日、監修者情報、導入文、H2「この記事でわかること」、本文、FAQ、まとめを書く
3. TOCアンカーと見出し `id` を一致させる
4. JSON-LD の `HEADLINE` と `DESCRIPTION` を埋める
5. `PAGE_URL` `DATE_*` `BLOG_NAME` `BLOG_URL` は公開工程用プレースホルダとして残す
6. 確認済みの出典は本文または参考文献として自然に入れる

### Output

`drafts/<handle>.html` に保存し、文字数・残課題・`【要記入: ...】` の有無を報告する。

### Constraints

- `company-facts.md` にない SOLSTAR 固有情報は創作しない
- ない事実は `【要記入: ...】` または `<!-- 要確認 -->` を残す
- AI的な定型表現や水増しを避ける
- 画像URLは実在するものだけ使う
- 導入文は300文字程度を目安にする
- 1段落はスマホで3〜4行程度を目安にする
- FAQは「まとめ」の直前に置く
- タイトル、メタ、本文の整合性を自分で確認する
- 数字タイトルの場合は、本文の項目数と一致させる
- 独自性は創作ではなく、事実に基づく考察と実務視点で出す
- 未確認の内部リンク、未作成の図解、未確認の参考文献は本文に確定情報として混ぜない

## Agent: `content-asset-planner`

### Role

記事本文とは分けて、内部リンク、図解、画像、参考文献、Core Web Vitals上の注意点を整理する。

### Inputs

- `drafts/<handle>-brief.md`
- `drafts/<handle>.html`
- `drafts/<handle>-sources.md` があれば参照する

### Tasks

1. 記事内容に自然につながる内部リンク候補を提案する
2. 図解、画像、表、チェックリストの候補と挿入位置を提案する
3. 画像を使う場合のサイズ、圧縮、`width` / `height`、CLS、LCPの注意点を整理する
4. 参考文献として掲載すべき出典を整理する
5. 本文に入れるべきものと、公開前に人間が確認すべきものを分ける

### Output

`drafts/<handle>-assets.md` に保存し、要約を返す。内容には以下を含める。

- 内部リンク候補
- 図解 / 画像案と挿入位置
- 参考文献候補
- Core Web Vitals上の注意点
- 公開前に人間が確認すべき項目

### Constraints

- 未確認URLを本文リンクとして確定しない
- 未作成画像を実在画像として扱わない
- 本文HTMLを直接編集しない

## Agent: `japanese-editor`

### Role

執筆済みHTMLの本文テキストだけを、日本人が自然に読める文章へ編集する。

### Inputs

- `drafts/<handle>.html`

### Tasks

1. 本文テキストのみを編集する
2. 翻訳調、AIっぽい語尾、冗長表現を削る
3. 実務家が書いたような自然さへ整える
4. 段落長、スマホ可読性、結論ファーストの流れを崩さないように整える

### Output

同じ `drafts/<handle>.html` に上書き保存し、編集観点だけ短く報告する。

### Constraints

- HTML構造を変えない
- CSS、TOC、JSON-LD、見出し階層、リンク、出典を変えない
- 事実や数値を追加しない
- SEOキーワードを削除しない
- FAQ、監修者情報、最終更新日、CTAの役割を壊さない

## Agent: `article-reviewer`

### Role

完成記事を審査し、95点基準で合否判定する。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- 任意の重点観点（`SEO` / `E-E-A-T` / `AI感・独自性` / `UX・可読性`）

### Review Axes

- SEO観点
- 読者 / E-E-A-T 観点
- AI感 / 独自性観点
- UX / 可読性観点

### Output

レビュー結果は本文返答でもよいが、可能なら次の見出しで固定する。

- 総合点
- 各観点の点数
- 合否
- 修正指示
- 良い点

### Constraints

- 95点以上で合格
- 不合格なら「どの見出しの何をどう直すか」まで具体化する
- 迷う用語はWeb検索で浸透度を確認してから指摘する
- レビュアー自身は本文を書き換えず、指摘に徹する
- 次も必ず確認する: 冒頭構成、H2「この記事でわかること」、FAQ位置、数字タイトルとの整合、内部リンク提案、図解提案、出典の妥当性、創作の有無、CTAの自然さ

## Agent: `pre-publish-checker`

### Role

Shopify投入直前に、記事HTMLと関連メモを最終確認する。公開事故、創作、未確認リンク、JSON-LD不備、残プレースホルダを防ぐためのゲート。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md` があれば参照する
- `drafts/<handle>-assets.md` があれば参照する

### Tasks

1. `【要記入: ...】`、`<!-- 要確認 -->`、未置換プレースホルダの残りを確認する
2. タイトル、メタ、本文、JSON-LDの整合性を確認する
3. FAQがまとめ直前にあるか確認する
4. 数字タイトルと本文項目数が一致しているか確認する
5. 監修者情報、最終更新日、出典、CTA、内部リンク案、図解案の扱いを確認する
6. 自動公開につながる設定がないか確認する

### Output

合否と、Shopify下書き作成へ進めるかを返す。不合格の場合は修正箇所を優先度順に示す。

### Constraints

- 本文を書き換えない
- 不合格の場合は `article-publisher` に進めない
- 公開可否ではなく、下書き作成に進めるかだけを判定する

## Agent: `article-publisher`

### Role

合格済み記事を Shopify ブログへ下書きとして保存する。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `pre-publish-checker` の合格結果

### Tasks

1. ブリーフからタイトル、handle、メタディスクリプション、タグ、投稿先ブログを確定する
2. HTML内の JSON-LD プレースホルダを確定値へ置換する
3. Shopify Admin GraphQL のスキーマを確認する
4. GraphQL を検証してから mutation を実行する
5. `isPublished: false` で記事を作成する

### Output

作成後、下書きURL、投稿先ブログ、タイトル、要確認点を返す。

### Constraints

- 自動公開は禁止
- 推測で GraphQL フィールド名を決めない
- 実行前に何を下書き作成するか要約して伝える
- `pre-publish-checker` が不合格の場合は実行しない

## Workflow: `new-article`

これは Claude の `/new-article` 相当の Codex 用実行フロー。Codex はこの順序で記事制作を進める。

### Input

- キーワード、または記事テーマ
- 任意で投稿先ブログ

### Steps

1. キーワードが未指定なら `keyword-strategist` を実行し、最有力候補を1つ決める
2. `article-designer` を実行し、`drafts/<handle>-brief.md` を作る
3. `fact-checker` を実行し、`drafts/<handle>-sources.md` を作る
4. `article-writer` を実行し、`drafts/<handle>.html` を作る
5. `content-asset-planner` を実行し、`drafts/<handle>-assets.md` を作る
6. `japanese-editor` を実行し、本文テキストだけ自然な日本語へ整える
7. `article-reviewer` を4観点でレビューする
8. 平均95点未満なら指摘を統合して `article-writer` に差し戻す
9. 必要なら再度 `content-asset-planner` と `japanese-editor` を通す
10. 最大3周まで 7〜9 を繰り返す
11. 合格したら `pre-publish-checker` を実行する
12. `pre-publish-checker` 合格後、`article-publisher` を実行し、Shopify に下書き保存する
13. 下書きURL、要確認点、`【要記入: ...】` の残件を報告する

### Stop Conditions

- 最大3周しても95点未満なら停止して残課題を報告する
- `company-facts.md` がなくても一般論と確認済み出典で書ける場合は続行し、SOLSTAR固有情報は `【要記入: ...】` として残す
- `company-facts.md` やキーデータが不足し、記事の主張そのものが成立しない場合は停止して不足を報告する
- `pre-publish-checker` が不合格なら下書き保存に進まず、修正点を報告する
- Shopify / Google Drive の接続や認証が不足している場合は、その時点で止めて必要な接続を報告する

### Output Expectations

- 設計だけで止まらず、可能なら下書き保存まで進める
- ただし公開はしない
- 各段階で主要な成果物パスを明示する
- 迷った場合はSEOテクニックより読者体験を優先する

## How To Ask Codex

- `new-article を "Shopify 越境EC 始め方" で実行して`
- `Marketing向けに、価格設定 心理学の記事を最初から下書き作成まで進めて`
- `キーワード未定なので keyword-strategist から始めて`

## Migration Notes

- `.claude/agents/` は Claude Code 用の定義として残してよい
- Codex ではこの `AGENTS.md` を正本として扱う
- 仕様差分が出たら、まず `AGENTS.md` を更新し、その後必要なら Claude 側定義も同期する
