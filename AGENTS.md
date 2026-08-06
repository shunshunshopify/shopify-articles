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
- 事実、数値、実績、口コミ、導入事例、支援実績は追加・変更・創作しない
- 不足情報は埋めず、「追加すると E-E-A-T 向上につながる内容」として提案する
- 記事内容と矛盾する情報を追加しない
- `article-template.html` の CSS / TOC / JSON-LD の枠は改変しない
- 記事生成・Rewriteのたびに、その時点の `article-template.html` を読み直す。過去記事や既存下書きの `<style>` を流用せず、最新版テンプレートの `<style>` をそのまま使う
- 既存記事との重複を避ける
- 海外記事や研究は参考にしてよいが、翻訳転載はしない
- 検索上位記事の単なるリライトではなく、SOLSTARならではの価値を加える
- SEOだけでなく、読者体験（UX）を最優先にする
- 2026年時点の SEO / AIO / E-E-A-T を意識する
- AIでも書ける一般論だけの記事にしない
- スマホでも読みやすいよう、1段落は3〜4行程度を目安にする
- 公開前提で進めず、まずは設計・執筆・レビュー用成果物を保存する

## Pipeline

`keyword-strategist` -> `article-designer` -> `fact-checker (pre-write)` -> `article-writer` -> `fact-checker (post-write)` -> `content-asset-planner (必要時)` -> `japanese-editor` -> `japanese-quality-reviewer` -> `article-reviewer` -> `legal-reviewer` -> `article-validator` -> `drive-draft-saver`（Google Drive保存・readback）-> （Shopify下書きを明示依頼された場合のみ）`pre-publish-checker` -> `article-publisher`

必要なキーワードがすでに決まっている場合は `keyword-strategist` を省略してよい。通常の `new-article` は `drive-draft-saver` によるGoogle Drive保存・readbackまで自動で実施する。Shopify下書き保存は明示依頼時だけ実施し、その場合に限り `pre-publish-checker` と `article-publisher` を起動する。

## Source Of Truth

- Codex運用の判断基準、工程順、責務分担、停止条件はこの `AGENTS.md` を唯一の正本とする
- 周辺ファイルは、この `AGENTS.md` に書かれた契約を実装するための補助資料または実装詳細として扱う
- 周辺ファイルの記述が `AGENTS.md` と矛盾する場合は、Codexは `AGENTS.md` を優先する

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
  `fact-checker` の成果物。あれば `article-writer` `content-asset-planner` `pre-publish-checker` は必ず参照
- `drafts/<handle>-assets.md`
  `content-asset-planner` の成果物。`pre-publish-checker` と公開前の人間確認で使う
- `drafts/<handle>-japanese-review.md`
  `japanese-quality-reviewer` の成果物。自然な日本語、段落論理、用語、リズム、文体統一の合格記録として使う
- `drafts/<handle>-drive.md`
  `drive-draft-saver` の保存記録。Google Doc URL、file ID、MIME type、readback結果、未解決事項を記録する。Shopify下書き工程はこの記録の合格結果を必須入力とする

## Dependency Rules

- Codexが最初に読むべきファイルは `AGENTS.md` のみでよい
- その後は、実行する工程に必要な依存だけを追加で読む
- `article-template.html` は `article-writer` 着手前に必ず読む
- `theme-css/solstar-article.css` と `article-template.html` のStyle整合は `article-validator` が検査する。不一致時は記事生成を続けず、先にテンプレートを最新版へ同期する
- `company-facts.md` は SOLSTAR固有情報を書く必要が出た時点で必ず読む
- `data/published-articles.md` は `keyword-strategist` の重複確認、`article-designer` の設計着手前、`article-writer` の内部リンク確定前に必ず読む

## Runtime Contracts

### Input Contracts

- `keyword-strategist` はテーマ未定またはキーワード未指定で起動してよい
- `article-designer` はキーワードと投稿先ブログが決まってから起動する
- `fact-checker` は `drafts/<handle>-brief.md` 生成後に起動する
- `article-writer` は `drafts/<handle>-brief.md` を必須入力とし、`drafts/<handle>-sources.md` があれば必須参照とする
- Google Drive保存前は、`article-writer`、`fact-checker (post-write)`、必要時の`content-asset-planner`、`japanese-editor`、`japanese-quality-reviewer`、`article-reviewer`、`legal-reviewer`、`article-validator` をすべて完了させる
- `drive-draft-saver` は `article-validator` 合格後にのみ起動し、Google Driveへの保存とURL・file IDのreadbackを完了させる
- `pre-publish-checker` と `article-publisher` は、Shopify下書き作成を明示依頼された時点でのみ実行する
- `content-asset-planner` は `drafts/<handle>.html` 生成後、図解・画像などの素材設計が必要な場合だけ起動する
- `japanese-editor` は `drafts/<handle>.html` だけを編集対象にする
- `japanese-quality-reviewer` は `japanese-editor` 完了後に起動し、`drafts/<handle>.html` と `drafts/<handle>-brief.md` を必須入力とする
- `article-reviewer` は `drafts/<handle>.html` と `drafts/<handle>-brief.md` がそろってから起動する
- `legal-reviewer` は `article-reviewer` 合格後に起動する
- `article-validator` は `legal-reviewer` 合格後に `scripts/article_validator.py --allow-draft-placeholders` を実行する。Shopify下書き作成を明示依頼された場合は、`pre-publish-checker` の直前にプレースホルダを許可しない通常モードで再実行する
- `pre-publish-checker` は `drafts/<handle>.html` 完成後に起動する
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
- `pre-publish-checker` は合否と修正点を返すが、本文は編集しない
- `article-publisher` は Shopify に下書きを作成し、`global.description_tag`と`isPublished: false`をreadbackして、管理用URL・保存したMeta description・確認結果を`drafts/<handle>-shopify.md`へ記録する

