import { readFile, writeFile } from "node:fs/promises";

const htmlPath = new URL("../../drafts/ec-site-project-failure-causes.html", import.meta.url);
const outputPath = new URL("./ec-site-project-failure-causes-article-create-variables.json", import.meta.url);
const updateOutputPath = new URL("./ec-site-project-failure-causes-article-update-variables.json", import.meta.url);
const body = await readFile(htmlPath, "utf8");
const description = "ECサイトプロジェクトが失敗する3つの原因を、商品の需要調査不足、ブランド力不足による価格競争、他人任せの運用から解説。売上目標やKPI、中止基準の決め方も紹介します。";

const payload = {
  article: {
    blogId: "gid://shopify/Blog/96528236766",
    title: "ECサイトプロジェクトはなぜ失敗する？3つの原因と防止策",
    author: { name: "島袋隼" },
    handle: "ec-site-project-failure-causes",
    body,
    summary: description,
    tags: ["EC運営", "事業計画", "マーケティング", "プロジェクト管理"],
    isPublished: false,
    metafields: [
      {
        namespace: "global",
        key: "description_tag",
        type: "single_line_text_field",
        value: description,
      },
    ],
  },
};

await writeFile(outputPath, `${JSON.stringify(payload)}\n`, "utf8");

const updatePayload = {
  id: "gid://shopify/Article/665615859934",
  article: {
    body,
    isPublished: false,
    metafields: [
      {
        namespace: "global",
        key: "description_tag",
        type: "single_line_text_field",
        value: description,
      },
    ],
  },
};

await writeFile(updateOutputPath, `${JSON.stringify(updatePayload)}\n`, "utf8");
