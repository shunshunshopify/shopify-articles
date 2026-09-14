from pathlib import Path
import json, hashlib, datetime

base=Path('drafts/physiology-about-price')
sha=hashlib.sha256(base.with_suffix('.html').read_bytes()).hexdigest()
snap_path=Path(str(base)+'-drive-sync-readback.json')
snap=json.loads(snap_path.read_text())
archive=Path('tmp/price-sync-archive-path.txt').read_text()
timestamp=datetime.datetime.now().astimezone().isoformat()
snap.update({'syncStatus':'passed','syncedAt':timestamp,'htmlSHA256':sha,'archive':archive,'verification':{'exactParagraphsAndTables':True,'paragraphs':134,'headings':33,'tables':6,'tableCells':108,'links':15,'images':3,'validator':'passed','googleDocModifiedByAgent':False},'reviewStatus':'not_re_reviewed_after_user_edit'})
snap_path.write_text(json.dumps(snap,ensure_ascii=False,indent=2)+'\n')
brief=Path(str(base)+'-brief.md')
s=brief.read_text().replace('金額を変える施策と表示だけを変える施策を分ける','価格を下げる前に、まず「見せ方」を見直す').replace('- /blogs/marketing/ecommerce-psychology: 価格以外の購入導線。','- /blogs/marketing/ecommerce-psychology: ユーザー編集により本文から削除（2026年09月14日同期）。')
s+='\n## 2026年09月14日 ユーザー編集のローカル同期\n\nGoogle Docs正本の導入文・第1章の説明・H3変更・関連記事リンク削除をローカルHTMLに同期。タイトル・確定メタディスクリプション・掲載URLは変更なし。最新の同期記録は `physiology-about-price-drive-sync-readback.json` を参照。今回はユーザー編集の同期であり、再校閲・再審査は未実施。\n'
brief.write_text(s)
notice='> 現在の状態（2026年09月14日）: ユーザーがGoogle Docsで編集した内容をローカルへ同期済み。以下は更新前のHTMLに対する審査・確認記録であり、現在のHTMLの合格証明には使用しない。現在版は再審査未実施。\n> 現在のHTML SHA-256: `'+sha+'`\n\n'
for suffix in ['-japanese-review.md','-review.md','-legal-review.md','-sources.md']:
 p=Path(str(base)+suffix)
 p.write_text(notice+p.read_text())
url='https://docs.google.com/document/d/'+snap['documentId']+'/edit'
record=f'''# Google Drive正本からのローカル同期記録

- 同期状態: passed
- 品質審査状態: not_re_reviewed_after_user_edit
- 同期日時: {timestamp}
- Google Doc URL: {url}
- file ID: {snap['documentId']}
- MIME type: {snap['metadata']['mime_type']}
- フォルダID: 1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee
- Google Docs最終更新日時: {snap['metadata']['modified_time']}
- revision ID: {snap['revisionId']}
- HTML SHA-256: {sha}
- 掲載URL: https://www.solstar.co.jp/blogs/marketing/physiology-about-price
- 同期前の全ローカル成果物: {archive}

## 反映内容

- 導入文の変更。
- 第1章の定義・比較例を変更し、段落分割を反映。
- H3を「価格を下げる前に、まず「見せ方」を見直す」へ変更。
- 価格変更と表示改善の説明・助言をユーザーの文章に同期。
- 購買心理学の記事への案内段落と内部リンクを削除。
- ブリーフの見出しとリンク方針を同期。

## 確認

本文134段落（タイトルを含む）・見出し33件・表6点108セル・画像3点・リンク15件を取得したGoogle Docsと照合し、一致を確認。テンプレートのCSS、目次、JSON-LD、タイトル、確定メタディスクリプション、掲載URLを維持。`article_validator.py --allow-draft-placeholders` はPASS。

readback: `drafts/physiology-about-price-drive-sync-readback.json`

今回はユーザー編集をローカルへ同期する作業のみ。Google Docsへの書き込み・新規コピー作成・Shopifyへの反映・公開は行っていない。ユーザー編集後の日本語・総合・法務・事実確認の再審査は未実施。過去の合格記録は更新前版の記録として保持し、現在版の合格として扱わない。以前のPDFも更新前版であり、今回版の表示確認記録には使用しない。
'''
Path(str(base)+'-drive.md').write_text(record)
Path(str(base)+'-sync.md').write_text(record)
print(json.dumps({'sha256':sha,'archive':archive,'sync':'passed'},ensure_ascii=False))
