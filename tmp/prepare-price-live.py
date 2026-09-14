from pathlib import Path
from datetime import datetime
import re, json, hashlib, shutil
p=Path('drafts/physiology-about-price.html')
s=p.read_text()
archive=Path('drafts/archive')/(datetime.now().strftime('%Y-%m-%d-%H%M%S')+'-before-live-replacement')
archive.mkdir()
shutil.copy2(p,archive/p.name)
def image(m):
    tag=m.group()
    return tag[:-1]+' style="width:100%;height:auto;aspect-ratio:16 / 9;object-fit:contain;background:#fff;box-sizing:border-box;">'
s,n=re.subn(r'<img\b[^>]*>',image,s)
assert n==10
assert re.search(r'<style>(.*?)</style>',s,re.S).group(1)==re.search(r'<style>(.*?)</style>',Path('article-template.html').read_text(),re.S).group(1)
p.write_text(s)
graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1))['@graph']
article=next(x for x in graph if x['@type']=='Article')
result={'archive':str(archive),'title':article['headline'],'description':article['description'],'body':s,'sha256':hashlib.sha256(s.encode()).hexdigest()}
Path('tmp/price-live-payload.json').write_text(json.dumps(result,ensure_ascii=False))
print(json.dumps({k:v for k,v in result.items() if k!='body'},ensure_ascii=False))