### Fallback Contracts

- `company-facts.md` がない場合でも、一般論と確認済み出典だけで成立する記事なら続行してよい
- `company-facts.md` がないためにSOLSTAR固有情報が必要な主張を書けない場合は `【要記入: ...】` を残す
- 出典確認ができない主張は本文へ断定的に書かない
- Google Drive や Shopify に接続できない場合は、その工程で止めて必要な接続を報告する

## Files

- `article-template.html`: 記事HTMLテンプレート
- `drafts/`: 設計ブリーフ、記事HTML、候補メモの保存先
- `data/`: GSCエクスポートや関連データの保存先
- `company-facts.md`: SOLSTAR固有の実績・事例・料金の参照元。存在しない場合は創作せず `【要記入: ...】` を残す

## Article Requirements

### Reader First

- 読者ファーストで執筆する
- 主な読者は、技術者ではない経営者、事業責任者、EC・マーケティング担当者とする。専門知識や実装経験を前提にしない
- 検索意図に最短で答えられる構成を優先する
- SEOテクニックだけでなく、可読性、回遊性、理解しやすさを優先する

### Technical Depth

- 詳細さは保ちつつ、説明順は「経営・業務への影響 → 判断基準 → 次に取る行動 → 必要な場合だけ仕組みの補足」とする
- 読者の判断や行動に影響しない実装詳細、管理画面の細かな設定、API・データ構造・コードの説明は、検索意図が技術情報を求めている場合を除いて本文へ入れない
- 専門用語や略語は、使わなくても意味が変わらないなら平易な日本語へ置き換える。不可欠な場合は平易な説明を先に置き、正式名称を初出の丸カッコ内で補足する
- 出典が技術文書でも、その情報順や用語をそのまま本文へ持ち込まない。Non-technicalな読者が意思決定に使える粒度へ再構成する
- 詳細な仕組みを残す必要がある場合は、本文の主線から分けて短い補足、表、箇条書きにまとめる

### Shopify Relevance

- `article-designer` はテーマごとにShopify関連度を `直接関連` / `一部関連` / `非関連` の3段階で判定し、理由をブリーフへ記載する
- `直接関連` の記事だけ、検索意図に必要な範囲でShopifyの機能、仕様、プラン、アプリ、管理画面を解説する
- `一部関連` の記事では、読者の比較や判断に役立つ場合だけShopifyへ触れる。記事の主題よりShopifyの説明を前に出さない
- `非関連` の記事では、Shopifyで何ができるかを説明する見出し、FAQ、比較、CTAを追加しない。Shopify上のブログへ掲載すること自体は、本文でShopifyへ触れる理由にならない
- 内部リンクとCTAもテーマとの関連性を優先し、Shopify記事へのリンクやShopify構築相談へ無理につなげない

### Editorial Voice

- 記事全体を説明だけで均一にせず、代表者が読者へ直接助言するような、率直で温かい実務コメントを自然に入れる
- コメントは1〜2文の短い判断や助言とし、記事全体で2〜4か所を目安にする。見出しラベルや「島袋コメント」などの署名は付けない
- コメントでは、選び方の勘所、優先順位、陥りやすい迷い、無理なく続ける考え方を示す。くだけすぎた会話調、あおり、感情の演出は避ける
- コメントを実績や体験談のように見せない。「現場でよく見る」「支援経験では」などの経験主張は、`company-facts.md` か確認済み出典に根拠がある場合だけ使う
- 事実と意見を混同せず、コメント部分でも数値、成果、顧客反応を創作しない

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
2. 監修者情報
3. 導入文
4. H2「この記事でわかること」
5. 目次

監修者表記は次を基本形とする。

`最終更新日：YYYY年MM月DD日`

`※この記事は、Shopify開発歴8年以上の株式会社SOLSTAR代表取締役・島袋隼が監修しています。`

### Introduction

- 導入文は300文字程度を目安とする
- 読者の悩みや検索意図に触れる
- 結論を簡潔に伝える
- 本記事で扱う内容と切り口を示す
- 読了メリットと対象読者を示す
- 上位記事との差分や実務上の付加価値を示す。ただし「単に○○を紹介するだけでなく、△△まで解説します」などの固定構文を毎回使わず、記事内容に合う自然な文で表現する

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

