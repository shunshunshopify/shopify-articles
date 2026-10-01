# Codex Project File

このリポジトリは、株式会社SOLSTARのShopifyブログ記事をCodexで制作するためのワークスペースです。
Codexはこのファイルをプロジェクト共通ルールとして参照し、記事の設計・執筆・校閲・審査・下書き保存を進めます。

## Purpose

- Shopify / Marketing / Branding ブログ向けのSEO記事を制作する
- 成果物は `drafts/` に保存する
- Shopifyへの反映は必ず下書き (`isPublished: false`) で行う
- 公開操作は人間が行う
- 人間ライターの下書きとレビュー済み原稿は、指定のGoogle Driveフォルダを受け渡しの正本とする

## Google Drive Draft Folder

- Folder URL: `https://drive.google.com/drive/folders/1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee`
- Folder ID: `1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee`
- 人間執筆記事のレビューは、ユーザーが指定した個別ファイルURLだけを対象にする
- フォルダ内の先頭記事や同名記事を推測で選ばない
- 原本は明示依頼がない限り上書きせず、レビュー済み版を同フォルダへ別ファイルとして保存する
- Driveへの保存後は、返されたURLとファイルIDをreadbackで確認してからShopify工程へ進む
- `drafts/` は処理中のローカル成果物置き場であり、人間との受け渡し正本はGoogle Driveとする

## Shared Rules

- Codex実行時はリポジトリ直下の `AGENTS.md` を正本とする
- 記事は SOLSTAR 向けの実務的なSEOコンテンツとして扱う
- 事実が不明な内容は創作しない
- 未確認の事実、数値、実績、口コミ、導入事例、支援実績は追加・変更・創作しない。確認済み出典による事実の記述・訂正は許可し、根拠と変更理由をsourcesへ残す。人間原稿の実績・体験は推測で補わない
- 不足情報は創作せず、本文成立に必要なものと将来提案を分けて記録する。提案は自動的に本文へ追加しない
- 記事内容と矛盾する情報を追加しない
- `article-template.html` の CSS / TOC / JSON-LD の枠は改変しない
- JSON-LDの例外は、確認済み著者の`author`追加、未公開で実際の公開日がない場合の`datePublished`省略、および指定プレースホルダの置換だけとする。テンプレート保守は記事生成と分け、検査も更新する
- 記事生成・Rewriteのたびに、その時点の `article-template.html` を読み直す。過去記事や既存下書きの `<style>` を流用せず、最新版テンプレートの `<style>` をそのまま使う
- 既存記事との重複を避ける
- 海外記事や研究は参考にしてよいが、翻訳転載はしない
- 検索上位記事の単なるリライトではなく、SOLSTARならではの価値を加える
- SEOだけでなく、読者体験（UX）を最優先にする
- 2026年時点の SEO / AIO / E-E-A-T を意識する
- AIO・AEO・GEO・LLMOは下記「AI Search And Answer Quality」の共通基準で扱い、略語ごとに同じ審査を重複させない
- 公開前提で進めず、まずは設計・執筆・レビュー用成果物を保存する

## Pipeline

`keyword-strategist` -> `article-designer` -> `fact-checker (pre-write)` -> `article-writer` -> `fact-checker (post-write)` -> `content-asset-planner (必要時)` -> `japanese-editor` -> `japanese-quality-reviewer` -> `article-reviewer` -> `legal-reviewer` -> `article-validator` -> `drive-draft-saver`（Google Drive保存・readback）-> （Shopify下書きを明示依頼された場合のみ）`Shopify Input Preparation` -> `pre-publish-checker` -> `article-publisher`

必要なキーワードがすでに決まっている場合は `keyword-strategist` を省略してよい。通常の `new-article` は `drive-draft-saver` によるGoogle Drive保存・readbackまで自動で実施する。Shopify下書き保存は明示依頼時だけ実施し、その場合に限り `pre-publish-checker` と `article-publisher` を起動する。

## Source Of Truth

- Codex運用の判断基準、工程順、責務分担、停止条件はこの `AGENTS.md` を唯一の正本とする
- 周辺ファイルは、この `AGENTS.md` に書かれた契約を実装するための補助資料または実装詳細として扱う
- 周辺ファイルの記述が `AGENTS.md` と矛盾する場合は、Codexは `AGENTS.md` を優先する
- 中央指揮と工程の実行判断はメインのCodexが担う。`article-orchestrator` 定義はメインが参照する進行手順の補助であり、別の中央指揮サブエージェントとして起動しない

## Dependency Map

### Required To Read

- `AGENTS.md`
  役割、ルール、工程、停止条件、成果物仕様の正本

### Required At Runtime

- `article-template.html`
  `article-writer` が本文HTMLを書き込むテンプレート。毎回ディスク上の最新版を読み、CSS / TOC / JSON-LD の枠は変更しない
- `theme-css/solstar-article.css`
  記事共通Styleの最新版正本。`article-template.html` の `<style>` は、このCSSと意味上同一でなければならない
- `scripts/shopify_publish_guard.py`
  Shopify記事作成mutationに`isPublished: false`と有効な`global.description_tag`が含まれることを機械的に検査する。コネクターだけでなくShopify CLI経由でも実行前に使う
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
- `data/published-articles.md`
  公開済み記事の正本（handle・タグ・公開状態・カニバリ注意）。`keyword-strategist` の重複確認、`article-designer` のカニバリ確認・内部リンク選定、`article-writer` の内部リンクhandle確定、`scripts/article_validator.py` の内部リンク検証が参照する
- `drafts/<handle>-sources.md`
  `fact-checker` の成果物。新規・人間原稿ともpre-writeで作成し、writer以降の編集・審査では必須参照。外部検証対象がない場合もその理由と独自考察の根拠を記録する
- `drafts/<handle>-assets.md`
  `content-asset-planner` の成果物。`pre-publish-checker` と公開前の人間確認で使う
- `drafts/<handle>-japanese-review.md`
  `japanese-quality-reviewer` の成果物。自然な日本語、段落論理、用語、リズム、文体統一の合格記録として使う
- `drafts/<handle>-drive.md`
  `drive-draft-saver` の保存記録。Google Doc URL、file ID、MIME type、readback結果、未解決事項を記録する。Shopify下書き工程はこの記録の合格結果を必須入力とする
- `drafts/<handle>-shopify.html`
  Shopify下書きが明示依頼された場合にメインの実行主体が作る投入用コピー。審査済みHTMLとの差分は承認されたJSON-LDの値確定だけに限定する
- `drafts/<handle>-search-performance.md`
  公開後に依頼された `review-search-performance` の記録。設計・改稿では該当記事の記録があれば参照する

## Dependency Rules

- Codexが最初に読むべきファイルは `AGENTS.md` のみでよい
- その後は、実行する工程に必要な依存だけを追加で読む
- `article-template.html` は `article-writer` 着手前に必ず読む
- `theme-css/solstar-article.css` と `article-template.html` のStyle整合はメインがwriter着手前に確認し、`article-validator` が完成後にも検査する。不一致時は先にテンプレートを最新版へ同期する
- `company-facts.md` は SOLSTAR固有情報を書く必要が出た時点で必ず読む
- `data/published-articles.md` は `keyword-strategist` の重複確認、`article-designer` の設計着手前、`article-writer` の内部リンク確定前に必ず読む

## Runtime Contracts

### Input Contracts

- `keyword-strategist` はテーマ未定またはキーワード未指定で起動してよい
- `article-designer` はキーワードと投稿先ブログが決まってから起動する
- `fact-checker` は `drafts/<handle>-brief.md` 生成後に起動する
- `article-writer` は `drafts/<handle>-brief.md` とpre-write済みの `drafts/<handle>-sources.md` を必須入力とする
- Google Drive保存前は、`article-writer`、`fact-checker (post-write)`、必要時の`content-asset-planner`、`japanese-editor`、`japanese-quality-reviewer`、`article-reviewer`、`legal-reviewer`、`article-validator` をすべて完了させる
- `drive-draft-saver` は `article-validator` 合格後にのみ起動し、Google Driveへの保存とURL・file IDのreadbackを完了させる
- `pre-publish-checker` と `article-publisher` は、Shopify下書き作成を明示依頼された時点でのみ実行する
- `content-asset-planner` は `drafts/<handle>.html` 生成後、図解・画像などの素材設計が必要な場合だけ起動する
- `japanese-editor` は `drafts/<handle>.html` だけを編集対象にする
- `japanese-quality-reviewer` は `japanese-editor` 完了後に起動し、`drafts/<handle>.html` と `drafts/<handle>-brief.md` を必須入力とする
- `article-reviewer` は `drafts/<handle>.html` と `drafts/<handle>-brief.md` がそろってから起動する
- `legal-reviewer` は `article-reviewer` 合格後に起動する
- `article-validator` は `legal-reviewer` 合格後に `scripts/article_validator.py --allow-draft-placeholders` を実行する。どのモードも確定メタを含むブリーフを必須入力とする。Shopify下書きの明示依頼時は、メインの実行主体が「Shopify Input Preparation」に従って投入用コピーを準備し、`pre-publish-checker` の直前にコピーを通常モードで検査する
- `pre-publish-checker` は審査済み原稿と投入用コピーがそろい、コピーの通常モード検査が合格してから起動する
- `pre-publish-checker` はブリーフの確定メタディスクリプションとJSON-LDの`Article.description`が完全一致しない場合は不合格とする
- `article-publisher` は `pre-publish-checker` 合格後しか起動せず、確定メタディスクリプションをShopifyの`global.description_tag`へ設定する

