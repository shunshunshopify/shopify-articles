#!/usr/bin/env python3
"""
Google Search Console から検索クエリのパフォーマンスデータを取得する。

サービスアカウント認証。事前準備:
  1. GCPでSearch Console APIを有効化し、サービスアカウントのJSONキーを取得
  2. そのサービスアカウントのメールをGSCのユーザーに追加（制限付きでOK）
  3. JSONキーを .secrets/gsc-service-account.json に配置

使い方:
  ./.venv/bin/python scripts/gsc_fetch.py \
      --property "sc-domain:solstar.co.jp" \
      --days 90 \
      --out data/gsc-queries.csv

property は GSC のプロパティ識別子:
  - ドメインプロパティ: "sc-domain:solstar.co.jp"
  - URLプレフィックス : "https://www.solstar.co.jp/"
"""
import argparse
import csv
import datetime as dt
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
DEFAULT_KEY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".secrets", "gsc-service-account.json",
)


def fetch(service, property_uri, start, end, dimensions, row_limit=25000):
    """searchAnalytics.query をページングしながら全件取得する。"""
    rows = []
    start_row = 0
    while True:
        body = {
            "startDate": start,
            "endDate": end,
            "dimensions": dimensions,
            "rowLimit": min(row_limit, 25000),
            "startRow": start_row,
        }
        resp = service.searchanalytics().query(
            siteUrl=property_uri, body=body
        ).execute()
        batch = resp.get("rows", [])
        rows.extend(batch)
        if len(batch) < body["rowLimit"]:
            break
        start_row += len(batch)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--property", required=True, help='例: "sc-domain:solstar.co.jp"')
    ap.add_argument("--days", type=int, default=90, help="過去何日分（既定90）")
    ap.add_argument("--out", default="data/gsc-queries.csv")
    ap.add_argument("--key", default=DEFAULT_KEY, help="サービスアカウントJSONのパス")
    args = ap.parse_args()

    if not os.path.exists(args.key):
        sys.exit(
            f"[エラー] 認証キーが見つかりません: {args.key}\n"
            "  GSCのサービスアカウントJSONを .secrets/gsc-service-account.json に配置してください。"
        )

    creds = service_account.Credentials.from_service_account_file(
        args.key, scopes=SCOPES
    )
    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    end = dt.date.today()
    start = end - dt.timedelta(days=args.days)
    s, e = start.isoformat(), end.isoformat()

    # クエリ単位（KW候補の母集団）
    query_rows = fetch(service, args.property, s, e, ["query"])
    # クエリ×ページ単位（どの記事/ページで拾えているか）
    page_rows = fetch(service, args.property, s, e, ["query", "page"])

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["query", "clicks", "impressions", "ctr", "position"])
        for r in sorted(query_rows, key=lambda x: x.get("impressions", 0), reverse=True):
            k = r["keys"][0]
            w.writerow([
                k, r.get("clicks", 0), r.get("impressions", 0),
                round(r.get("ctr", 0) * 100, 2), round(r.get("position", 0), 1),
            ])

    page_out = args.out.replace(".csv", "-by-page.csv")
    with open(page_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["query", "page", "clicks", "impressions", "ctr", "position"])
        for r in sorted(page_rows, key=lambda x: x.get("impressions", 0), reverse=True):
            q, p = r["keys"]
            w.writerow([
                q, p, r.get("clicks", 0), r.get("impressions", 0),
                round(r.get("ctr", 0) * 100, 2), round(r.get("position", 0), 1),
            ])

    print(f"取得期間: {s} 〜 {e}")
    print(f"クエリ件数: {len(query_rows)}  → {args.out}")
    print(f"クエリ×ページ件数: {len(page_rows)}  → {page_out}")


if __name__ == "__main__":
    main()
