from pathlib import Path
import json,sys,hashlib
root=Path('/Users/garrypanda/Documents/shopify-articles')
stem='brand-building-first-steps-language-20260922'
src=root/'drafts/.trusted-read-brand-language-source-20260922'
dst=Path(sys.argv[1])
pairs=json.loads((root/f'drafts/{stem}-replacements.json').read_text())
def read(base,name):return json.loads((base/name).read_text())
def trans(s):
 for a,b in pairs:s=s.replace(a,b)
 return s
sp=read(src,'document-outline.json')['paragraphs'];dp=read(dst,'document-outline.json')['paragraphs']
assert len(sp)==len(dp),(len(sp),len(dp))
changes=0
for i,(a,b) in enumerate(zip(sp,dp)):
 assert trans(a['text'])==b['text'],(i,a['text'],trans(a['text']),b['text'])
 for key in ('namedStyleType','isListItem','nestingLevel'):
  assert a[key]==b[key],(i,key,a[key],b[key])
 assert (a['table'] is None)==(b['table'] is None)
 if a['table']:
  assert a['table']['rowIndex']==b['table']['rowIndex']
  assert a['table']['columnIndex']==b['table']['columnIndex']
 changes+=a['text']!=b['text']
sj=read(src,'document-result.json')['structuredContent'];dj=read(dst,'document-result.json')['structuredContent']
def signature(j):
 tabs=[];tables=[];links=[];paragraphstyles=[]
 def walk(x):
  if isinstance(x,dict):
   if 'table' in x:
    t=x['table'];tables.append({'rows':t.get('rows'),'columns':t.get('columns'),'tableStyle':t.get('tableStyle')})
   if 'textRun' in x:
    url=x['textRun'].get('textStyle',{}).get('link',{}).get('url')
    if url:links.append(url)
   if 'paragraphStyle' in x:paragraphstyles.append(x['paragraphStyle'])
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 for t in j['tabs']:
  tabs.append({k:t.get(k) for k in ('title','parentTabId','index','nestingLevel')});walk(t['body'])
 return {'tabs':tabs,'tables':tables,'links':links,'paragraphstyles':paragraphstyles}
ss=signature(sj);ds=signature(dj)
for k in ('tabs','tables','links','paragraphstyles'):assert ss[k]==ds[k],k
print(json.dumps({'status':'passed','paragraphs':len(dp),'changed_paragraphs':changes,'tables':len(ds['tables']),'hyperlink_runs':len(ds['links']),'preserved':'tab topology, paragraph styles, list membership, table shape/style, all links, all source text except approved replacements','html_sha256':hashlib.sha256((root/f'drafts/{stem}.html').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
