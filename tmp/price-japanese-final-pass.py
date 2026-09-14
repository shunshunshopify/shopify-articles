from pathlib import Path
import hashlib
p=Path('drafts/physiology-about-price.html');s=p.read_text()
s=s.replace('これが「左端桁効果」です。研究では、','これが「左端桁効果」です。</p>\n<p>研究では、')
s=s.replace('この送料無料になる基準額は「送料無料閾値」と呼ばれることもあります。','この基準額を「送料無料閾値（いきち）」と呼ぶこともあります。')
s=s.replace('施策を選ぶときは、購入者が購入をためらう理由を考え、自社で改善できる箇所を探します。','施策を選ぶときは、購入をためらう理由を考え、自社で改善できる箇所を探します。')
s=s.replace('一方で、高級感や職人性を重視するブランドでは、','一方で、高級感や職人の技を重視するブランドでは、')
p.write_text(s)
Path('drafts/physiology-about-price-edit-log.md').write_text('''# 横断レビュー反映後の日本語編集記録

- 担当: メイン担当（japanese-editor工程）
- 対象: physiology-about-price.html
- 第1パス: 段落間の因果、8施策の役割、冒頭から選定・採算・検証までの流れを通読。重複は改稿工程で集約済み。端数価格の研究補足を段落分割。
- 第2パス: 主述、用語、語尾、見出し、FAQ、CTAを確認。「職人性」を「職人の技」へ平易化、「送料無料閾値」に読みを補足。「購入者が購入」の重なりを解消。価格効果の限定と比較条件は保持。
- 購入者に呼称統一。松竹梅・おとり効果・バンドル販売の分類と利益指標を本文・表で統一。
- CSS、URL、メタ、参照URL、数値、表の比較関係は不変。
- HTML SHA-256: '''+hashlib.sha256(p.read_bytes()).hexdigest()+'\n')
print(hashlib.sha256(p.read_bytes()).hexdigest())
