import json,difflib,sys
from pathlib import Path
source=json.loads(Path(sys.argv[1]).read_text());source=source.get('structuredContent',source)
model=json.loads(Path('tmp/price-taxonomy-model.json').read_text())
tab=source['tabs'][0];tid=tab['tabId'];old=[]
for e in tab['body']['content']:
 if 'paragraph' in e:
  t=''.join(x.get('textRun',{}).get('content','') for x in e['paragraph']['elements']).strip()
  if t:old.append({'key':t,'element':e,'kind':'p'})
 elif 'table' in e:
  rows=[]
  for r in e['table']['tableRows']:
   rows.append([''.join(x.get('textRun',{}).get('content','') for p in c['content'] for x in p.get('paragraph',{}).get('elements',[])).strip() for c in r['tableCells']])
  old.append({'key':'TABLE:'+json.dumps(rows[0],ensure_ascii=False),'element':e,'kind':'table','rows':rows})
desired=[]
for z in model['blocks']:
 if z['kind']=='paragraph':desired.append({'key':z['text'],'model':z})
 elif z['kind']=='table':desired.append({'key':'TABLE:'+json.dumps([c['text'] for c in z['rows'][0]],ensure_ascii=False),'model':z})
ops=[];new_tables=[]
sm=difflib.SequenceMatcher(None,[x['key'] for x in old],[x['key'] for x in desired],autojunk=False)
for tag,a,b,c,d in sm.get_opcodes():
 if tag=='equal':
  for i,j in zip(range(a,b),range(c,d)):
   if old[i]['kind']=='table':
    src=old[i];dst=desired[j]['model'];assert len(src['rows'])==len(dst['rows'])
    for ri,(rs,rd) in enumerate(zip(src['rows'],dst['rows'])):
     assert len(rs)==len(rd)
     for ci,(ts,td) in enumerate(zip(rs,rd)):
      if ts!=td['text']:
       cell=src['element']['table']['tableRows'][ri]['tableCells'][ci]
       paras=[p for p in cell['content'] if 'paragraph' in p]
       assert len(paras)==1
       p=paras[0];ops.append({'start':p['startIndex'],'end':p['endIndex']-1,'text':td['text']})
  continue
 assert not any(x['kind']=='table' for x in old[a:b]),'Native table deletion unexpected'
 start=old[a]['element']['startIndex'] if a<len(old) else old[-1]['element']['endIndex']-1
 end=old[b-1]['element']['endIndex'] if b>a else start
 text=[]
 for z in desired[c:d]:
  if z['model']['kind']=='table':
   marker='PRICE_TABLE_INSERT_'+str(len(new_tables)+1)
   new_tables.append({'marker':marker,'rows':z['model']['rows']});text.append(marker)
  else:text.append(z['model']['text'])
 ops.append({'start':start,'end':end,'text':'\n'.join(text)+('\n' if text else '')})
requests=[]
for x in sorted(ops,key=lambda x:x['start'],reverse=True):
 if x['end']>x['start']:requests.append({'deleteContentRange':{'range':{'tabId':tid,'startIndex':x['start'],'endIndex':x['end']}}})
 if x['text']:requests.append({'insertText':{'location':{'tabId':tid,'index':x['start']},'text':x['text']}})
Path('tmp/price-doc-content-requests.json').write_text(json.dumps(requests,ensure_ascii=False))
Path('tmp/price-doc-new-tables.json').write_text(json.dumps(new_tables,ensure_ascii=False))
print(json.dumps({'requests':len(requests),'newTables':len(new_tables),'oldTablesPreserved':sum(x['kind']=='table' for x in old)}))
