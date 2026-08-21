import { readFile, writeFile } from "node:fs/promises";

const htmlPath = new URL("../../drafts/qoo10-vs-shopify-cosmetics.html", import.meta.url);
const outputPath = new URL("./qoo10-vs-shopify-cosmetics-article-create-variables.json", import.meta.url);
const queryPath = new URL("./qoo10-vs-shopify-cosmetics-article-create.graphql", import.meta.url);
const guardInputPath = new URL("./qoo10-vs-shopify-cosmetics-guard-input.json", import.meta.url);
const body = await readFile(htmlPath, "utf8");
const query = await readFile(queryPath, "utf8");
const description = "Qoo10とShopifyをコスメ事業者向けに比較。出店費用・販売手数料・メガ割・集客・顧客データの違いと、月商別試算、ブランド認知や粗利に応じた選び方、併用戦略を解説します。";

const payload = {
  article: {
    blogId: "gid://shopify/Blog/96528236766",
    title: "Qoo10とShopifyを比較｜コスメECはどちらを選ぶ？",
    author: { name: "島袋隼" },
    handle: "qoo10-vs-shopify-cosmetics",
    body,
    summary: description,
    tags: ["全般", "比較", "費用相場", "コスメEC"],
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
await writeFile(
  guardInputPath,
  `${JSON.stringify({
    tool_name: "shopify store execute",
    tool_input: { query, variables: payload },
  })}\n`,
  "utf8",
);
