# 公開済み記事一覧（内部リンク・重複回避の正本）

SOLSTAR Shopifyブログの記事マスター。**内部リンクの実URL確定**と**新規KWの重複回避**に使う。
URL形式: `https://www.solstar.co.jp/blogs/<blog-handle>/<article-handle>`（本文中の内部リンクは相対パス `/blogs/<blog-handle>/<article-handle>` でよい）。

- **最終更新: 2026-06-08（Shopify Admin API のライブ取得で照合）**
- `status: 公開` の記事のみ内部リンク先に使う。`status: 下書き` の記事へはリンクしない（URLが存在しないため）。
- 更新方法: Shopify Admin API で各ブログの `articles` を取得し直し、この表を上書きする（GraphQLは `articles(first: 50, reverse: true)`。`sortKey` は非対応）。

ブログのgid: Shopify=`gid://shopify/Blog/96499761374`（handle: `shopify`） / Marketing=`gid://shopify/Blog/96528236766`（handle: `marketing`） / Branding=`gid://shopify/Blog/103031931102`（handle: `branding`）

---

## Shopifyブログ（handle: shopify）

| handle | タイトル | タグ | 公開日 | status | テーマ／内部リンク用途 |
|---|---|---|---|---|---|
| shopify-store-setup-for-beginners | Shopifyの始め方｜開設・初期設定から公開まで全手順【初心者向け】 | 全般 | 2026-06-05 | 公開 | 始め方・初期設定。初心者導線の受け皿 |
| shopify-theme-ranking | Shopifyテーマ ランキング2026｜無料・有料を忖度なし比較【業種別の選び方】 | 全般/比較 | 2026-06-03 | 公開 | テーマ選び。デザイン・構築系から誘導 |
| shopify-plan-cost-simulation | Shopify料金プランは月商で選ぶ｜損益分岐点で見る最安プラン早見表 | 全般/費用相場 | 2026-06-02 | 公開 | Basic〜Advancedの料金プラン選び。費用系の中核 |
| shopify-cost-simulation-enterprise | Shopify Plusの費用は？決済手数料を年商別にシミュレーション | Plus/全般/費用相場 | 2026-06-01 | 公開 | Plus・エンタープライズ費用。Plus検討者向け |
| shopify-dropshipping | 【2026年版】Shopify ドロップシッピングとPODの始め方を徹底解説 | 全般 | 2026-05-28 | 公開 | ドロップシッピング・POD。物販モデル系 |
| shopify-development-company-how-to-choose | Shopify制作会社の選び方｜費用相場と失敗しない7つの基準 | 全般/費用相場 | 2026-05-27 | 公開 | 制作会社の選び方。費用・依頼系のハブ |
| makeshop-vs-shopify-which-to-choose | 【2026年版】MakeShopとShopifyの比較 | 全般/比較 | 2025-09-14 | 公開 | カート比較。比較・乗り換え系から誘導 |
| shopify-reviews-expert-analysis | Shopifyの評判は本当に良い？リアルな口コミと専門家の分析 | 全般 | 2025-09-14 | 公開 | 評判・口コミ。検討初期の不安解消 |
| shopify-success-case-18-analysis-ec-site-construction-hints | Shopify成功事例18選を徹底分析 | 全般 | 2025-09-13 | 公開 | 成功事例。説得・権威付けの参照先 |
| shopify-partner-what-they-do-costs-how-to-choose | Shopifyパートナーとは？費用・選び方 | 全般 | 2025-09-13 | 公開 | パートナー制度。依頼・外注系 |
| shopify-introduction-how-to-start-ec-site-for-beginners | Shopifyとは？ECサイト構築の全てを徹底解説【2026年最新版・初心者向け】 | 全般 | 2025-09-11 | 公開 | Shopify基礎。用語・概要の参照先 |
| shopify-freelance-cost-tips | ShopifyでECサイト構築をフリーランスに依頼する前に。費用相場と注意点 | 費用相場 | 2025-09-11 | 公開 | フリーランス依頼費用。費用・外注系 |
| cost-of-building-a-shopify-store | Shopifyを利用したECサイト構築費用を徹底解説 | 費用相場 | 2025-09-08 | 公開 | 構築費用の総合。費用系のハブ |
| netshop-osusume-comparison | ネットショップおすすめ4社を比較｜無料〜本格まで失敗しない選び方【2026】 | 全般/比較 | — | 下書き | ※2026-06-08作成（Article gid 665213042910）。総合比較（Shopify/BASE/STORES/MakeShop）。公開後はstatus更新。1対1の makeshop-vs-shopify と相互補完。内部リンク先にするのは公開後 |
| pros-and-cons-about-shopify | Shopifyのメリットとデメリット | 全般 | — | 下書き | ※未公開。内部リンク先にしない |
| shopify-shipping-methods-japan | Shopifyの配送方法｜国内配送アプリまで解説 | 全般/配送/アプリ/運用 | — | 下書き | ※2026-06-28作成（Article gid 665314459870）。Shopify標準配送設定と日本国内配送アプリ。公開後はstatus更新。内部リンク先にするのは公開後 |