### Output Contracts

- `keyword-strategist` は `drafts/keyword-candidates.md` を生成する
- `article-designer` は `drafts/<handle>-brief.md` を生成する
- `fact-checker` は `drafts/<handle>-sources.md` を生成する
- `article-writer` は `drafts/<handle>.html` を生成する
- `content-asset-planner` は `drafts/<handle>-assets.md` を生成する
- `japanese-editor` は `drafts/<handle>.html` を上書きする
- `japanese-quality-reviewer` は `drafts/<handle>-japanese-review.md` に日本語品質の審査結果を保存し、本文は編集しない
- `article-reviewer` は `drafts/<handle>-review.md` にレビュー結果を保存し、本文は編集しない
- `legal-reviewer` は `drafts/<handle>-legal-review.md` に法務リスクと合否を保存し、本文は編集しない
- `article-validator` は決定論的な検査結果を返すが、本文は編集しない
- `drive-draft-saver` は `drafts/<handle>-drive.md` に保存記録を残し、Google Doc URL・file ID・MIME type・readback結果を返す
- `pre-publish-checker` は合否と修正点、元原稿・投入用コピーのSHA-256を `drafts/<handle>-pre-publish.md` に記録する。本文は編集しない
- `article-publisher` は Shopify に下書きを作成し、`global.description_tag`と`isPublished: false`をreadbackして、管理用URL・保存したMeta description・確認結果を`drafts/<handle>-shopify.md`へ記録する

### Fallback Contracts

- `company-facts.md` がない場合でも、一般論と確認済み出典だけで成立する記事なら続行してよい
- `company-facts.md` がないためにSOLSTAR固有情報が必要な主張を書けない場合は `【要記入: ...】` を残す
- 出典確認ができない主張は本文へ断定的に書かない
- Google Drive や Shopify に接続できない場合は、その工程で止めて必要な接続を報告する

### Gate Lifecycle And Draft Exceptions

- 各ゲートの不合格は「後工程へ進めない」という意味であり、修正可能なら指定担当へ差し戻す。最大3周は初回を含む同じゲートの審査3回とし、上限に達しても不合格ならタスクを停止する。writerへ戻しても回数をリセットしない。validatorの修正・再検査も最大3回とする
- 本文・タイトル・メタ・構成・事実をwriterが変えたら、fact-checker（post-write）→必要時の素材計画更新→japanese-editor→日本語審査→総合審査→法務→validatorの順で、後工程へ渡すまでに再合格させる。日本語editorだけの意味不変編集でも、日本語審査以降の既存合格は失効する
- 各審査は対象HTMLのSHA-256を記録する。法務・Drive・投入準備は直前の日本語・総合・法務の合格が現在の原稿に対するものか照合する。fact-checker後の意味不変編集はeditorの変更報告で追跡し、意味の変化が疑われる場合はwriterとfact-checkerへ戻す
- 日本語editorが見出しを変えた場合、HTMLとTOCを同期し、メインがbriefの見出し文だけを同じIDに対して同期する。意味・SEO意図の変更はwriterへ戻す。これによりeditorの編集対象はHTMLだけに保つ
- 記事の主要な結論に影響しない不足情報は `【要記入: ...】`、`【要確認: ...】`、`【内部リンク要記入: ...】` または `<!-- 要確認: ... -->` で明示し、各審査は未確認の事実として断定されていないことと本文の成立を確認して下書き合格にできる。Driveは必ず `needs_human_input` とする。本文の主張が成立しない不足はこの例外を使わず停止する
- `{{...}}`、確定タイトル・確定メタの欠落は下書きでも許さない。公開用JSON-LDトークンだけは通常の下書きで許容し、回答品質ゲートでは値の確定を投入準備で行う旨を記録する。未確認任意情報の省略理由や本文外の将来提案は、それ自体を未解決の本文として扱わない
- 下書きの目安と機械検査の上限を区別する。FAQは3〜5問、「この記事でわかること」は4〜6項目を現行テンプレートの必須範囲とする。記事別の例外が必要なら契約・検査を先に変更する

## Files

- `article-template.html`: 記事HTMLテンプレート
- `drafts/`: 設計ブリーフ、記事HTML、候補メモの保存先
- `data/`: GSCエクスポートや関連データの保存先
- `company-facts.md`: SOLSTAR固有の実績・事例・料金の参照元。存在しない場合は創作せず `【要記入: ...】` を残す

## Article Requirements

### AI Search And Answer Quality

- AIOはAI検索全般（GoogleのAI Overviewsを含む）への対応、AEOは質問に直接答える構成、GEOは生成AIが根拠として参照できる情報品質、LLMOは名称・関係・条件を誤解しにくい情報設計として運用する。これらは独立した必須HTML規格ではない
- 設計ブリーフに「質問・回答・条件・根拠の対応表」を必ず作る。列は `質問ID / 読者の質問 / 主・補足 / 回答する見出し・ID / 答えの要点 / 適用条件・例外 / 根拠IDまたは確認予定 / 独自の判断・次の行動` とする。主検索意図の回答漏れは設計で差し戻す。無関係な質問や検索語の全変種を増やさない
- 主要な質問には本文で直接答え、必要な対象・時点・条件・例外を近くに置く。「この記事でわかること」の予告を回答の代わりにしない。簡潔な1〜2文は目安であり、固定文字数や全見出しの疑問文化は要求しない
- 重要な数値・比較・変化しやすい事実は、該当文・表の近くに出典リンクまたは参照番号を置き、対象・確認時点を示す。根拠のない一般化を避け、事実とSOLSTARの考察・助言を区別する
- 出典台帳には `根拠ID / 支える主張・質問ID / 本文位置 / 出典URL・該当箇所 / 公表・更新日 / 確認日 / 対象・適用条件 / 検証結果` を記録する。日付不明は不明と書き、確認日と混同しない。助言は根拠と推論のつながりを示し、未確認の経験談へ変えない
- 専門用語は必要性を確認し、平易な説明を先に置く。初出だけでなく、表・FAQ・独立した節から読み始めても主要な判断を理解できるか点検する。必要な短い補足だけを加え、毎回同じ説明を繰り返さない
- 著者・監修者・発行者を区別する。構造化データの名前・役割・主題・日付・URLは確認済み情報と一致させる。監修者を自動的に著者にしない。未確認の任意情報は省略して理由を記録する。公開ページではテーマが出力するデータも含めて重複・矛盾を確認する
- 標準著者はユーザー確認済みの島袋隼とし、company-facts.mdの著者情報を正本としてArticle.authorのPersonに名前・役職・所属組織を記載する。日本語記事のjobTitleは「代表取締役」に統一し、worksForとpublisherは同じSOLSTARのOrganizationを参照する。人間原稿などで別の著者が確認されている場合は筆者の情報を保持し、監修者との同一性を推測しない。人物@idは識別子として扱い、未確認のプロフィールURL・写真・SNSを追加しない
- `article-reviewer` は下記の「回答品質ゲート」を独立した合否表として記録する。各行に `passed / failed / not_applicable`、対象箇所、根拠、修正先を記載する。該当なしは理由が必要で、主要質問への直接回答・初心者理解・独自価値を該当なしにしない
  1. 主検索意図への直接回答と対応表の充足
  2. 回答に不可欠な条件・例外・対象・時点の保持
  3. 重要な主張と出典の対応、出典が支える範囲
  4. 初心者理解と、表・FAQを含む独立した箇所の明瞭さ
  5. 確認済み事実に基づく独自の判断・次の行動
  6. 会社・人物・主題・日付など、本文と構造化データの整合
- 上記に重大な欠落があれば総合点にかかわらず不合格。対応表・出典台帳・合否表の欠落も完了扱いにしない。文章調整後も条件・根拠が失われていないか審査する。定義や事実が変わる修正はwriterへ戻し、fact-checkerから再実行する
- AIへの掲載・引用・モデル学習への採用を保証しない。引用数、質問文の個数、専用スキーマ、llms.txt、細かい文章分割を合格条件にしない。公式ガイドの確認日を記録し、変更される仕様を過去の記憶だけで断定しない
- FAQPage・QAPage・HowToは内容に合う場合だけ採用候補にする。FAQPageは運営者が用意した複数の質問と回答、QAPageは単一の質問に利用者が回答を投稿できるページ、HowToは目的を達成するための順序付き手順に使う。通常のブログFAQにQAPageを使わず、一般的な助言の箇条書きをHowToへ変換しない。本文に表示する質問・回答・手順と構造化データを一致させ、根拠・対象・条件・例外を落とさない。採用する場合はdesignerがbriefへ用途を記し、fact-checkerが最新の適用条件を確認し、article-reviewerが本文との整合を回答品質ゲートで審査する。追加はShared Rulesに従うテンプレート保守と検査更新を先に行い、記事生成中にJSON-LDの枠を独自に増やさない
- 構造化データとして表現できること、Googleのリッチリザルトに対応すること、AI検索で参照されること、AIモデルの学習に使われることを区別する。FAQPage・HowTo等の追加をAIOの必須条件や掲載・学習採用の保証にしない。公開サイトの取得・検索登録・生成AI検索への参加設定・計測はreview-search-performanceの担当とし、ローカル原稿の品質合格だけでサイト全体のAIO対応完了と報告しない