- 一般論だけで終わらせず、SOLSTARとしての判断軸や実務視点を加える。ただし専門性をテクニカルな言葉の多さで表現しない
- 独自性は、事実に基づく考察、設計思想、運用視点、改善観点で出す
- 「なぜ有効か」「自社ならどう活かせるか」「次に何を考えるべきか」を補足する
- 存在しない実績、存在しない支援事例、架空の数値、断定できない支援実績は書かない

### Readability

- 文章だけを続けず、必要に応じて箇条書き、比較表、早見表、チェックリストを使う
- 出典・調査結果をもとに書く場合も、原文の情報順や分量に引っ張られず、まず読者が知りたい結論・要点を先に示してから、詳細な根拠・出典情報を続ける
- 情報量が多い部分（項目・手順・条件・数値などが3つ以上並ぶ場合）は、地の文で羅列せず箇条書きや表に変換する

### Japanese Language Quality

- SOLSTARの文体は、技術者ではないEC担当者・事業責任者・経営者に向けた、簡潔で落ち着きがあり、適度に人の判断が感じられる実務文とする
- 一文の短さだけを目的にせず、主語と述語、原因と結果、前後の段落の接続が自然に伝わることを優先する
- 「重要です」「必要があります」「まずは」「一方で」「〜ではなく、〜」など、便利な構文や語尾の反復を避ける
- 指示語の参照先、主語の省略、名詞化の連続、不自然な受動態、過剰な接続詞を確認する
- 専門用語は正確さを保ちつつ、想定読者に浸透していない場合は原則として平易な表現を本文の主語にする。正式名称が必要なときだけ初出で短く補足し、同じ概念の訳語は記事内で統一する
- タイトル、メタディスクリプション、見出し、本文、FAQ、アンカーテキスト、CTAの語調をそろえる
- 読者への過度な呼びかけ、断定、あおり、幼すぎる言い換えを避ける
- 流暢さを禁止語の機械的な回避だけで判断せず、意味の明瞭さ、情報密度、文章のリズムを総合して整える

### Word Choice And Expression

- 専門知識がない読者でも一度で意味を理解できる、やさしく自然な日本語を使う
- 中学2〜3年生でも理解できる漢字、単語、言い回しを基本とし、硬い熟語、抽象的な表現、回りくどい言い方は意味がすぐに伝わる言葉へ置き換える
- 文章をやさしくする際も、情報の正確さや専門性を失わない。幼い文章にせず、専門的な内容を分かりやすく伝える
- 一文に多くの内容を詰め込まず、できるだけ一つの内容に絞る。主語と結論の関係を明らかにする
- 漢字が連続する硬い表現は日常的な言葉へ置き換え、抽象語だけで済ませず具体的な行動や変化を書く
- 「〜することが可能です」は原則として「〜できます」と書く
- 「〜を実施します」は「〜を行います」または「〜します」と書く
- 「〜の向上につながります」と抽象的にまとめず、何がどう良くなるのかを書く
- 同じ意味を重ねたくどい文章を避ける
- Shopify、ECサイト、SEO、CVR、在庫連携、APIなど、専門用語を使うほうが正確で自然な場合は無理に言い換えない。読者が理解しにくい用語は初出で短く説明する
- 読者の判断に必要ない専門用語や横文字は使わず、専門用語の表記は記事内で統一する
- 言い換えは次の例を基準とし、文脈に合わせて具体的な言葉へ変える
  - 「購買行動を促進する」→「購入につなげる」
  - 「視認性を向上させる」→「見やすくする」
  - 「顧客との接点を創出する」→「お客様とつながる機会をつくる」
  - 「導入を検討する必要があります」→「導入するか確認します」
  - 「売上の最大化を図る」→「売上を伸ばす」
  - 「ユーザーの離脱を防止する」→「ページから離れるのを防ぐ」
  - 「運用負荷を軽減する」→「運用の手間を減らす」
  - 「情報を網羅的に掲載する」→「必要な情報をまとめて掲載する」
  - 「購入の意思決定を支援する」→「お客様が購入を判断しやすくする」
  - 「適切な導線を設計する」→「必要なページへ進みやすくする」
- 執筆後は、硬い表現、難しい漢字、不要な専門用語、長すぎる文が残っていないか見直し、意味を変えずに調整する

### FAQ

- FAQは記事末に設置する
- 配置は「まとめ」の直前を基本とする
- 各質問のH3見出しは必ず先頭に「Q.」を付ける（例: `<h3>Q. 〇〇はどのくらいですか？</h3>`）。回答本文に「A.」は付けない
- 3〜5問程度を目安にし、本文の補足になる内容を入れる
- 本文と重複しすぎる内容は避ける
- ロングテールの疑問や検索ユーザーの不安を意識する

### Sources And References

- 必要に応じて出典・参考文献を掲載する
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