## Marketingブログ（handle: marketing）

| handle | タイトル | タグ | 公開日 | status | テーマ／内部リンク用途 |
|---|---|---|---|---|---|
| ecommerce-psychology | ECサイトの購買心理学｜CVRを上げる売れる導線9の法則【保存版】 | UIUX/心理学 | 2026-05-31 | 公開 | 購買心理・導線。心理系のハブ |
| ec-pricing-techniques | 価格設定テクニック12選｜心理学でECの売上を伸ばす実装術 | UIUX/価格/心理学 | 2026-05-28 | 公開 | 価格設定の実装術。価格心理系 |
| physiology-about-price | 価格の心理学：安く感じさせる価格設定のテクニックとは？ | UIUX/価格/心理学 | 2025-02-18 | 公開 | 自社最強の価格心理ページ。価格・心理系は必ずここへ内部リンク |
| json-ld-shopify-seo | 【徹底解説】JSON-LDとは？SEO効果とShopifyでの実装・設定方法まで完全ガイド | SEO | 2026-02-02 | 公開 | 構造化データ・SEO。技術SEO系 |
| brand-concept-how-to | ブランドコンセプトの作り方｜初心者でも今日書ける5ステップ【EC実践】 | 全般/心理学 | — | 下書き | ※未公開。内部リンク先にしない |

## Brandingブログ（handle: branding）

| handle | タイトル | タグ | 公開日 | status | テーマ／内部リンク用途 |
|---|---|---|---|---|---|
| what-is-brand-beginner | ブランドとは？高級品だけではない意味を初心者向けに解説 | 全般/心理学 | — | 下書き | ※2026-06-29作成（Article gid 665316917470）。ブランディング基礎の入門記事。公開後はstatus更新。内部リンク先にするのは公開後 |

---

## 重複回避・カニバリ注意（新規KW選定・設計時）

- **費用系**は記事が密集（`cost-of-building-a-shopify-store` / `shopify-freelance-cost-tips` / `shopify-development-company-how-to-choose` / `shopify-plan-cost-simulation` / `shopify-cost-simulation-enterprise`）。新規の費用記事は切り口（対象規模・依頼形態・プラン）を明確に分け、既存と相互リンクする。
- **料金プラン費用**は `shopify-plan-cost-simulation`（Basic〜Advanced・損益分岐点）と `shopify-cost-simulation-enterprise`（Plus）で住み分け済み。1億円未満の費用は前者・構築費用記事へ寄せる。
- **価格・心理系**は `physiology-about-price`（最強ページ）を中心に `ec-pricing-techniques` `ecommerce-psychology` がある。新規価格心理記事は必ず `physiology-about-price` へ内部リンクし、テーマを重複させない（[[kolenda-pricing-article-series]] 方針）。
- **比較系**は `makeshop-vs-shopify-which-to-choose`（GSCで順位下落中＝強化対象）。他カート比較を足すなら相互リンク。
