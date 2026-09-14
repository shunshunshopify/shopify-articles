from pathlib import Path
import json,re,html,subprocess,hashlib,datetime,shutil

base=Path('drafts/physiology-about-price')
p=base.with_suffix('.html'); old=p.read_text()
snap=json.loads(Path('tmp/price-sync2-snapshot.json').read_text()); b=snap['blocks']
notes={56,75,76}
def esc(t):return html.escape(t,quote=False)
def rich(z):
 out=[]
 for run in z.get('runs',[]):
  t=esc(run['content'].rstrip('\n'));st=run.get('textStyle',{})
  if st.get('bold'):t='<strong>'+t+'</strong>'
  if st.get('italic'):t='<em>'+t+'</em>'
  if st.get('link',{}).get('url'):t='<a href="'+html.escape(st['link']['url'],quote=True)+'">'+t+'</a>'
  out.append(t)
 return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',''.join(out))
def table(rows):
 return '<div class="tbl-scroll"><table>\n<thead><tr>'+''.join('<th>'+esc(c)+'</th>' for c in rows[0])+'</tr></thead>\n<tbody>\n'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>\n' for row in rows[1:])+'</tbody></table></div>'
out=[];i=25;list_ranges={61:64,86:88,101:107,112:114,117:120}
while i<127:
 z=b[i]
 if i in notes:i+=1;continue
 if i in (42,49):
  end=i+4;out.append(table([v['text'].split('\t') for v in b[i:end]]));i=end;continue
 if i in list_ranges:
  end=list_ranges[i];out.append('<ul>\n'+''.join('<li>'+rich(v)+'</li>\n' for v in b[i:end])+'</ul>');i=end;continue
 if z['role']=='HEADING_1':
  num=z['text'].split('.')[0];out.append('<hr class="section-divider">\n<h2 id="sec-'+num+'">'+rich(z)+'</h2>')
 elif z['role']=='HEADING_2':out.append('<h3 id="sec-2-'+z['text'].split('.')[0]+'">'+rich(z)+'</h3>')
 elif i in (97,114,121):
  tag='h4' if i==97 else 'h3';ids={97:'sec-2-8-quality',114:'sec-3-1',121:'sec-3-display'}
  out.append('<'+tag+' id="'+ids[i]+'">'+rich(z)+'</'+tag+'>')
 else:out.append('<p>'+rich(z)+'</p>')
 i+=1
start=old.index('<p>',old.index('<h3 id="sec-1-1">'));end=old.index('<h3 id="sec-3-2">')
s=old[:start]+'\n'.join(out)+'\n\n'+old[end:]
toc=b[108]['text'].split('. ',1)[1]
s=re.sub(r'(<a href="#sec-3">)[^<]+',lambda m:m[1]+esc(toc),s)
template=Path('article-template.html').read_text()
assert re.search(r'<style>.*?</style>',s,re.S).group()==re.search(r'<style>.*?</style>',template,re.S).group()
assert re.search(r'<script.*?</script>',s,re.S).group()==re.search(r'<script.*?</script>',old,re.S).group()
p.write_text(s)
model=json.loads(subprocess.check_output(['python3','tmp/price-review-doc-model.py',str(p)]))
actual=[]
for z in model['blocks']:
 if z['kind']=='paragraph':actual.append(z['text'])
 elif z['kind']=='table':actual.extend(c['text'] for r in z['rows'] for c in r)
 else:raise AssertionError('Unexpected image')
expected=[]
for i,z in enumerate(b):
 if i in notes:continue
 if 'table' in z:expected.extend(c for r in z['table'] for c in r)
 elif '\t' in z['text']:expected.extend(z['text'].split('\t'))
 else:expected.append(toc if i==13 else z['text'].replace('**',''))
assert actual==expected,'Text mismatch'
doclinks=[{'text':r['content'].strip(),'url':r['textStyle']['link']['url']} for z in b for r in z.get('runs',[]) if r.get('textStyle',{}).get('link',{}).get('url')]
links=[{'text':z['text'][m['start']:m['end']],'url':m['value']} for z in model['blocks'] if z['kind']=='paragraph' for m in z['marks'] if m['kind']=='link']
assert links==doclinks,'Link mismatch'
sha=hashlib.sha256(p.read_bytes()).hexdigest();archive=Path('tmp/price-sync2-archive.txt').read_text()
counts={'paragraphs':sum(z['kind']=='paragraph' for z in model['blocks']),'headings':sum(z['kind']=='paragraph' and z['role'].startswith('HEADING') for z in model['blocks']),'tables':sum(z['kind']=='table' for z in model['blocks']),'cells':sum(len(r) for z in model['blocks'] if z['kind']=='table' for r in z['rows']),'images':0,'links':len(links)}
snap.update({'syncedAt':datetime.datetime.now().astimezone().isoformat(),'htmlSHA256':sha,'archive':archive,'syncStatus':'passed_with_documented_format_normalization','reviewStatus':'not_re_reviewed_after_user_edit','verification':counts,'normalizations':{'editorialNotesSeparated':sorted(notes),'tabSeparatedRowsToTables':[42,49],'tocSyncedToChapter3':True,'markdownBoldToHTML':True,'plainTextHeadings':[97,114,121],'lists':list_ranges},'links':doclinks})
Path(str(base)+'-drive-sync-readback.json').write_text(json.dumps(snap,ensure_ascii=False,indent=2)+'\n')
note='# Google Docsに残っていた編集コメント（本文から分離）\n\n元データ全体は `physiology-about-price-drive-sync-readback.json` に保存。以下は原文のまま保持し、代替見出しの提案は本文へ自動採用していない。\n\n'+'\n\n'.join('## コメント '+str(j+1)+'\n\n'+b[i]['text'] for j,i in enumerate(sorted(notes)))
note+='\n\n## 同期時に確認した残件（今回の同期では改稿しない）\n\n- 画像が削除されているが、第3章に「図を見るときは」という参照文が残る。\n- 第2章の施策区分変更と第4章の既存早見表の対応は、次の校閲で確認する。\n- 第2章第3項と第4項のおとり効果の説明、新しい価格例・心理効果の主張は再審査未実施。\n'
Path(str(base)+'-user-edit-notes.md').write_text(note)
Path('tmp/price-sync2-result.json').write_text(json.dumps({'sha':sha,'counts':counts,'archive':archive},ensure_ascii=False))
print(json.dumps({'contentComparison':'passed','sha':sha,'counts':counts},ensure_ascii=False))
