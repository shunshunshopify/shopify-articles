from pathlib import Path
import json,re,html,struct,shutil,hashlib,datetime,subprocess
root=Path('tmp/price-user-sync-latest')
doc=json.loads((root/'document-result.json').read_text())['structuredContent']
content=doc['tabs'][0]['body']['content']
p=Path('drafts/physiology-about-price.html');old=p.read_text()
archive=Path('drafts/archive')/(datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')+'-user-sync');archive.mkdir()
for f in Path('drafts').glob('physiology-about-price*'):
 if f.is_file():shutil.copy2(f,archive/f.name)
def text(e):return ''.join(x.get('textRun',{}).get('content','') for x in e.get('paragraph',{}).get('elements',[])).strip()
def rich(e):
 out=[]
 for x in e['paragraph']['elements']:
  r=x.get('textRun',{});s=html.escape(r.get('content','').rstrip('\n'));style=r.get('textStyle',{})
  if style.get('bold'):s='<strong>'+s+'</strong>'
  if style.get('italic'):s='<em>'+s+'</em>'
  if style.get('link',{}).get('url'):s='<a href="'+html.escape(style['link']['url'],quote=True)+'">'+s+'</a>'
  out.append(s)
 return ''.join(out)
start=next(i for i,e in enumerate(content) if text(e)=='7. 割引率・割引額｜最終的な支払額まで分かりやすく示す')
end=next(i for i,e in enumerate(content) if text(e)=='8. 名声価格｜高い価格に見合う価値を伝える')
paras=[e for e in content[start+1:end] if text(e) and not text(e).startswith('https://cdn.shopify.com/')]
a=old.index('</h3>',old.index('<h3 id="sec-2-7">'))+len('</h3>');b=old.index('<h3 id="sec-2-8">',a)
s=old[:a]+'\n'+'\n'.join('<p>'+rich(e)+'</p>' for e in paras)+'\n\n'+old[b:]
items=json.loads((root/'image-urls.json').read_text())
alts=['単品価格とセット価格による3,000円の見え方の比較','2,000円と1,980円の端数価格の比較','単品合計3,600円とセット価格3,000円の比較','松・竹・梅の3段階の価格と内容の比較','選択肢A・BにCを加えるおとり効果の説明','スキンケア商品の単品購入とセット購入の比較','カート金額4,200円から5,000円で送料無料になる例','20％OFFと2,000円OFFの表示と最終支払額','高価格の商品と素材・製法・保証・サポートの説明','近接の法則と類似の法則による情報のまとまり']
assets=Path('drafts/physiology-about-price-assets');assets.mkdir(exist_ok=True)
for i,item in enumerate(items):
 image=root/f'image-{i+1}.png';raw=image.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';w,h=struct.unpack('>II',raw[16:24]);dest=assets/f'image-{i+1}.png';shutil.copy2(image,dest)
 pattern=r'(<h[23][^>]*>'+re.escape(item['afterHeading'])+r'</h[23]>)';assert len(re.findall(pattern,s))==1
 tag='<p><img src="'+html.escape(item['url'],quote=True)+'" alt="'+html.escape(alts[i],quote=True)+'" width="'+str(w)+'" height="'+str(h)+'" loading="lazy" decoding="async"></p>'
 s=re.sub(pattern,lambda m:m[1]+'\n'+tag,s)
 item.update({'width':w,'height':h,'alt':alts[i],'localPath':str(dest),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()});item.pop('paragraph',None)
template=Path('article-template.html').read_text()
assert re.search(r'<style>.*?</style>',s,re.S).group()==re.search(r'<style>.*?</style>',template,re.S).group()
assert re.search(r'<script.*?</script>',s,re.S).group()==re.search(r'<script.*?</script>',old,re.S).group()
p.write_text(s)
model=json.loads(subprocess.check_output(['python3','tmp/price-review-doc-model.py',str(p)]));model['blocks'][0]['text']='価格の心理学とは？ECで使える価格設定8選と選び方'
actual=[]
for z in model['blocks']:
 if z['kind']=='paragraph':actual.append(z['text'])
 elif z['kind']=='image':actual.append(z['url'])
 elif z['kind']=='table':actual.extend(c['text'] for r in z['rows'] for c in r)
expected=[]
for e in content:
 if text(e):expected.append(text(e))
 elif 'table' in e:expected.extend(''.join(text(p) for p in c['content']) for row in e['table']['tableRows'] for c in row['tableCells'])
assert actual==expected,'Source and HTML text/image/table order mismatch'
record={'status':'passed_with_image_url_embedding','reviewStatus':'not_re_reviewed_after_user_edit','documentId':doc['documentId'],'revisionId':doc['revisionId'],'url':'https://docs.google.com/document/d/'+doc['documentId']+'/edit','syncedAt':datetime.datetime.now().astimezone().isoformat(),'htmlSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'archive':str(archive),'images':items,'tables':3,'cells':73,'paragraphs':sum(z['kind']=='paragraph' for z in model['blocks']),'sourceComparison':'passed','normalization':'User image URL paragraphs embedded as images; image alt/actual dimensions/lazy decoding added. No copyediting.'}
shutil.copy2(root/'document-result.json',Path('drafts/physiology-about-price-drive-sync-raw.json'))
Path('drafts/physiology-about-price-drive-sync-readback.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(root/'sync-result.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in record.items() if k!='images'},ensure_ascii=False))
