from pathlib import Path
import json,re,subprocess,shutil
base=Path('drafts/physiology-about-price')
sp=Path(str(base)+'-drive-sync-readback.json');s=json.loads(sp.read_text());sha=s['htmlSHA256'];c=s['verification']
s['verification'].update({'contentAndLinksMatch':True,'revisionStableAtCompletion':True,'validator':'passed','validatorWarnings':['「重要です」が6回出現（ユーザー編集を保持）'],'googleDocModifiedByAgent':False})
sp.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
model=json.loads(subprocess.check_output(['python3','tmp/price-review-doc-model.py',str(base.with_suffix('.html'))]))
brief=Path(str(base)+'-brief.md');t=brief.read_text()
outline='\n'.join(('  - ' if z['role']!='HEADING_1' else '- ')+z['text'] for z in model['blocks'] if z['kind']=='paragraph' and z['role'].startswith('HEADING') and z['text']!='目次')
t=re.sub(r'## H2/H3の設計\n.*?(?=## 実務コメント)',lambda m:'## H2/H3の設計\n\n'+outline+'\n\n上記はGoogle Docsの最新本文に合わせた見出し。普通段落で貼られた小見出し3件をHTML見出しとして整形。\n\n',t,flags=re.S)
t=t.replace('- /blogs/branding/what-is-brand-beginner: 名声価格とブランド価値。','- /blogs/branding/what-is-brand-beginner: 今回のユーザー編集により本文から削除。')
t=t.replace('- 既存の端数価格・アンカリング・近接・類似画像を必要性と本文の整合を確認して維持。未作成画像を入れない。','- 最新Google Docsに合わせて既存画像3点を削除。現在の本文画像は0点。')
t+='\n## 追加同期（'+s['syncedAt']+'）\n\n第1章後半・第2章の8施策・第3章を同期。編集コメント3件は `physiology-about-price-user-edit-notes.md` へ保存。タイトル・確定メタ・URLは維持。本文の新たな主張・章間の整合は再審査未実施。以前の設計判断・審査履歴と現稿が異なる場合は、最新本文と同期記録を参照する。\n'
brief.write_text(t)
for suffix in ['-japanese-review.md','-review.md','-legal-review.md','-sources.md']:
 p=Path(str(base)+suffix);t=p.read_text();t=re.sub(r'(> 現在のHTML SHA-256: `)[^`]+',lambda m:m[1]+sha,t,count=1);p.write_text(t)
p=Path(str(base)+'-assets.md');p.write_text('> 最新同期: Google Docsで画像3点が削除され、現在のHTML画像は0点。以下の画像記録は旧稿の履歴。図を参照する残文は `physiology-about-price-user-edit-notes.md` に記録。\n\n'+p.read_text())
record=f'''# Google Drive正本からのローカル同期記録

- 同期状態: passed_with_documented_format_normalization
- 品質審査状態: not_re_reviewed_after_user_edit
- 同期日時: {s['syncedAt']}
- Google Doc URL: https://docs.google.com/document/d/{s['documentId']}/edit
- file ID: {s['documentId']}
- MIME type: {s['metadata']['mime_type']}
- フォルダID: 1nY8LitmaNw6v8ZPb2tVxb2bVK4pK3Wee
- Google Docs最終更新日時: {s['metadata']['modified_time']}
- revision ID: {s['revisionId']}
- HTML SHA-256: {sha}
- 掲載URL: https://www.solstar.co.jp/blogs/marketing/physiology-about-price
- 同期前の全ローカル成果物: {s['archive']}

## 反映内容

第1章後半、第2章8施策、第3章の追加・変更を同期。画像3点とブランド関連記事リンク1件の削除を反映。本文と重複しない編集コメント3件は別メモへ原文保存し、コメント中の代替見出し案は自動採用していない。タブ区切りの表2点をHTML表へ戻し、箇条書き・小見出し・Markdown強調を整形。目次の第3章文言を本文見出しに合わせた。本文の価格例や主張は改稿せず保持。

## 確認結果

- 本文ブロック {c['paragraphs']}件（タイトル・見出し・箇条書きを含む）、見出し{c['headings']}件、表{c['tables']}点・{c['cells']}セル、画像0点、リンク{c['links']}件。
- 元の全内容はreadback JSONに保持。コメントの分離、表の復元、目次更新、強調記号のHTML変換を除き、本文文字列の一致を確認。
- CSSは最新article-templateと完全一致、JSON-LD・タイトル・メタ・URLは不変。
- article-validator: PASS。文体警告「重要です」が6回は記録し、ユーザー文を維持。
- 完了時にGoogle Docsのrevision不変を再取得して確認。

## 関連記録

- 最新readback: `drafts/physiology-about-price-drive-sync-readback.json`
- 編集コメント・残件: `drafts/physiology-about-price-user-edit-notes.md`

画像削除後の図参照文、施策区分と第4章の対応、新しい例・心理効果の主張は次の校閲対象として記録。今回の依頼はローカル同期であり、日本語・総合品質・法務・事実確認の再審査は未実施。旧審査と旧PDFは現稿の合格証明として使用しない。Google Docs書き込み、別Doc作成、Shopify反映、公開は未実施。
'''
for suffix in ['-drive.md','-sync.md']:Path(str(base)+suffix).write_text(record)
shutil.copy2('tmp/price-user-sync-round2/document-text.md',str(base)+'-drive-source-text.md')
print('Updated brief, sync records, source text, review notices and assets record.')