- タイトル、メタ、本文の内容は一致しているか
- 確定メタディスクリプションが1つあり、JSON-LDの`Article.description`と完全一致しているか
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
- Non-technicalな経営者・担当者が、専門知識なしで結論、判断基準、次の行動を理解できるか
- 読者の判断に不要な実装詳細や、説明のない専門用語・略語が残っていないか
- Shopify関連度が `一部関連` または `非関連` の記事で、Shopifyの機能説明、FAQ、CTAを無理に追加していないか
- 根拠のある内容を踏まえた、短く自然な実務コメントが2〜4か所程度あり、記事がフラットな説明だけになっていないか
- 実績、数値、支援事例を創作していないか
- 最終更新日と監修者情報を記載したか
- CTAが自然につながっているか
- 主述のねじれ、指示語の曖昧さ、直訳調、不自然な受動態が残っていないか
- 同じ語尾・接続詞・対比構文が短い範囲で反復していないか
- タイトル、見出し、本文、FAQ、CTAの文体が統一されているか
- 中学2〜3年生でも理解できる言葉を基本とし、硬い熟語や抽象語を日常的で具体的な表現へ変えているか
- 専門用語は必要な範囲に絞られ、難しい用語には初出で短い説明があるか
- 長すぎる文、一文に複数の論点を詰め込んだ文、同じ意味を重ねた文が残っていないか

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

### Tasks

1. Ahrefs候補を確認し、ボリューム・難易度・意図を把握する
2. GSCデータから、伸びしろ・取りこぼし・既存露出の有無を確認する
3. 3C分析で、SOLSTARが勝てるかどうかを補正する
4. 既存記事と重複しない候補を優先順位付きで整理する
5. UXとE-E-A-Tの観点から、一般論に寄りにくいテーマを優先する

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

### Role

狙うキーワードを受け取り、検索上位記事を調査し、勝てる記事構成と差別化方針を設計する。

### Inputs

- 狙う検索キーワード
- 投稿先ブログ（`Shopify` / `Marketing` / `Branding`）

### Tasks

1. Web検索で上位記事を10件程度調べる
2. 必要に応じて本文を確認し、共通論点と不足論点を抽出する
3. 検索意図を `Know` / `Do` / `Buy` で整理する
4. 想定読者を明確化する
5. Shopify関連度を `直接関連` / `一部関連` / `非関連` で判定し、本文で触れる範囲を決める
6. Non-technicalな読者が理解できる説明順と用語の粒度で、SOLSTAR独自の切り口を組み合わせた H2 / H3 アウトラインを作る
7. 記事冒頭の統一構成、FAQ、内部リンク、図解提案に加え、短い実務コメントを入れる見出しと伝える助言まで設計する
8. `data/published-articles.md`（公開済み記事の正本）を読み、(a) このテーマと**カニバリ（重複）しないか**を確認し、(b) 本文から内部リンクすべき**関連する公開済み記事を2〜3本を目安に**選ぶ。`status: 公開` の記事のみ対象とし、Shopify記事を優先しない。関連する記事が少ない場合は本数を無理に満たさない

### Output

`drafts/<handle>-brief.md` に保存し、要約を返す。内容には以下を含める。

- **handle（URLスラッグ）**: 内容を表す半角英小文字ハイフン区切り。以降の全工程がこの handle をファイル名に使うため、設計工程で必ず確定する
- タイトル案3つ
- **確定メタディスクリプション**（80〜120字を目安に1つ。記事の主題、対象読者、読了メリットを含める）
- 想定読者と検索意図
- **Shopify関連度**: `直接関連` / `一部関連` / `非関連` の判定、理由、本文で触れる範囲
- H2 / H3 アウトライン
- 各見出しの要点
- 差別化ポイント
- **Non-technical向け編集方針**: 読者の判断に必要な内容、削る実装詳細、噛み砕く専門用語
- **実務コメント計画**: 2〜4か所を目安に、挿入する見出しと伝える判断・助言
- 推奨タグ
- 想定文字数
- FAQ案
- **内部リンク候補**: `data/published-articles.md` から選んだ関連公開済み記事2〜3本を目安に記載する（handle・相対URL・本文のどの見出しから張るか）。カニバリ懸念がある既存記事があればその注意も明記する。関連する記事が少ない場合は本数を無理に満たさず理由を書く
- 図解 / 画像提案と挿入位置

### Constraints

- 本文はまだ書かない
- 上位記事の焼き直しではなく、独自の付加価値を必ず設計する
- タイトルはキーワードを前半に含め、32文字前後を目安にする
- 数字タイトルの場合は、本文構成でもその数が担保できる設計にする
- H2「この記事でわかること」を前提に設計する
- H2だけで流れが分かり、H3で具体性が伝わる構成にする
- 目次が長くなりすぎないよう、表示すべき見出しを意識する
- 確定メタディスクリプションを空欄・仮値・複数案のまま後工程へ渡さない
- Shopify関連度が `非関連` の記事にShopifyの機能、仕様、プラン、アプリ、管理画面を説明する見出し・FAQ・CTAを設計しない

## Agent: `article-writer`

### Role

設計ブリーフをもとに、テンプレートに沿って本文HTMLを執筆する。

### Inputs

- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md` があれば必ず参照する
- 差し戻し時は `drafts/<handle>-japanese-review.md`、`drafts/<handle>-review.md`、`drafts/<handle>-legal-review.md` のうち該当する指摘

### Tasks

1. 初回執筆・Rewriteのたびに、その時点の `article-template.html` を読み直し、過去記事や既存下書きのStyleを流用せず、最新版のCSSを含む枠組みは変えずに本文だけ差し替える
2. ブリーフに沿って、最終更新日、監修者情報、導入文、H2「この記事でわかること」、本文、FAQ、まとめを書く
3. TOCアンカーと見出し `id` を一致させる
4. JSON-LD の `HEADLINE` を確定タイトルで、`DESCRIPTION` をブリーフの確定メタディスクリプションと完全に同じ文字列で埋める。空欄・仮値・別案は禁止する
5. `PAGE_URL` `DATE_*` `BLOG_NAME` `BLOG_URL` は公開工程用プレースホルダとして残す
6. 確認済みの出典は本文または参考文献として自然に入れる
7. 出典（`drafts/<handle>-sources.md`）から得た情報は、原文の順序や分量をそのまま反映せず、読者が知りたい結論を先に立ててから詳細・根拠を続ける形に再構成する
8. 項目・手順・条件・数値の比較など情報量が多い内容は、地の文の羅列にせず箇条書きや表にする
9. 説明順を「経営・業務への影響 → 判断基準 → 次に取る行動 → 必要な場合だけ仕組みの補足」とし、Non-technicalな読者の判断に不要な実装詳細を入れない
10. ブリーフのShopify関連度に従い、`非関連` の記事ではShopifyの機能説明、FAQ、CTAを追加しない
11. 代表者が読者へ直接助言するような短い実務コメントを、記事全体で2〜4か所を目安に自然に入れる。署名や専用ラベルは付けず、未確認の経験談は書かない
12. 執筆後に全文を見直し、硬い表現、難しい漢字、不要な専門用語、長すぎる文を、意味と正確さを保ったまま分かりやすく整える

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
- ブリーフに確定メタディスクリプションがない場合は執筆完了扱いにせず、`article-designer`へ差し戻す
- ブリーフにShopify関連度またはNon-technical向け編集方針がない場合は、主題と検索意図から補完してブリーフへ明記してから執筆し、Shopifyへ安易に寄せない

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

執筆済みHTMLの読者に見えるテキストを、意味と事実を変えず、日本人が自然に読める実務文へ編集する。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`

### Tasks

1. マクロ編集として、各セクションの結論、段落間の論理接続、指示語の参照先、情報の重複を確認する
2. ミクロ編集として、主述のねじれ、翻訳調、同じ語尾・構文の反復、不自然な受動態、冗長表現を整える
3. 本文に加え、見出し、FAQ質問、アンカーテキスト、CTAも、意味・SEO意図・リンク先を維持した範囲で自然な日本語へ整える
4. Non-technicalな読者に不要な専門用語・略語・実装目線の表現を、意味を変えない範囲で平易にする。削除や構成変更が必要なら `article-writer` へ差し戻す
5. ブリーフのShopify関連度と照合し、不要なShopify説明があれば `article-writer` へ差し戻す
6. 実務コメントの自然さを整えつつ、人の判断が感じられる表現を無機質な説明へ均質化しない
7. タイトルまたはメタディスクリプションに修正が必要な場合は本文を独断で変えず、`article-writer` への修正指示として報告する
8. 構成変更や主張変更が必要な問題は編集で隠さず、`article-writer` への差し戻し事項として報告する
9. 中学2〜3年生でも理解できる言葉を基本に、硬い熟語、抽象語、回りくどい表現を日常的で具体的な言葉へ整える。ただし、専門性と正確さは維持する
10. 一文に複数の内容が詰め込まれている場合は、HTML構造を変えない範囲で文を分ける。専門用語は必要性を確認し、難しい用語には初出で短い説明を加える

### Output

同じ `drafts/<handle>.html` に上書き保存し、変更箇所、主な編集観点、`article-writer` への差し戻し要否を報告する。

### Constraints

- HTMLタグ、見出し階層、CSS、JSON-LD構造、リンク先、出典を変えない
- 見出し文を変える場合は対応するTOC表示文も同じ文言へ同期し、アンカーIDは変えない
- 事実や数値を追加しない
- SEOキーワードと検索意図を削除・変更しない
- 監修者情報、最終更新日、FAQ位置、CTAの役割を変えない

## Agent: `japanese-quality-reviewer`

### Role

