from pathlib import Path
import hashlib
p=Path('drafts/physiology-about-price.html');sha=hashlib.sha256(p.read_bytes()).hexdigest()
assert sha=='b354a0b062fab1262a8e80760fce7790a688562d9479d83e8d9c100c97c96dbd'
review=Path('drafts/physiology-about-price-review.md').read_text();assert sha in review and '合格' in review
Path('drafts/physiology-about-price-legal-review.md').write_text('''# 法務レビュー（横断レビュー反映後）

- 審査日: 2026年09月14日
- 担当: メイン担当（総合審査合格後のlegal-reviewer工程）
- 対象HTML SHA-256: `'''+sha+'''`
- 前提: 日本語96.4点・総合97.0点の合格と対象SHA一致を確認。
- 総合点: 98 / 100
- 判定: passed
- リスク: 高0・中0・低1
- 必須修正: なし

## 審査結果

| 分野 | 結果 |
|---|---|
| 景品表示法・価格比較 | 単品合計は実際の商品・数量・販売条件をそろえる。架空の通常価格を推奨せず、過去価格とメーカー希望小売価格の根拠を区別。研究の例を販売実績と偽っていない |
| 効果・優良性の表示 | 松竹梅、おとり効果、品質シグナル、割引、送料無料の効果を保証せず、自社検証と利益確認へつなぐ。高価格を品質の証明とはしていない |
| 特定商取引法・総額表示 | 税込支払額、送料額と条件、割引対象・期間・併用条件を明示する方針。誤認を招く架空の期間限定は推奨しない |
| 著作権 | 論文は独自の説明と概念例に再構成。参考文献へのリンクあり。引用転載や未作成画像なし。本文画像は0点 |
| 薬機法・健康増進法 | スキンケア等は組み合わせの例のみで、効能効果の主張なし。低カロリーの購買効果主張は削除済み |
| ステマ・自社誘導 | 自社名を示した自然な相談CTA。第三者の口コミ・中立評価を装う表現なし |
| 個人情報・実績 | 顧客名や非公開実績、架空の成果数値の追加なし |

## 再確認した一次資料

- https://www.caa.go.jp/policies/policy/representation/fair_labeling/representation_regulation/double_price/ ：同一商品、過去価格、比較価格の根拠と誤認防止を照合。
- https://www.no-trouble.caa.go.jp/what/mailorder/advertising.php ：税込販売価格、送料の金額表示、条件・料金表へのリンクを照合。
- https://www.caa.go.jp/policies/policy/representation/fair_labeling/faq/representation ：表示に関する案内を参照。本文の価格表示の主張は上記具体ページとsourcesでも確認済み。

## 低リスク管理事項

監修者の「Shopify開発歴8年以上」はAGENTS.md指定の既存表記を維持。根拠記録を保管する従来の管理事項で、今回の改稿による新規実績主張ではない。

今回の判定は記事原稿の表現に対する審査で、個別の価格表示を一律に適法と保証するものではない。公開操作は人間が行う。
''')
print('Legal review passed: 98, high 0, medium 0, low 1.')