運用仕様の確認基準（確認日: 2026-10-01）: [Googleの生成AI検索ガイド](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)、[生成AI検索への参加設定](https://support.google.com/webmasters/answer/16908024)、[生成AIパフォーマンスレポート](https://support.google.com/webmasters/answer/16984139)、[QAPageの適用条件](https://developers.google.com/search/docs/appearance/structured-data/qapage)。FAQ・HowToのGoogle検索での対応状況は[公式更新履歴](https://developers.google.com/search/updates)も参照する。この確認日は当該サイトの実設定・計測結果の確認を意味せず、運用時に最新資料と実際の取得可否を再確認する。

### Brief Metadata Contract

- 確定メタディスクリプションは、ブリーフの `## 機械検証用メタデータ` に置くJSONコードブロック1つを正本とする。キーは `meta_description` のみ、値は確定した1行の文字列。別の見出し・案・表に確定値を重複管理しない
- 記述形式は次のとおり（例文は実際の記事に合った80〜120字程度の確定値へ置換する）。この節にはコードブロック以外を書かず、次の節はH2見出しで始める

```json
{"meta_description": "記事の主題・対象読者・読了メリットを反映した確定文"}
```

- 新規・Rewrite・人間原稿の改稿すべてに適用する。既存ブリーフを使うときは、designerまたはhuman-draft-reviewerが既存の確定値を確認してこの形式へ移す。HTMLの値を無条件で正本へコピーしない。候補が複数ある場合は内容と照合して1つに確定する
- validatorは既定で記事と同じ場所の `<stem>-brief.md` を読む。別名の投入用コピーでは `--brief drafts/<handle>-brief.md` を指定する。ブリーフの欠落・形式不備・仮値・メタ不一致は下書きモードでも不合格

### Editorial Standard

文体・見出し・補足の採否はこの節を唯一の共通基準とし、各Roleへ再掲しない。事実と根拠の記録は「AI Search And Answer Quality」、編集できる範囲は「Agent: `japanese-editor`」に従う。

#### 読者と記事の範囲

- 読者は技術者ではない経営者、事業責任者、EC・マーケティング担当者。大人向けの専門的な内容を、中学2〜3年生でも意味を追える日本語で書く。専門性や必要な情報量を保ちながら読む負荷を下げ、主質問への答えを先に伝える。
- briefの検索意図欄に「主質問 / 読了後に理解・判断できること / 扱う範囲 / 扱わない隣接テーマ」を短く記す。質問対応表と重複する大きな台帳は作らない。
- 競合の共通論点や不足論点は候補であり、掲載必須ではない。主質問への回答、理解に必要な説明、正確さに必要な条件に絞って採用する。
- 各節は一つの中心論点を持つ。記事全体で理解・判断・次の行動につなげるが、定義・比較・具体例などすべての節に影響・助言・行動を一律に足さない。
- 技術仕様や操作手順は、検索意図または読者の判断に必要な場合だけ扱う。出典の章立てや専門性の高さを、そのまま記事の構成へ持ち込まない。

#### 補足を残す・削る基準

| 情報の役割 | 本文での扱い |
|---|---|
| 主質問への答え、理解を助ける具体例・用語説明 | 必要な箇所で説明する |
| 主張の成立に必要な対象・時点・条件・例外、誤解が判断や安全に影響する注意 | 該当する回答・表・例の近くへ簡潔に置く |
| 関連はあるが別の質問を解決する情報 | 原則省く。必要なら確認済み関連記事へ案内する |
| 調査経緯・出典採用理由・審査上の説明 | sourcesへ記録する。本文には根拠が支える主張と、誤認を防ぐのに必要な区別だけを残す |
| 同じ結論・条件の言い換えや、なくても理解・判断・正確さが変わらない注意 | 削除または統合する |

- 「念のため」「独自性のため」「出典があるから」だけを追加理由にしない。引用の対象を明確にし、内部記録への移動で根拠のない一般化や事実と考察の混同を起こさない。
- 表・FAQを単独で読む場合に不可欠な条件は残す。複数の節に共通する注意をまとめる場合も、結論の成立条件を回答から切り離さない。
- 削除は文字数削減のために行わない。理解を助ける例や説明は、読者の行動が変わらないという理由だけでは削らない。

#### 見出し

- 見出しは一つの中心論点を、一般的で自然な語の組み合わせで表す。正確さ、意味の明瞭さ、本文との一致、続きを読む理由の順に優先し、SEOキーワードは自然に含められる場合に使う。コピーのために検索意図・事実・条件を変えない。
- H2は章の答えや発見を示し、記事を読み進める理由を作る。H3は説明する対象や内容をより具体的に示し、H2の論点を理解しやすくする。すべてのH3を強いコピーにする必要はない。
- 「概要」「ポイント」だけで内容を予測できない分類名、意味の説明が必要な比喩、抽象語の詰め込みを避ける。内容と読む価値が明瞭な名詞句や定義・費用などの見出しは許容し、分類名という理由だけで不合格にしない。主語・動詞・結論・行動を全部入れることや、動詞で終えることを必須にしない。
- 読む理由は、読者の疑問、判断に役立つ結論、本文で説明する発見などから作る。結論の提示、疑問、比較、誤解の解消、根拠のある数字などは必要に応じて使い、型の使用や意外性自体を目的にしない。「知らないと損」「絶対」「劇的」などのあおりやクリックベイトを避ける。
- 本文より強い断定・誇張を見出しへ加えない。仮説を決定へ、継続できる強みを模倣されない強みへ変えるような意味変更は、自然な言い換えとして扱わない。
- H2を上から順に並べ、記事の流れ、各章を読む理由、同じ型の過剰な反復、本文との約束の一致を確認する。「〜とは」「〜の方法」などの語尾だけで合否を決めず、全体として論点や読む価値が伝わるかを判断する。冒頭の必須見出し、FAQ、まとめ、参考文献は所定の役割を優先し、コピー化を求めない。

#### 文章と語彙

- 落ち着いた実務文で、前の文から次の文へ疑問が解消する順に説明する。主述、助詞、係り受け、指示語、段落間の因果関係を確認し、文法が成立するだけで自然と判定しない。
- 一文の短さや漢字の学年を機械的な基準にしない。難しい漢語、抽象名詞の連続、名詞化された表現を見直し、誰が何をするか、何が起こるかを一読で追える言葉にする。必要な説明、正式名称、サービス名、法律名、正確な専門用語は保つ。
- 一般的な言葉で同じ意味を自然に伝えられる場合は、その表現を優先する。「選定する→選ぶ」「明確化する→はっきりさせる」「〜することが可能です→〜できます」は参考例であり、置換辞書や禁止語一覧にしない。「担保する」「訴求する」なども文脈ごとに意味の範囲を確かめ、専門性や条件を損なう機械的な置換はしない。
- 読者が比較・把握しにくい列挙は箇条書きや表にする。スマホの1段落3〜4行は目安であり、論理のまとまりを優先する。
- 同じ語尾、逆接、否定して補足する構文の反復を文脈で直す。「重要です」「求められます」「といえるでしょう」「という観点から」などの固い定型表現も、必要な意味を保って自然に整える。「AではなくB」はAを否定する必要がある場合に使う。出現回数だけで禁止・不合格にせず、必要な対比は残す。
- タイトル、メタ、見出し、本文、FAQ、アンカー、CTAの語調をそろえる。読者への過剰な呼びかけ、あおり、幼い言い換えを避ける。
- 読者表示テキストではダッシュ（──／—／―）を使わず、句読点・丸カッコ・文の分割等で表す。機械検査と一致させる。

#### 用語・独自性・助言

- 不要な専門語は平易にする。不可欠な用語は意味を先に説明し、正式名称を初出で短く補足する。必要な場合だけ読み仮名を添える。表・FAQの説明要否は「AI Search And Answer Quality」に従う。
- 翻訳語の自然さ・読者への浸透度・定義の正確さを確認し、迷う場合は出典やWebで調べる。用語計画へ判断を記録し、同一概念を語彙の変化だけを目的に言い換えない。誤った過去の用語判断はwriterへ戻す。
- 独自性は主題内の比較・判断軸・具体的な説明で出す。一般論や隣接テーマを足して差別化しない。
- 読者の迷いを減らす短い判断・助言を本文に自然に含める。2〜4か所は目安であり、専用のコメントや数合わせの注意書きを作らない。主題内で判断を示していれば、別のコメントがないことだけで不合格にしない。
- 経験・実績を装う表現はShared Rulesの根拠要件に従う。監修者の口調や未確認の体験談を創作しない。

### Shopify Relevance

- designerは `直接関連` / `一部関連` / `非関連` と理由・扱う範囲をbriefへ記す。
- 直接関連でも検索意図に必要な範囲だけ解説する。一部関連では比較・判断に役立つ箇所だけ触れ、非関連では機能説明・FAQ・Shopify構築相談CTAを追加しない。
- Shopify上での掲載は本文へ触れる理由にならない。内部リンク・CTAを含む他の隣接テーマにもEditorial Standardの関連性判断を適用する。

### Title And Meta

- 記事内容に合わせてメタタイトルとメタディスクリプションを作成する
- `article-designer` は80〜120字を目安に**確定メタディスクリプションを1つ**決め、空欄・仮値・複数案のまま後工程へ渡さない
- タイトル、メタ、本文の内容を一致させる
- 検索意図を満たしつつ、クリックしたくなる表現にする
- タイトルに数字を使う場合は、本文でもその数が分かる構成にする
- 確定メタディスクリプションは、ブリーフ、JSON-LDの`Article.description`、Shopifyの`global.description_tag`で完全に同じ文字列を使う
- Shopifyの`summary`は抜粋用であり、SEOメタディスクリプションの代替にしない

### Opening Structure

記事冒頭は原則として次の順序で統一する。

1. 最終更新日
2. 著者・監修者情報
3. 導入文
4. H2「この記事でわかること」
5. 目次

標準記事では、著者と監修者が同じ人物の場合は次の著者表記1行にまとめ、同じ人物の監修文を重ねない。経歴や専門性は末尾の著者プロフィールにまとめ、記事の主題に必要な場合だけ冒頭へ補足する。

`最終更新日：YYYY年MM月DD日`

`著者：島袋隼（株式会社SOLSTAR 代表取締役）`

別の執筆者が確認された人間原稿では、writerが著者表示とArticle.authorをその筆者に合わせる。著者と異なる監修者について、実際の監修と人物・役職が確認できた場合だけ `監修：氏名（所属・役職）` を追加する。標準監修者を機械的に付けず、company-facts.mdとsourcesへ確認根拠を残す。表示上の著者とArticle.authorの人物を一致させる。AIOを理由に同じ氏名・肩書き・年数を反復しない。

### Introduction

- 導入文は300文字程度を目安とする
- 読者の悩みや検索意図に触れる
- 結論を簡潔に伝える
- 本記事で扱う内容と切り口を示す
- 読了メリットと対象読者を示す
- 上位記事との差分や実務上の付加価値を示す。ただし「単に○○を紹介するだけでなく、△△まで解説します」などの固定構文を毎回使わず、記事内容に合う自然な文で表現する

### What Readers Will Learn

- 導入文の直後に、H2「この記事でわかること」を必ず置く
- 箇条書きは4〜6項目とする
- 本文で実際に解説する内容と一致させる
- 数秒で読むメリットが伝わる内容にする

### Headings And TOC

- 見出しの表現はEditorial Standardに従う。H2だけで記事全体の流れ、H3で各節の内容を把握できるようにする。
- 本文の主要H2は原則連番とし、「この記事でわかること」「よくある質問」「まとめ」「参考文献」は連番なしでよい。宣言した件数と本文の項目数を一致させる。
- 目次は一覧性を優先し、全H3を掲載する必要はない。掲載見出しの文言・アンカーIDを本文と一致させる。

### FAQ

- FAQは記事末に設置する
- 配置は「まとめ」の直前を基本とする
- 各質問のH3見出しは必ず先頭に「Q.」を付ける（例: `<h3>Q. 〇〇はどのくらいですか？</h3>`）。回答本文に「A.」は付けない
- 3〜5問とし、本文の補足になる内容を入れる
- 本文と重複しすぎる内容は避ける
- ロングテールの疑問や検索ユーザーの不安を意識する

### Sources And References

- 重要な主張の出典表示はAI Search And Answer Qualityに従い、参考文献一覧は必要に応じて掲載する
- テーマに合う一次情報、官公庁、論文、信頼できる調査を優先する。Shopify公式はShopifyに直接関係する事実を確認する場合に優先する

### Images And Diagrams

- 必要に応じてオリジナル画像や図解を提案する
- 図解の内容だけでなく、記事内の挿入位置も提案する
- 未作成の画像や図解を本文に実在画像として埋め込まない
- テーマに応じて、管理画面、比較図、導線図、フロー図、グラフなどを候補にする。Shopify管理画面はShopifyに直接関係する記事でのみ候補にする

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

同じ品質項目をここで再採点しない。メインはRuntime Contractsに従い、現在のHTMLに対する日本語・総合・法務・validatorの合格、必須成果物、未解決事項を照合する。内容基準はEditorial StandardとAI Search And Answer Quality、保存条件は各保存担当の契約を参照する。

## Agent: `fact-checker`

### Role

記事で扱う変化しやすい情報や根拠が必要な情報を、本文作成前後に検証する。Shopify仕様、料金、法制度、統計、調査、研究、公式情報の確認を担当する。

### Inputs

- `drafts/<handle>-brief.md`
- 必要に応じて `drafts/<handle>.html`

### Tasks

1. `pre-write` ではブリーフから事実確認が必要な論点を抽出する
2. `post-write` では完成HTMLの主張、数値、比較、引用を一文ずつ出典メモと照合する
3. テーマに合う一次情報、官公庁、論文、信頼できる調査を優先して確認する。Shopify公式はShopify関連の主張を検証する場合に使う
4. 変化しやすい情報は最新性を確認する
5. 出典として使えるURL、確認日、本文での使いどころを整理する
6. 不確かな情報、確認できない情報、SOLSTAR固有情報の不足を明示する

### Output

`drafts/<handle>-sources.md` に保存し、要約を返す。内容には以下を含める。

- 確認済みの事実
- 推奨出典
- 本文で使う場合の候補箇所（掲載の要否はEditorial Standardとbriefの範囲で決める）
- 使用禁止または要確認の情報
- 主質問への回答に必要な不足情報と、本文外の将来提案を区別する
- 「AI Search And Answer Quality」に従った出典台帳。post-writeでは主張の対応、限定条件、本文近くの出典表示を照合し、審査したHTMLのSHA-256と合否を記録する

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

### Tasks

1. Ahrefs候補を確認し、ボリューム・難易度・意図を把握する
2. GSCデータから、伸びしろ・取りこぼし・既存露出の有無を確認する
3. 3C分析で、SOLSTARが勝てるかどうかを補正する
4. 既存記事と重複しない候補を優先順位付きで整理する
5. UXとE-E-A-Tの観点から、一般論に寄りにくいテーマを優先する
6. 関連する `drafts/<handle>-search-performance.md` があれば、確認期間と欠測を区別して既存記事の改善候補へ反映する。AI表示・引用指標をGSCの順位・CTRや成果と混同せず、既定のスコアへ根拠のない加点をしない

### Scoring Details

- Ahrefs候補プール: Google Drive連携で読む。ECサイト系 fileId `1EnCG1a2NEozHJ0VQSjpXcZ14wttjUTfkYpP7mh1KxK8` / Shopify系 fileId `1dV_Un3QSZHVn3YP3QQhno5qdwp5KFuzytXjCpzkk7Fk`。抽出基準: Volume ≥ 1,000 × KD ≤ 20 × Intent = Commercial
- GSC伸びしろ判定: position 8〜20 かつ impressions ≥ 1,000 → 上位10本を最優先。取りこぼし判定: impressions ≥ 1,000 かつ CTR < 1.0%
- 優先度スコア = 40% Ahrefs適性 + 35% GSC伸びしろ + 15% 3C評価 + 10% 新規余地（各0〜10点で加重平均、同点時はGSC impressions高い順）
- いずれかのソースが読めない場合は「データ取得失敗: file/ID=...」と明示し、利用可能なソースのみで継続する

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

### Role And Inputs

キーワードと投稿先ブログを受け取り、主質問に答える範囲と章の役割を設計する。本文は書かない。共通編集基準はEditorial Standardに従う。

### Tasks

1. 検索上位記事を10件程度調べ、共通論点と不足論点を候補として抽出する。主質問への必要性を判断して採否を決める。
2. 読者、Know/Do/Buyの検索意図、記事の範囲を決め、章ごとに何へ答えるかを明らかにする。関連するsearch-performance記録があれば観測事実と仮説を分けて参照する。
3. `data/published-articles.md` で重複を確認し、関連する公開済み記事を内部リンク候補にする。2〜3本は目安とし、本数のために範囲を広げない。
4. 見出し、必要なFAQ・素材、主題内の独自の判断を設計する。各主要H2の答えと読む理由を決め、本文完成後にwriterが見出しを調整できるよう、見出し文と章の役割を区別する。Editorial StandardのH2一覧確認を設計時に行う。

### Output And Handoff

`drafts/<handle>-brief.md` に以下を保存する。

- handle、投稿先ブログ、タイトル案3つと採用タイトル1つ、タグ、想定文字数。タイトルはキーワードを前半に含め32文字前後を目安とする。
- 検索意図欄の主質問・読了後の状態・扱う範囲・扱わない隣接テーマ、Shopify関連度。
- H2/H3のID・見出し案・各章の答え。各主要H2には読む理由（解決する疑問や伝える発見）を添え、同じ章設計欄にH2一覧確認の結果と必要な修正を記す。主題内の差別化・判断軸、FAQ案、内部リンク候補のhandle/URL/位置、必要時の素材案。
- AI Search And Answer Qualityの質問対応表・用語計画。読み手に必要な用語だけを計画し、補足質問を数合わせで増やさない。
- 確定メタはBrief Metadata ContractのJSONに一度だけ記載する。

主質問への回答漏れ、記事範囲・採用タイトル・確定メタの欠落があれば設計を完了しない。本文に必要な答えがない見出しや、除外範囲の話題を後工程へ渡さない。

## Agent: `article-writer`

### Role And Inputs

briefとpre-write済みsourcesから本文HTMLを作る。初回、差し戻し、人間原稿の改稿に対応する。差し戻しは該当レビュー、人間原稿は指定原稿とhuman-reviewを追加で読む。

### Tasks

1. 毎回ディスク上の最新版article-template.htmlを読み、Shared Rulesの枠を維持して執筆する。内部リンクはpublished-articlesで公開状態とhandleを確定する。
2. 主質問・範囲・質問対応表・用語計画・確定メタが欠けていればdesigner（人間原稿はhuman-draft-reviewer）へ戻す。隣接テーマへ広げて不足を補わない。
3. 初稿からEditorial Standardの日本語基準を満たす本文を書く。editorは残る不自然さや重複を整える担当とし、固い文章を後から平易にする前提で執筆しない。完成後に補足の採否、本文の核心・条件・断定の強さと見出しの一致を見直し、H2一覧確認を行ってbriefの章設計欄を更新する。見出し案は固定せず、意味・検索意図・ID・階層を保って改善する。検索意図や章の役割が変わる場合はdesigner（人間原稿はhuman-draft-reviewer）へ戻してbriefから更新し、Gate Lifecycle And Draft Exceptionsに従う。範囲外の事実を削る必要があれば根拠と理由をsourcesへ記録し、残る主張・質問への回答を確認する。
4. タイトル・メタ・本文・TOC・質問対応表を同期する。JSON-LDのHEADLINEとDESCRIPTIONは確定値を使い、DESCRIPTIONはbriefと完全一致させる。
5. 著者・監修者表示はOpening Structureに従い、company-facts.mdとsourcesの確認済み役割を使う。同一人物の監修文を重ねず、Article.authorと一致させる。
6. 新規記事のPAGE_URL / DATE_* / BLOG_NAME / BLOG_URLは公開工程用トークンとして残す。公開済み記事の確認済みURLと実際の公開日は保持し、更新日は実際の本文更新に合わせる。著者を監修者から推定しない。
7. 重要な主張の出典は支える文の近くへ置く。調査経緯や出典採用理由はsourcesへ残し、読者に必要な適用条件だけを本文へ反映する。

### Output And Constraints

- `drafts/<handle>.html` と、変更した場合はbrief/sourcesの整合を確保し、文字数・残課題・差し戻し対応を報告する。
- Rewriteでは指摘箇所を優先し、問題のない箇所を無用に変えない。人間原稿の有用な表現、取材、論旨を保持する。
- 新規画像や事実・構成の変更後はGate Lifecycle And Draft Exceptionsの再審査を省略しない。未確認の画像・リンク・参考文献を確定情報にしない。

## Agent: `content-asset-planner`

### Role

記事本文とは分けて、内部リンク、図解、画像、参考文献、Core Web Vitals上の注意点を整理する。

### Inputs

- `drafts/<handle>-brief.md`
- `drafts/<handle>.html`
- `drafts/<handle>-sources.md`（必須）

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

### Role And Inputs

記事HTML、brief、sources、差し戻し時の日本語レビューを読み、Editorial Standardに沿って意味を保った文章編集を行う。編集対象は `drafts/<handle>.html` のみ。

### Tasks And Editing Authority

1. 先に見出しと段落を通読し、中心論点、情報順、説明の重複、突然の補足を確認する。その後、Editorial Standardの文章と語彙に沿って、一読を妨げる固さ、抽象的な言い回し、文型の反復を整える。
2. 同一セクション内で、意味が重なる文・不要な補足の削除、段落の統合・分割、文順変更、`p` と `ul/li` の変換を許可する。節は原則として同じ見出し配下の範囲とし、別の見出しをまたいだ移動はwriterへ戻す。
3. 削除・移動後も、質問への答え、事実、数値、引用、対象・時点・条件、出典との対応を保つ。重要な条件が表・FAQから離れる場合は実行しない。削除対象が唯一の根拠や主張を含む場合もwriterへ戻す。
4. 見出し文はEditorial Standardに沿って明瞭さと読む理由を確認し、FAQ質問、アンカーテキスト、CTAとともに意味不変で整える。TOC表示文を同期し、見出しIDを維持する。briefの見出し文はメインが同期する。新しい主張や強い断定を加えなければ改善できない場合はwriterへ戻す。

### Protected Elements And Returns

- CSS、テンプレート外枠、TOC枠、JSON-LD、見出し階層・ID、リンク先・出典、画像、表の行列、確認済み著者・監修者の役割、更新日、FAQ位置、CTAの役割、検索意図、SEOキーワード、必須項目数を保つ。許可した本文内の局所的タグ編集は「テンプレート枠の変更」に含めない。
- 章の追加・削除・移動、表の行列変更、主張・事実・条件・タイトル・メタの変更、原稿にない手段・主体・具体例の追加はwriterへ戻す。範囲外の内容も、意味不変の重複削除で扱えない場合はwriterへ戻す。
- 番号はbriefと本文から意図した件数を確定できる表示文言だけ直してよい。`ol start` / `li value` 等の属性、項目数、構成の変更はwriterへ戻す。

### Output

同じHTMLに保存し、変更前後のSHA-256、代表的な修正前後と理由、削除・移動した情報と保持先、主要用語の統一要否、writerへの差し戻し要否を報告する。疑わしい意味変更を「意味不変」と自己認定して隠さず、Gate Lifecycle And Draft Exceptionsに従う。

## Agent: `japanese-quality-reviewer`

### Role And Inputs

HTML、brief、sourcesを必須入力に、見出し・段落・文の一読理解を独立審査する。本文は編集しない。内容の範囲・検索意図・根拠の十分さは総合審査が主担当であり、日本語の自然さとは重複採点しない。

### Review Method And Axes

最初にHTMLの見出し・本文を読み、前工程の点数や「改善済み」という自己評価に依存せず引っかかる箇所を記録する。その後brief・sourcesと照合し、言い換えで意味や条件が落ちていないかを確認する。Editorial Standardを基準に各観点を100点換算し、下記の重みで総合点を計算する。

- 論理・段落構成（15%）：説明順、文間の接続、突然の補足。
- 文の自然さ・主述（20%）：助詞、語順、係り受け、自然な語の組み合わせ。
- 読みやすい語彙・専門用語・訳語（20%）：一般的な語で伝えられる固さの解消、必要な説明、概念の統一。
- リズム・反復（10%）：必要な反復と単調さを文脈で区別。
- 明瞭さ・簡潔さ・情報密度（15%）：FAQ・アンカー・CTAを含む一読理解、重複や補足で答えが埋もれないか。
- 実務文としての語調（5%）：落ち着き、自然な判断・助言、FAQ・アンカー・CTAを含む語調の一致。
- 見出しの吸引力・明瞭さ（15%）：Editorial Standardに沿った意味の明瞭さ、読む理由、表現の単調さ、本文との意味・強さの一致。好みや意外性の有無だけで採点しない。章の順序や検索意図との整合は総合審査が担当する。

### Pass And Return Rules

- 総合95点以上かつ各観点90点以上、重大な問題なしで合格。
- 主述の破綻、参照先不明、誤解を招く曖昧さ、主要判断に必要な用語の未説明、一読できない見出し・語順・不自然な語の組み合わせ、論理の飛躍、必要な意味・条件の欠落、宣言件数・連番の不整合は点数にかかわらず不合格。
- 重複・逆接・補足が理解を妨げる、または記事全体で不自然に反復する場合も不合格。単語の回数や軽微な表現の好みだけでHard Failにしない。
- 自然な平易語へ変えられる難しい熟語や固い定型表現が記事全体に続く、抽象名詞の連続や語順のために複数箇所で読み返しが必要になる、主要H2の多くから内容や読む理由が伝わらない、同じ見出し型の過剰な反復で論点の違いが見えない場合は不合格とする。該当箇所と読む負荷・理解への影響を具体的に示し、明瞭な名詞句や軽微な好みを問題扱いしない。見出しが本文より強い断定になっている場合も不合格。
- 意味不変の修正はeditor、内容・構成・事実・タイトル・メタの変更はwriterへ戻す。範囲外の話題や根拠問題に気づいた場合は総合審査向けに記録し、重大な問題はwriterへ戻して後工程を止める。
- 同じ問題を複数観点で重複減点しない。解消すべき問題を任意改善と呼び替えて合格させない。

### Output

`drafts/<handle>-japanese-review.md` に、対象SHA-256、総合点・各点・加重根拠、合否、重大度別の指摘（箇所・修正前・理解を妨げる理由・修正案・種別・差し戻し先）、維持すべき表現、用語・概念確認表を記録する。見出しの評価には、どの疑問・結論・発見が伝わるか、または何が伝わらないかを具体的に記す。問題なしの場合も確認範囲を示す。評価は読者が実際に読んだ際の理由で説明し、ルールの形式充足だけを根拠にしない。

## Agent: `article-reviewer`

### Role And Inputs

HTML、brief、sourcesと、現在のSHA-256に対する日本語審査の合格を入力とし、内容品質を審査する。本文は編集しない。日本語審査が未実施・不合格・別の版なら開始しない。

### Review Axes

- SEO：主質問への回答、記事範囲、タイトル・メタと本文の整合。
- 読者 / E-E-A-T：必要情報、条件・根拠、事実と考察の区別。
- 独自性 / 非定型性：主題内での比較・判断・具体的説明の価値。補足の量やコメント数で評価しない。
- UX / 内容構成：必要な情報への到達、章・表・FAQ・内部リンク・CTAの役割と関連性。完成HTMLのH2一覧を確認し、記事の流れ、各章を読む理由、見出しと本文の約束、検索意図・情報の探しやすさをコピーが妨げていないかを審査する。同じ見出し型が続く場合は、章の役割や論点の違いを把握できるかで判断する。文法・語尾・コピーの好みは日本語審査と重複採点しない。

### Pass And Return Rules

- 総合95点以上かつ各観点90点以上、AI Search And Answer Qualityの回答品質ゲート合格を条件とする。4観点は等重みで計算し、点数と指摘を対応させる。
- 主質問への回答漏れ、事実誤認・創作、根拠の不足、高リスク法務表現、確定メタの欠落・不一致は点数にかかわらず不合格。
- briefの範囲外の説明・不要な補足が主題を押しのける場合は不合格。補足質問の必要性も点検し、対応表に書いてあるだけで採用を正当化しない。Shopify Relevanceもこの担当が判定する。
- 初心者が判断できる内容かは確認するが、表現の問題は日本語担当へ返す。重大な日本語の見逃しを見つけた場合は日本語ゲートを再開する。意味不変ならeditor、内容・構成・主張の変更ならwriterへ戻し、Gate Lifecycle And Draft Exceptionsに従う。
- 共通要件の確認は該当するArticle Requirementsを参照し、同じ表層表現を重複採点しない。

### Output

`drafts/<handle>-review.md` に総合点、各点と根拠、合否、修正指示、良い点、対象SHA-256、回答品質ゲート6項目を保存する。UX / 内容構成の根拠にH2一覧確認の結果を含める。範囲外・削除候補と残す条件は修正指示へ含め、別の台帳を増やさない。

## Agent: `legal-reviewer`

### Role

品質審査合格後の記事を、日本の広告・表示関連法と著作権の観点から審査する公開前ゲート。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md`
- `drafts/<handle>-review.md` の合格結果（現在のHTMLとSHA-256が一致すること）

### Tasks

1. 景品表示法、ステマ規制、薬機法、特定商取引法、著作権、商標、個人情報のリスクを確認する
2. 断定、保証、最上級、比較表示、出典不明の数値、翻訳転載を検出する
3. 各指摘に該当箇所、具体的リスク、根拠、代替表現を示す。該当する主張の訂正・限定・削除を優先し、無関係な注意事項や一般免責の追加で代替しない
4. 法令や運用が変化しうる場合は官公庁などの一次情報で最新性を確認する

### Output

`drafts/<handle>-legal-review.md` に保存し、以下を返す。

- 総合点
- 高・中・低別のリスク
- 合否
- 不合格時の具体的な修正指示
- 審査したHTMLのSHA-256（総合審査の対象と同じ原稿であることを確認してから採点する）

### Constraints

- 95点以上かつ高リスクゼロで合格
- 本文は編集しない
- 最終的な法的判断は人間が行う

## Component: `article-validator`

### Role

エージェントの目視審査ではなく、`scripts/article_validator.py` でHTMLを決定論的に検査する。

### Checks

- HTMLの基本構造、見出しIDの重複、TOCリンクとの一致
- JSON-LDの構文と必須値
- JSON-LDに`Article`ノードがあり、`Article.description`に空欄・仮値ではない確定メタディスクリプションが入っていること
- FAQがまとめの直前にあること
- FAQ質問が `Q.` で始まり、3〜5問あること
- H2「この記事でわかること」と4〜6項目のリストがあること
- 最終更新日と著者表記があること。監修者は任意とし、著者と同じ人物の重複表示を避け、別人の場合は確認根拠を審査すること
- 禁止ダッシュなど、決定論的に判定できる日本語ルール
- 導入文が220〜380字の目安から外れる場合、固定的な導入構文、同一表現の過剰反復は警告として報告すること
- 見出しが宣言した件数と配下の明示的な番号付き項目数の不一致、番号付き見出しやリストの不自然な開始番号・欠番・重複・形式混在は警告として報告すること。別セクションからの意図的な継続やネストを決定論的に区別できない場合は不合格にしない
- `【要記入...】`、`<!-- 要確認 -->`、禁止プレースホルダ
- 公開済み記事一覧に存在しない内部リンク
- テンプレートのCSS枠が維持されていること

### Constraints

- 検査失敗時は `pre-publish-checker` と `article-publisher` に進まない
- 本文は編集しない
- 日本語の自然さ、概念の同一性、言い換えの妥当性、見出しの吸引力は機械判定せず、`japanese-editor` と `japanese-quality-reviewer` が文脈を見て判断する。定型表現や見出し型の反復を機械検出する場合も確認用の警告にとどめ、単語数・語尾だけで不合格にしない

### Metadata And Delivery Checks

- ブリーフの機械検証用メタデータと、すべてのArticle.descriptionが完全一致すること
- 本文の最終更新日は実在する暦日であること。確定したdateModifiedは本文の日付とJST基準で一致し、datePublishedがあればdateModified以前であること
- 下書きモードでは既定の公開用トークンを許す。通常モードではJSON-LDのPAGE_URL・DATE_*・BLOG_NAME・BLOG_URLの残存、無効な日付・URLを不合格とする
- authorを記載する場合はPerson/Organizationと名前を確認する。著者であるという事実やリンク先の妥当性はエージェントが審査する
- `--source` 指定時はJSON-LDを除いた原稿との完全一致を検査する。これはJSON-LD変更の意味的な妥当性やAIへの掲載を保証する検査ではない

## Component: `Shopify Input Preparation`

Shopify下書きの明示依頼時だけ、Drive保存・readback後にメインの実行主体が行う。

1. 元原稿 `drafts/<handle>.html` と日本語・総合・法務審査、Drive記録のSHA-256を照合する。元原稿を変更せず `drafts/<handle>-shopify.html` へコピーする
2. コピーのJSON-LDだけを確定する。PAGE_URLは確認したドメイン・ブログhandle・記事handleから作る予定URL、BLOG_NAME/BLOG_URLは確認済みの投稿先とする。dateModifiedは本文の実際の最終更新日をISO8601で記載する
3. 新規未公開記事のdatePublishedは省略し、作業日を公開日として入れない。既存公開記事では確認済みの実際の公開日を保持する。人間が公開する際に実際の公開日を設定・確認すべきことを引き継ぐ
4. 確定メタ、本文、CSS、見出し、リンクは変更しない。authorの追加・訂正など審査未実施の意味変更が必要ならwriterへ戻し、該当するゲートとDrive保存を再実行する
5. `python3 scripts/article_validator.py drafts/<handle>-shopify.html --brief drafts/<handle>-brief.md --source drafts/<handle>.html` を実行する。JSON-LD差分、値の根拠、元原稿とコピーそれぞれのSHA-256、検査結果を `drafts/<handle>-pre-publish.md` へ記録する
6. pre-publish-checkerは元原稿の審査結果と、投入用コピーの差分・通常モード検査を確認する。publisherは合格したコピーをそのままbodyへ渡す。直前にコピーのSHA-256と通常モード検査を再確認し、変更があれば再審査する

## Agent: `drive-draft-saver`

### Role

品質・法務・機械検証を通過した記事を、指定Google DriveフォルダへGoogle Docの下書きとして保存し、保存結果をreadbackする。Google Drive上の文書を人間との受け渡し正本にする。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `drafts/<handle>-japanese-review.md` の合格結果
- `drafts/<handle>-review.md` の合格結果
- `drafts/<handle>-legal-review.md` の合格結果
- `python3 scripts/article_validator.py --allow-draft-placeholders drafts/<handle>.html` の合格結果
- Google Drive Draft Folder ID: `1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee`
- 保存モード: `new_article`（既定）または `reviewed_human_draft`

### Tasks

1. 日本語品質レビューに記録されたHTMLのSHA-256が現在のHTMLと一致することを確認する。一致しなければ保存しない
   総合品質・法務レビューのSHA-256と合格、回答品質ゲート、日本語審査の用語・概念確認表も確認する。公開用JSON-LDトークンは下書きで許容するが、未確認事実・要記入事項は未解決として扱う
2. ブリーフから確定タイトルを取得し、`new_article` は `[下書き] <記事タイトル>`、`reviewed_human_draft` は `[レビュー済み] <記事タイトル>` のGoogle Docを指定フォルダに新規作成する
3. HTMLの本文をGoogle Docs向けに変換し、見出し、段落、リスト、表、リンクを可能な範囲で保持する。CSS、JSON-LD、公開用プレースホルダはGoogle Doc本文へ混在させない
4. 記事本文の `【要記入...】`、`【要確認...】`、`【内部リンク要記入...】`、`<!-- 要確認... -->` と審査記録の未解決事項を確認する。残る場合はGoogle Docの先頭に明示し、保存記録を `needs_human_input` とする。Shopify下書き工程へは進めない
5. 作成後、返されたURL、file ID、MIME typeを記録する
6. Google Docsコネクターで作成済み文書をreadbackし、タイトル、フォルダ、本文冒頭、主要見出し、リンクの保存を確認する

### Output

`drafts/<handle>-drive.md` に以下を保存し、要約を返す。

- 保存状態（`passed` / `needs_human_input` / `failed`）
- Google Doc URL、file ID、MIME type、保存先フォルダID
- readbackしたタイトル、本文冒頭、主要見出し、リンク確認結果
- 照合したHTMLのSHA-256
- 未解決事項とShopify下書き工程へ進める可否

### Constraints

- 既存のGoogle Drive文書を上書きしない
- 保存またはreadbackに失敗した場合は `failed` とし、Shopify工程へ進まない
- `needs_human_input` の文書は人間確認用の下書きとして保存してよいが、`pre-publish-checker` と `article-publisher` は起動しない
- Google Drive接続・認証がない場合は、その時点で停止して必要な接続を報告する

## Agent: `pre-publish-checker`

### Role

Shopify投入直前に、記事HTMLと関連メモを最終確認する。公開事故、創作、未確認リンク、JSON-LD不備、残プレースホルダを防ぐためのゲート。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-shopify.html` と `drafts/<handle>-pre-publish.md` の準備記録
- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md`（必須）
- `drafts/<handle>-assets.md` があれば参照する
- `drafts/<handle>-japanese-review.md` の合格結果
- `drafts/<handle>-review.md` と `drafts/<handle>-legal-review.md` の合格結果
- `article-validator` の合格結果
- `drafts/<handle>-drive.md` の `passed` 結果（Google Drive URL・file ID・readback結果を含む）

### Tasks

1. 投入用コピーに `【要記入: ...】`、`<!-- 要確認 -->`、未置換プレースホルダが残っていないことを確認する。審査済み元原稿の公開用JSON-LDトークンはコピーの確定値と照合する
2. ブリーフに確定メタディスクリプションが1つあり、空欄・仮値・未解決プレースホルダを含まないことを確認する。さらにJSON-LDの`Article.description`と完全一致することを確認する
3. FAQがまとめ直前にあるか確認する
4. 数字タイトルと本文項目数が一致しているか確認する
5. 著者情報、必要な場合の別人の監修者情報、最終更新日、出典、CTA、内部リンク案、図解案の扱いを確認する
6. 自動公開につながる設定がないか確認する
7. `article-validator` が合格済みか確認する
8. `drafts/<handle>-drive.md` が `passed` で、Google Drive保存・readbackが完了しているか確認する
9. `drafts/<handle>-japanese-review.md` と総合品質・法務レビューが合格済みで、記録されたHTMLのSHA-256が審査済み元原稿と一致するか確認する
10. Shopify投入仕様として、確定メタディスクリプションを`global.description_tag` / `single_line_text_field`に設定し、`summary`では代替しないことを確認する
11. 「Shopify Input Preparation」のJSON-LD差分と根拠を確認する。投入用コピーと元原稿の本文同一性、コピーに対する通常モード検査、回答品質ゲート6項目の合格を確認し、両HTMLのSHA-256と合否をpre-publish記録へ追記する

### Output

合否、Shopify下書き作成へ進めるか、Shopifyへ渡す確定メタディスクリプションを返す。不合格の場合は修正箇所を優先度順に示す。

### Constraints

- 本文を書き換えない
- 不合格の場合は `article-publisher` に進めない
- 公開可否ではなく、下書き作成に進めるかだけを判定する
- メタディスクリプションの欠落・不一致があれば不合格とする

## Agent: `article-publisher`

### Role

合格済み記事を Shopify ブログへ下書きとして保存する。

### Inputs

- `drafts/<handle>-shopify.html`（投入用コピー）と `drafts/<handle>.html`（審査済み原稿）
- `drafts/<handle>-brief.md`
- `pre-publish-checker` の合格結果
- `article-validator` の合格結果
- `drafts/<handle>-drive.md` の `passed` 結果

### Tasks

1. ブリーフからタイトル、handle、確定メタディスクリプション、タグ、投稿先ブログを取得する。確定メタディスクリプションが空、仮値、複数案、またはJSON-LDの`Article.description`と不一致なら停止する
2. `drafts/<handle>-pre-publish.md` の合格と投入用コピーのSHA-256を確認し、`python3 scripts/article_validator.py drafts/<handle>-shopify.html --brief drafts/<handle>-brief.md --source drafts/<handle>.html` を再実行する。合格したコピーを変更せずbodyへ渡す。著者は確認済みの場合だけ設定し、監修者から推定しない
3. Shopify Admin GraphQL のスキーマを確認する
4. GraphQL を検証してから mutation を実行する
5. `isPublished: false`で記事を作成し、確定メタディスクリプションを`metafields`の`global.description_tag`（type: `single_line_text_field`）へ必ず設定する。`summary`は代替にしない
6. コネクター経由でもShopify CLI経由でも、mutation実行前に実際のqueryとvariablesを`scripts/shopify_publish_guard.py`で検査し、`allow`の場合だけ実行する
7. 作成直後に別queryで`global.description_tag { type value }`と`isPublished`をreadbackし、ブリーフとの完全一致、type、`isPublished: false`を確認する
8. 欠落・不一致なら、`isPublished: false`と`global.description_tag`だけを明示した`articleUpdate`で1回だけ修復して再readbackする。それでも一致しなければ`failed`とする
9. guardへはJSON入力 `{"tool_input":{"query":"実際のmutation","variables":{}}}` を標準入力で渡し、出力の `hookSpecificOutput.permissionDecision` が `allow` であることを確認する。終了コード0だけでは許可を意味しない。hookの自動起動に依存せずCLIでも同じ検査を行う

### Output

作成後、下書きURL、投稿先ブログ、タイトル、保存したMeta description、readback結果、要確認点を返し、`drafts/<handle>-shopify.md`へ記録する。

### Constraints

- 自動公開は禁止
- 推測で GraphQL フィールド名を決めない
- 実行前に何を下書き作成するか要約して伝える
- `pre-publish-checker` が不合格の場合は実行しない
- `article-validator` が不合格または未実行の場合は実行しない
- `drafts/<handle>-drive.md` がない、または `passed` でない場合は実行しない
- ShopifyからのreadbackでMeta descriptionと`isPublished: false`を確認できない限り、下書き保存完了と報告しない
- mutationガードは単一の明示的なmutationを対象に、各記事の実際の入力を個別に検査する。未対応構文・欠落変数・公開日時`publishedAt`の指定は拒否する。CLIでも同じガードを実行し、GraphQLの構文・型は別途Shopifyスキーマで確認する

## Workflow: `new-article`

これはCodexの記事制作フロー。Codexはこの順序で記事制作を進める。
中央指揮を担うのはサブエージェントではなく、この指示を実行するCodex自身（メインの実行主体）である。通常依頼ではGoogle Drive下書き保存・readbackまでを自動実行する。

### Input

- キーワード、または記事テーマ
- 任意で投稿先ブログ

### Steps

1. キーワードが未指定なら `keyword-strategist` を実行し、最有力候補を1つ決める。投稿先ブログが未指定ならメインが主題から選び、キーワードとともに設計へ渡す
2. `article-designer` を実行し、`drafts/<handle>-brief.md` を作る
3. `fact-checker` を実行し、`drafts/<handle>-sources.md` を作る
4. `article-writer` を実行し、`drafts/<handle>.html` を作る
5. `fact-checker (post-write)` を実行し、完成HTMLの主張、数値、比較、引用を出典メモと照合する
6. 図解・画像などの素材設計が必要な場合だけ `content-asset-planner` を実行する
7. `japanese-editor` を実行し、読者に見えるテキストを自然な日本語へ整える
8. `japanese-quality-reviewer` を実行し、`drafts/<handle>-japanese-review.md` に保存する。総合95点以上かつ全観点90点以上を合格条件とする
9. 日本語品質が不合格なら、意味を変えない文章調整は `japanese-editor`、タイトル・メタ・構成・主張の修正は `article-writer` に差し戻す。`article-writer` が編集した場合は必ず5、7、8を再実行し、`japanese-editor` だけが編集した場合も8を再実行する。最大3周とする
10. 日本語品質合格後に `article-reviewer` を1回起動してSEO、読者/E-E-A-T、独自性/非定型性、UX/内容構成の4観点をレビューし、`drafts/<handle>-review.md` に保存する。総合95点以上かつ4観点すべて90点以上を合格条件とする
11. 品質レビュー不合格時は、意味不変の表現・局所編集なら `japanese-editor` に戻して7、8、10を、内容・構成・主張の変更なら `article-writer` に戻して5、7、8、10を再実行する。素材への影響も確認し、最大3周とする
12. 品質合格後に `legal-reviewer` を実行し、`drafts/<handle>-legal-review.md` に保存する。95点未満または高リスクがあれば `article-writer` に差し戻し、5、7、8、10、12を必ず再実行する。最大3周とする
13. `article-validator` を `python3 scripts/article_validator.py --allow-draft-placeholders drafts/<handle>.html` で実行する。構造、TOC、JSON-LD、CSS、内部リンク、日本語の決定論的ルールの検証に失敗した場合は修正し、影響した品質ゲートから再実行する
14. `drive-draft-saver` を実行し、指定Google Driveフォルダへ `[下書き] <記事タイトル>` のGoogle Docとして保存・readbackする。通常依頼での自動実行はここまでとする
15. Shopify下書き作成を明示依頼された場合だけ、`drafts/<handle>-drive.md` が `passed` であることを確認し、「Shopify Input Preparation」に従って投入用コピーの値確定・通常モード検査を完了してから `pre-publish-checker` を実行する。確定メタディスクリプションとJSON-LDの完全一致も合格条件にする
16. `pre-publish-checker` 合格後、`article-publisher` を実行し、Shopify に `isPublished: false` の下書きとして保存する。確定メタディスクリプションを`global.description_tag`へ設定し、別queryのreadbackで値・型・下書き状態を確認する
17. Google Drive URL、Shopify下書きURL（作成した場合のみ）、Shopifyへ保存したMeta description、readback結果、要確認点、`【要記入: ...】` の残件を報告する

### Stop Conditions

- 日本語品質、総合品質、法務のいずれかが最大3周しても合格しない場合は停止して残課題を報告する
- 日本語品質・総合品質・法務・validatorが不合格なら後工程を止め、「Gate Lifecycle And Draft Exceptions」に従って差し戻す。上限到達、必要な根拠の欠如、接続不足など修正不能な場合はタスクを停止する
- 指定Google Driveフォルダへの保存とreadbackが完了しない場合は、Google Drive下書き作成として失敗を報告し、Shopifyへ進まない
- `drive-draft-saver` が `needs_human_input` の場合はGoogle Drive URLと未解決事項を報告して停止し、Shopifyへ進まない
- `company-facts.md` がなくても一般論と確認済み出典で書ける場合は続行し、SOLSTAR固有情報は `【要記入: ...】` として残す
- `company-facts.md` やキーデータが不足し、記事の主張そのものが成立しない場合は停止して不足を報告する
- `pre-publish-checker` が不合格ならShopify下書き保存に進まず、修正点を報告する
- 確定メタディスクリプションが欠落・仮値・不一致、またはShopify readbackで`global.description_tag`を確認できない場合は停止する
- Shopify / Google Drive の接続や認証が不足している場合は、その時点で止めて必要な接続を報告する

### Output Expectations

- 設計だけで止まらず、通常はGoogle Drive下書き保存・readbackまで自動で進める
- Shopify下書き保存は、ユーザーが明示的に依頼した場合だけ実施する
- ただし公開はしない
- 各段階で主要な成果物パスを明示する
- 迷った場合はSEOテクニックより読者体験を優先する

## Workflow: `review-human-draft`

人間ライターが執筆したGoogle Drive上の記事をレビューし、修正済み原稿を同フォルダへ保存する。Shopify下書き作成はユーザーが明示した場合だけ行う。

### Input

- ユーザーが指定した個別のGoogle DocsまたはDriveファイルURL
- 任意で投稿先ブログ

### Steps

1. 指定URLからファイルID、MIME type、タイトルを取得し、対象ファイルを固定する
2. Google DocsならDocsコネクターで本文・見出し・表・リンクを読み、原本の現在内容を取得する
3. `human-draft-reviewer` が検索意図、構成、SEO、E-E-A-T、事実、独自性、日本語、CTAをレビューし、`drafts/<handle>-human-review.md` と `drafts/<handle>-brief.md` を作る。新規記事と同じ主質問・記事範囲、質問対応表・用語計画・機械検証用メタデータを必須とする
4. `fact-checker (pre-write)` でsourcesを作成してから、`article-writer` を人間原稿の改稿モードで実行する。原文の有用な内容と筆者の意図を保持しながら `article-template.html` に統合して `drafts/<handle>.html` を作る
5. `fact-checker (post-write)`、必要時の `content-asset-planner`、`japanese-editor` を実行する
6. `japanese-quality-reviewer`、`article-reviewer`、`legal-reviewer`、`article-validator`（`--allow-draft-placeholders`）の順でゲートを通す。Rewrite後は「Gate Lifecycle And Draft Exceptions」に従い `fact-checker (post-write)` から法務・validatorまで再実行し、差し戻しは各最大3周とする
7. `drive-draft-saver` を `reviewed_human_draft` モードで実行し、レビュー済み原稿を指定フォルダへ `[レビュー済み] <記事タイトル>` として別ファイル保存・readbackする
8. Shopify下書き作成を明示依頼された場合だけ、Drive保存記録が `passed` であることを確認し、「Shopify Input Preparation」に従って投入用コピーの値確定・通常モード検査を完了する。Drive保存URL、記事タイトル、handle、投稿先ブログ、残課題をユーザーへ要約してから `pre-publish-checker` を実行する
9. Shopify下書き作成を明示依頼され、全ゲートに合格した場合に限り、`article-publisher` がShopifyへ `isPublished: false` で下書き作成する
10. Google Driveのレビュー済みURLと、作成した場合だけShopify管理URLを報告する

### Stop Conditions

- 個別記事URLが指定されていない場合は、フォルダ内の記事を推測で選ばず停止する
- URL先を取得できない、または対象ファイルを一意に固定できない場合は停止する
- Google Driveへのレビュー済み版保存・readbackが完了しない場合はShopifyへ進まない
- `【要記入...】`、未確認事実、重大なレビュー指摘、法務高リスク、validatorエラーが残る場合はShopifyへ進まない
- Shopifyへの反映は下書きのみとし、公開操作は行わない

## Workflow: `review-search-performance`

人間が公開した記事について、依頼時にメインの実行主体が行う読み取り専用の評価。新規記事の下書き保存とは別の工程とし、定期実行の設定・自動公開・本番設定変更は行わない。

### Input

- 対象の公開記事URLまたはhandle（複数可）、任意の評価期間・比較期間
- 対象記事のbrief、sources、利用可能なSearch Console・Bing Webmaster Tools・アクセス解析の資料
- 日付指定がなければ、取得できる直近の確定28日間とその直前28日間を運用上の比較期間とし、取得範囲と時間帯を記録する。仕様上取得できない指標は推定しない

### Steps

1. 対象URL・公開状態・記事を固定する。下書きや対象不明のURLは分析せず対象の指定を求める
2. サイト取得と検索登録を点検する。HTTP応答、robots.txt、CDN等による取得制限、noindex・スニペット制御、canonical、主要本文の取得可否、内部リンク、公開ページと構造化データの人物・主題・日付の整合を確認する。取得不能・管理権限不足は `unverified` と記録し、問題なしと判定しない
   - Search Consoleの「Search generative AI」設定を確認し、対象プロパティ、設定値（参加・除外・親から継承）、継承元と実効値、確認日時を同じ評価記録へ残す。初期設定が参加であることを理由に、対象サイトも参加済みと推定しない。確認できない場合は `unverified` とし、除外・継承の解消は人間の管理担当への提案にする。通常検索への掲載、生成AI検索への参加、Google-Extended等によるモデル学習の制御を混同せず、このワークフローで設定を変更しない
3. 各サービスの最新公式資料で計測できる範囲を確認する。Search Consoleの「Generative AI performance report (Search)」を確認対象にし、取得できた生成AI検索の表示回数、Bingの引用、通常検索の順位・クリック、参照元別流入・問い合わせ成果を別の列で記録する。データ源・期間・単位・抽出条件・公式資料URLと確認日を残す。欠測は `unavailable` とし、ゼロや推定値に置き換えない
   - 専用レポートの取得可否、対象機能、集計単位（プロパティ・ページ等）、ページ・国・日付・端末・検索種別の利用可能な切り口、確定値か暫定値かを確認する。レポートが表示されない理由を表示回数不足・除外設定・権限不足等のいずれかと推定で断定しない
   - 表示回数を引用数やクリック数と同一視せず、専用レポートにないAI別クリック・CTR・順位は通常検索の値から算出しない。通常の検索パフォーマンスレポートとの対象範囲の重なりを確認し、生成AI表示回数を単純加算しない。比較時は期間・集計単位・検索種別・タイムゾーンをそろえ、そろえられない差は明記する
   - エクスポート時の欠測表記と数値への変換を公式資料・画面表示と照合する。画面の「~」「-」がダウンロードで0になる場合も観測ゼロへ置き換えず、元の欠測・非数値の状態を記録する。由来を確認できない0は欠測との区別が未確認である旨を残す
4. AI回答を確認できる場合はbriefの主な質問を使い、サービス・モデル（表示される場合）・質問文・日時・言語/地域・回答記録・引用URL・誤引用/条件脱落を記録する。確認できない場合は未実施とする。少数の試行から全体の引用率や順位を推定しない
5. 前期間との差を確認し、観測事実・原因仮説・推奨対応を分ける。引用数や表示数の変化だけで売上効果や因果関係を断定しない。重大な誤情報、巡回障害、回答不足を優先して改善案を作る
6. `drafts/<handle>-search-performance.md` に結果、未確認事項、改稿候補と担当、次回確認の目安を保存する。既存記事の改善はarticle-designer、用語問題はjapanese-editor、事実問題はfact-checker、新規テーマはkeyword-strategist、サイト設定は人間の管理担当への作業案として記録する

### Output And Follow-up

- 記録の必須列は `対象URL / 評価・比較期間 / データ源 / 指標・単位 / 値または欠測理由 / 観測事実 / 仮説 / 推奨対応 / 担当 / 優先度 / 次回確認目安`
- briefの対応表に戻す質問IDと修正理由を明記する。次の設計・改稿時に参照し、同じ問題の再発を確認する
- 接続がない場合も公開ページなど確認できた範囲の評価を保存し、必要な資料・接続を明記する。未確認項目があれば全体を合格とはしない
- このワークフロー単独では本文・Drive・Shopify・robots設定を変更しない。改稿も依頼されている場合は通常の品質ゲートを通してDriveの別下書きまで進める。Shopify下書きは明示依頼時だけ、公開は人間が行う
- 公開直後の取得可否確認と、その後の定期確認を引き継ぎ事項とする。次回日付の記載は予約実行を意味しない

## How To Ask Codex

- `new-article を "Shopify 越境EC 始め方" で実行して`
- `Marketing向けに、価格設定 心理学の記事を最初から下書き作成まで進めて`
- `キーワード未定なので keyword-strategist から始めて`
- `review-search-performance を <公開記事URL> で実行して`