日本語編集後の記事を、流暢さ、論理、用語、リズム、文体統一の観点だけで独立審査する。SEOや法務との総合評価に埋もれさせず、日本語品質の専用ゲートを担う。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md` があれば参照する

### Review Axes

- 論理・段落構成（20%）
- 文の自然さ・主述（20%）
- 語彙・専門用語・訳語（15%）: 中学2〜3年生でも理解できる言葉を基本とした平易さ、必要な専門用語の初出説明、不要な実装用語の排除、表記の統一を含む
- リズム・語尾・構文の反復（15%）
- 明瞭さ・簡潔さ・情報密度（15%）: 一文一義、主語と結論の分かりやすさ、硬い熟語や抽象語を具体的な表現へ変えているかを含む
- SOLSTARの実務文としての語調（10%）: 落ち着きに加え、短い判断・助言に人の温度があるかも含む
- 見出し・FAQ・アンカーテキスト・CTAの統一（5%）

### Output

`drafts/<handle>-japanese-review.md` に次を保存する。本文は編集しない。

- 総合点と各観点の100点換算スコア
- 審査したHTMLのSHA-256
- 合否
- 重大度別の指摘
- 該当箇所、問題の理由、具体的な修正案
- `japanese-editor` と `article-writer` のどちらへ差し戻すべきか
- 良い点と維持すべき表現

### Constraints

- 総合95点以上かつ各観点90点以上で合格
- 主述の破綻、参照先不明の指示語、意味が変わる曖昧さ、未説明の難解な直訳語、記事全体の語調不統一が1件でもあれば点数にかかわらず不合格
- 主要な結論・判断基準・次の行動の理解に技術知識が必要な場合は不合格
- Shopify関連度が `非関連` なのにShopifyの機能説明・FAQ・CTAがある場合、または `一部関連` でShopify説明が主題を押しのけている場合は不合格
- 記事が無機質な説明だけで、読者の迷いに寄り添う短い判断・助言がない場合は合格にしない
- 禁止語の有無だけで採点せず、前後の文脈と読者の理解しやすさを根拠にする
- 不合格時は「どこを、なぜ、どう直すか」を具体化し、本文は書き換えない
- タイトル・メタの問題、構成変更、主張変更は `article-writer`、意味を変えない文章調整は `japanese-editor` へ差し戻す

## Agent: `article-reviewer`

### Role

完成記事を審査し、95点基準で合否判定する。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md` があれば参照する
- `drafts/<handle>-japanese-review.md` の合格結果
- 4観点（`SEO` / `E-E-A-T` / `独自性・非定型性` / `UX・可読性`）を1回でまとめて審査する

### Review Axes

- SEO観点
- 読者 / E-E-A-T 観点（Non-technicalな読者が自社への影響、判断基準、次の行動を理解できるかを含む）
- 独自性 / 非定型性観点（文章表層の流暢さは `japanese-quality-reviewer` の合格結果を前提とし、一般論の水増し、上位記事の焼き直し、実務コメントの自然さを中心に見る）
- UX / 可読性観点（不要な実装詳細や専門用語が本文の主線を妨げていないかを含む）

### Output

`drafts/<handle>-review.md` に保存し、次の見出しで固定する。本文は編集しない。

- 総合点
- 各観点の点数
- 合否
- 修正指示
- 良い点

### Constraints

- 総合95点以上かつ各観点90点以上で合格
- `japanese-quality-reviewer` が未実行または不合格なら審査を開始しない
- 現在のHTMLのSHA-256が `drafts/<handle>-japanese-review.md` の審査時SHA-256と一致しない場合は審査を開始しない
- 事実誤認、創作、検索意図の重大な不一致、高リスク法務表現が1件でもあれば点数にかかわらず不合格
- 不合格なら「どの見出しの何をどう直すか」まで具体化する
- 迷う用語はWeb検索で浸透度を確認してから指摘する
- レビュアー自身は本文を書き換えず、指摘に徹する
- 確定メタディスクリプションの欠落、空欄、仮値、またはブリーフとJSON-LDの`Article.description`の不一致は点数にかかわらず不合格とする
- Shopify関連度が `非関連` の記事にShopifyの機能説明・FAQ・CTAがある場合、または `一部関連` でShopify説明が主題より前に出ている場合は不合格とする
- 主要な結論・判断基準・次の行動が専門用語や実装知識を持つ読者にしか理解できない場合は不合格とする
- 次も必ず確認する: 冒頭構成、H2「この記事でわかること」、FAQ位置、数字タイトルとの整合、内部リンク提案、図解提案、出典の妥当性、創作の有無、CTAの自然さ、各セクションが結論先出しになっているか（出典情報を原文順のまま羅列していないか）、情報量が多い箇所が箇条書き・表に整理されているか

## Agent: `legal-reviewer`

### Role

品質審査合格後の記事を、日本の広告・表示関連法と著作権の観点から審査する公開前ゲート。

### Inputs

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md`

### Tasks

1. 景品表示法、ステマ規制、薬機法、特定商取引法、著作権、商標、個人情報のリスクを確認する
2. 断定、保証、最上級、比較表示、出典不明の数値、翻訳転載を検出する
3. 各指摘に該当箇所、リスク、根拠、安全な代替表現を示す
4. 法令や運用が変化しうる場合は官公庁などの一次情報で最新性を確認する

### Output

`drafts/<handle>-legal-review.md` に保存し、以下を返す。

- 総合点
- 高・中・低別のリスク
- 合否
- 不合格時の具体的な修正指示

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
- 最終更新日と、テンプレートで承認済みの監修者表記があること
- 禁止ダッシュなど、決定論的に判定できる日本語ルール
- 導入文が220〜380字の目安から外れる場合、固定的な導入構文、同一表現の過剰反復は警告として報告すること
- `【要記入...】`、`<!-- 要確認 -->`、禁止プレースホルダ
- 公開済み記事一覧に存在しない内部リンク
- テンプレートのCSS枠が維持されていること

### Constraints

- 検査失敗時は `pre-publish-checker` と `article-publisher` に進まない
- 本文は編集しない

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
2. ブリーフから確定タイトルを取得し、`new_article` は `[下書き] <記事タイトル>`、`reviewed_human_draft` は `[レビュー済み] <記事タイトル>` のGoogle Docを指定フォルダに新規作成する
3. HTMLの本文をGoogle Docs向けに変換し、見出し、段落、リスト、表、リンクを可能な範囲で保持する。CSS、JSON-LD、公開用プレースホルダはGoogle Doc本文へ混在させない
4. 記事本文に `【要記入...】` または `<!-- 要確認 -->` が残る場合は、Google Docの先頭に未解決事項として明示し、保存記録を `needs_human_input` とする。Shopify下書き工程へは進めない
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
- `drafts/<handle>-brief.md`
- `drafts/<handle>-sources.md` があれば参照する
- `drafts/<handle>-assets.md` があれば参照する
- `drafts/<handle>-japanese-review.md` の合格結果
- `article-validator` の合格結果
- `drafts/<handle>-drive.md` の `passed` 結果（Google Drive URL・file ID・readback結果を含む）

### Tasks

1. `【要記入: ...】`、`<!-- 要確認 -->`、未置換プレースホルダの残りを確認する
2. ブリーフに確定メタディスクリプションが1つあり、空欄・仮値・未解決プレースホルダを含まないことを確認する。さらにJSON-LDの`Article.description`と完全一致することを確認する
3. FAQがまとめ直前にあるか確認する
4. 数字タイトルと本文項目数が一致しているか確認する
5. 監修者情報、最終更新日、出典、CTA、内部リンク案、図解案の扱いを確認する
6. 自動公開につながる設定がないか確認する
7. `article-validator` が合格済みか確認する
8. `drafts/<handle>-drive.md` が `passed` で、Google Drive保存・readbackが完了しているか確認する
9. `drafts/<handle>-japanese-review.md` が合格済みで、記録されたHTMLのSHA-256が現在のHTMLと一致するか確認する
10. Shopify投入仕様として、確定メタディスクリプションを`global.description_tag` / `single_line_text_field`に設定し、`summary`では代替しないことを確認する

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

- `drafts/<handle>.html`
- `drafts/<handle>-brief.md`
- `pre-publish-checker` の合格結果
- `article-validator` の合格結果
- `drafts/<handle>-drive.md` の `passed` 結果

### Tasks

1. ブリーフからタイトル、handle、確定メタディスクリプション、タグ、投稿先ブログを取得する。確定メタディスクリプションが空、仮値、複数案、またはJSON-LDの`Article.description`と不一致なら停止する
2. HTML内の JSON-LD プレースホルダを確定値へ置換し、`Article.description`を確定メタディスクリプションと完全一致させる
3. Shopify Admin GraphQL のスキーマを確認する
4. GraphQL を検証してから mutation を実行する
5. `isPublished: false`で記事を作成し、確定メタディスクリプションを`metafields`の`global.description_tag`（type: `single_line_text_field`）へ必ず設定する。`summary`は代替にしない
6. コネクター経由でもShopify CLI経由でも、mutation実行前に実際のqueryとvariablesを`scripts/shopify_publish_guard.py`で検査し、`allow`の場合だけ実行する
7. 作成直後に別queryで`global.description_tag { type value }`と`isPublished`をreadbackし、ブリーフとの完全一致、type、`isPublished: false`を確認する
8. 欠落・不一致なら、`isPublished: false`と`global.description_tag`だけを明示した`articleUpdate`で1回だけ修復して再readbackする。それでも一致しなければ`failed`とする

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

## Workflow: `new-article`

これはCodexの記事制作フロー。Codexはこの順序で記事制作を進める。
中央指揮を担うのはサブエージェントではなく、この指示を実行するCodex自身（メインの実行主体）である。通常依頼ではGoogle Drive下書き保存・readbackまでを自動実行する。

### Input

- キーワード、または記事テーマ
- 任意で投稿先ブログ

### Steps

1. キーワードが未指定なら `keyword-strategist` を実行し、最有力候補を1つ決める
2. `article-designer` を実行し、`drafts/<handle>-brief.md` を作る
3. `fact-checker` を実行し、`drafts/<handle>-sources.md` を作る
4. `article-writer` を実行し、`drafts/<handle>.html` を作る
5. `fact-checker (post-write)` を実行し、完成HTMLの主張、数値、比較、引用を出典メモと照合する
6. 図解・画像などの素材設計が必要な場合だけ `content-asset-planner` を実行する
7. `japanese-editor` を実行し、読者に見えるテキストを自然な日本語へ整える
8. `japanese-quality-reviewer` を実行し、`drafts/<handle>-japanese-review.md` に保存する。総合95点以上かつ全観点90点以上を合格条件とする
9. 日本語品質が不合格なら、意味を変えない文章調整は `japanese-editor`、タイトル・メタ・構成・主張の修正は `article-writer` に差し戻す。`article-writer` が編集した場合は必ず5、7、8を再実行し、`japanese-editor` だけが編集した場合も8を再実行する。最大3周とする
10. 日本語品質合格後に `article-reviewer` を1回起動してSEO、読者/E-E-A-T、独自性/非定型性、UX/可読性の4観点をレビューし、`drafts/<handle>-review.md` に保存する。総合95点以上かつ4観点すべて90点以上を合格条件とする
11. 品質レビューが不合格または重大ブロッカーを検出した場合は `article-writer` に差し戻し、5、7、8、10を必ず再実行する。最大3周とする
12. 品質合格後に `legal-reviewer` を実行し、`drafts/<handle>-legal-review.md` に保存する。95点未満または高リスクがあれば `article-writer` に差し戻し、5、7、8、10、12を必ず再実行する。最大3周とする
13. `article-validator` を `python3 scripts/article_validator.py --allow-draft-placeholders drafts/<handle>.html` で実行する。構造、TOC、JSON-LD、CSS、内部リンク、日本語の決定論的ルールの検証に失敗した場合は修正し、影響した品質ゲートから再実行する
14. `drive-draft-saver` を実行し、指定Google Driveフォルダへ `[下書き] <記事タイトル>` のGoogle Docとして保存・readbackする。通常依頼での自動実行はここまでとする
15. Shopify下書き作成を明示依頼された場合だけ、`drafts/<handle>-drive.md` が `passed` であることを確認し、`python3 scripts/article_validator.py drafts/<handle>.html` を通常モードで再実行してから `pre-publish-checker` を実行する。確定メタディスクリプションとJSON-LDの完全一致も合格条件にする
16. `pre-publish-checker` 合格後、`article-publisher` を実行し、Shopify に `isPublished: false` の下書きとして保存する。確定メタディスクリプションを`global.description_tag`へ設定し、別queryのreadbackで値・型・下書き状態を確認する
17. Google Drive URL、Shopify下書きURL（作成した場合のみ）、Shopifyへ保存したMeta description、readback結果、要確認点、`【要記入: ...】` の残件を報告する

### Stop Conditions

- 日本語品質、総合品質、法務のいずれかが最大3周しても合格しない場合は停止して残課題を報告する
- 日本語品質または総合品質のいずれかの観点が90点未満、法務高リスクが残る、または `article-validator` が失敗した場合は停止する
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
3. `human-draft-reviewer` が検索意図、構成、SEO、E-E-A-T、事実、独自性、日本語、CTAをレビューし、`drafts/<handle>-human-review.md` と `drafts/<handle>-brief.md` を作る
4. `article-writer` を人間原稿の改稿モードで実行し、原文の有用な内容と筆者の意図を保持しながら `article-template.html` に統合して `drafts/<handle>.html` を作る
5. `fact-checker (post-write)`、必要時の `content-asset-planner`、`japanese-editor` を実行する
6. `japanese-quality-reviewer`、`article-reviewer`、`legal-reviewer`、`article-validator`（`--allow-draft-placeholders`）の順でゲートを通す。Rewrite後は `fact-checker (post-write)`、`japanese-editor`、`japanese-quality-reviewer`、`article-reviewer` を省略せず、差し戻しは各最大3周とする
7. `drive-draft-saver` を `reviewed_human_draft` モードで実行し、レビュー済み原稿を指定フォルダへ `[レビュー済み] <記事タイトル>` として別ファイル保存・readbackする
8. Shopify下書き作成を明示依頼された場合だけ、Drive保存記録が `passed` であることを確認し、プレースホルダを許可しない通常モードで `article-validator` を再実行する。Drive保存URL、記事タイトル、handle、投稿先ブログ、残課題をユーザーへ要約してから `pre-publish-checker` を実行する
9. Shopify下書き作成を明示依頼され、全ゲートに合格した場合に限り、`article-publisher` がShopifyへ `isPublished: false` で下書き作成する
10. Google Driveのレビュー済みURLと、作成した場合だけShopify管理URLを報告する

### Stop Conditions

- 個別記事URLが指定されていない場合は、フォルダ内の記事を推測で選ばず停止する
- URL先を取得できない、または対象ファイルを一意に固定できない場合は停止する
- Google Driveへのレビュー済み版保存・readbackが完了しない場合はShopifyへ進まない
- `【要記入...】`、未確認事実、重大なレビュー指摘、法務高リスク、validatorエラーが残る場合はShopifyへ進まない
- Shopifyへの反映は下書きのみとし、公開操作は行わない

## How To Ask Codex

- `new-article を "Shopify 越境EC 始め方" で実行して`
- `Marketing向けに、価格設定 心理学の記事を最初から下書き作成まで進めて`
- `キーワード未定なので keyword-strategist から始めて`
