from pathlib import Path
from datetime import datetime, timezone
import json,re,html,hashlib,shutil,difflib

root=Path('/Users/garrypanda/Documents/shopify-articles');d=root/'drafts'
base='brand-building-first-steps';version=base+'-language-20260922'
live=d/'.trusted-read-brand-human-sync-20260922'
old=d/'.trusted-read-brand-language-copy-after-20260922'
now=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
archive=d/'archive'/(base+'-before-human-sync-'+now);archive.mkdir(parents=True)
for path in d.glob(base+'*'):
    if path.is_file():shutil.copy2(path,archive/path.name)
oldps=json.loads((old/'document-outline.json').read_text())['paragraphs']
doc=json.loads((live/'document-outline.json').read_text());ps=doc['paragraphs']
raw=json.loads((live/'document-result.json').read_text())['structuredContent']
assert len(raw['tabs'])==1
oldids=json.loads((d/(version+'-heading-ids.json')).read_text())
def heads(items):return [p for p in items if p['namedStyleType'].startswith('HEADING_') and p['text'].strip()]
oh,nh=heads(oldps),heads(ps);assert len(oh)==len(nh)
ids={};changes=[]
for a,b in zip(oh,nh):
    assert a['namedStyleType']==b['namedStyleType']
    if a['paragraphId'] in oldids:ids[b['paragraphId']]=oldids[a['paragraphId']]
    av=a['text'].replace('[HORIZONTAL_RULE]','');bv=b['text'].replace('[HORIZONTAL_RULE]','')
    if av!=bv:changes.append((av,bv))
template=(root/'article-template.html').read_text();css=(root/'theme-css/solstar-article.css').read_text()
style=re.search(r'<style>(.*?)</style>',template,re.S)[1]
def normcss(s):return re.sub(r'\s+','',re.sub(r'/\*.*?\*/','',s,flags=re.S))
assert normcss(style)==normcss(css)
def inline(t):
    out=[];pos=0
    for m in re.finditer(r'\[([^\]]+)\]\((https?://[^)]+)\)',t):
        out.extend([html.escape(t[pos:m.start()]),'<a href="'+html.escape(m[2],quote=True)+'">'+html.escape(m[1])+'</a>']);pos=m.end()
    out.append(html.escape(t[pos:]));return ''.join(out).replace('\x0b','<br>')
out=[];listopen=False;i=2
while i<len(ps):
    p=ps[i];t=p['text'].replace('[HORIZONTAL_RULE]','');pid=p['paragraphId'];i+=1
    if not t.strip():continue
    if t=='目次':
        if listopen:out.append('</ul>');listopen=False
        out.append('<div class="toc">\n<h2 class="no-style">目次</h2>\n<ol>')
        for q in nh:
            qid=ids.get(q['paragraphId'])
            if q['namedStyleType']=='HEADING_2' and qid not in ('sec-learn','sec-references'):
                tx=re.sub(r'^\d+\. ','',q['text'].replace('[HORIZONTAL_RULE]',''))
                if qid=='sec-summary':tx='まとめ'
                out.append('<li><a href="#'+qid+'">'+inline(tx)+'</a></li>')
        out.append('</ol>\n</div>')
        while i<len(ps) and ps[i]['namedStyleType']!='HEADING_2':i+=1
        continue
    if p['table']:
        if listopen:out.append('</ul>');listopen=False
        group=[p];key=p['table']['tableStartIndex']
        while i<len(ps) and ps[i]['table'] and ps[i]['table']['tableStartIndex']==key:group.append(ps[i]);i+=1
        rows={}
        for q in group:rows.setdefault(q['table']['rowIndex'],{}).setdefault(q['table']['columnIndex'],[]).append(q['text'])
        out.append('<div class="tbl-scroll"><table>')
        for ri,cells in rows.items():
            if ri==0:out.append('<thead>')
            elif ri==1:out.append('<tbody>')
            tag='th' if ri==0 else 'td'
            out.append('<tr>'+''.join('<'+tag+'>'+inline(' '.join(v))+'</'+tag+'>' for v in cells.values())+'</tr>')
            if ri==0:out.append('</thead>')
        out.append('</tbody></table></div>');continue
    if p['isListItem'] or t.startswith('* '):
        if not listopen:out.append('<ul>');listopen=True
        out.append('<li>'+inline(t[2:] if t.startswith('* ') else t)+'</li>');continue
    if listopen:out.append('</ul>');listopen=False
    if p['namedStyleType'].startswith('HEADING_'):
        level=p['namedStyleType'][-1]
        if '[HORIZONTAL_RULE]' in p['text']:out.append('<hr class="section-divider">')
        attr=' id="'+ids[pid]+'"' if pid in ids else ''
        out.append('<h'+level+attr+'>'+inline(t)+'</h'+level+'>')
    else:
        cls=' class="article-updated"' if pid=='P00003' else ' class="article-supervisor"' if pid=='P00004' else ''
        out.append('<p'+cls+'>'+inline(t)+'</p>')
if listopen:out.append('</ul>')
brief=(d/(version+'-brief.md')).read_text()
for a,b in changes:brief=brief.replace(a,b)
intro_new=ps[4]['text'];intro_old=oldps[4]['text']
notice=f'''## 人間レビュー反映・同期状態（2026-09-22）

- 最新正本: https://docs.google.com/document/d/{raw['documentId']}/edit
- revision ID: `{raw['revisionId']}`
- 今回はGoogle Docからローカルへの同期。人間の編集文を保持し、追加の文章校正・事実審査は行っていない。
- 導入文、第1〜3章、ペルソナの呼称、H2 2/H2 3/H3 1件、画像URLを同期した。
- 以下の設計意図は前版から継承した参考資料。変更箇所では最新HTML/Drive本文を正本とする。旧審査の合格を現行稿へ引き継がない。
- 確定メタは主題と7項目/コンセプト作成/命名の内容が維持されているため変更なし。
- 第1章の画像URLはDriveでURLのみの段落として追加されているため、その形で取り込む。埋め込みやaltは今回確定しない。

'''
brief=brief.replace('## 機械検証用メタデータ',notice+'## 機械検証用メタデータ',1)
meta=json.loads(re.search(r'## 機械検証用メタデータ\s*```json\s*(.*?)\s*```',brief,re.S)[1])['meta_description']
prefix=template.split('<!-- ▼▼▼ ここから本文')[0]
suffix=template[template.index('<!-- 構造化データ（JSON-LD）'):].replace('HEADLINE',ps[1]['text']).replace('DESCRIPTION',meta)
result=prefix+'\n'+'\n'.join(out)+'\n'+suffix
sha=hashlib.sha256(result.encode()).hexdigest()
source_text='\n\n'.join(p['text'] for p in ps)+'\n'
diff='\n'.join(difflib.unified_diff([p['text'] for p in oldps],[p['text'] for p in ps],fromfile='前回保存時Drive',tofile='人間レビュー後Drive',n=2))
for stem in (base,version):
    (d/(stem+'.html')).write_text(result)
    (d/(stem+'-brief.md')).write_text(brief)
    (d/(stem+'-drive-source.txt')).write_text(source_text)
    (d/(stem+'-heading-ids.json')).write_text(json.dumps(ids,ensure_ascii=False,indent=2)+'\n')
    for gate in ('japanese-review','review','legal-review'):
        (d/(stem+'-'+gate+'.md')).write_text(f'# 現行原稿の審査状態\n\n- 状態: `not_reviewed_after_human_edit`\n- 現行HTML SHA-256: `{sha}`\n- 人間レビュー後のGoogle Docを2026-09-22に同期。前版の合格は現行稿に適用しない。\n- 以前の審査記録: `{archive.relative_to(root)}/{stem}-{gate}.md`\n- 今回は同期のみ。再審査やDriveへの書き戻しは行っていない。\n')
sources=(archive/(version+'-sources.md')).read_text()
source_header=f'''# 現行同期稿の事実確認状態

- 状態: `not_rechecked_after_human_edit`
- 現行HTML SHA-256: `{sha}`
- 2026-09-22に人間レビュー後のDriveを同期。下記台帳とpost-write合格は前版の履歴であり、現行稿の再合格ではない。
- 同期した第2章には「ペルソナ（ターゲット）」の用語、第3章には「選ばれる理由になります」という人間の編集がある。元の文を保持し、独自の検証済み主張に置き換えない。
- 画像URLの追加位置は第1章冒頭。画像内容・権利・altは今回未検証。

---

'''
for stem in (base,version):(d/(stem+'-sources.md')).write_text(source_header+sources)
url=next(p['text'] for p in ps if p['text'].startswith('https://cdn.shopify.com/'))
assets=f'# 同期した素材情報\n\n- 提供元: 人間レビュー後のGoogle Doc\n- 挿入位置: H2 1直後\n- URL: {url}\n- Drive上は画像埋め込みではなくURL段落。HTMLでもURL段落を保持。\n- 画像内容・権利・alt・寸法は未検証。今回のローカル同期で推測追加していない。\n'
for stem in (base,version):(d/(stem+'-assets.md')).write_text(assets)
(d/(base+'-human-sync-20260922.diff')).write_text(diff+'\n')
summary={'archive':str(archive.relative_to(root)),'sha256':sha,'previous_sha256':hashlib.sha256((archive/(version+'.html')).read_bytes()).hexdigest(),'document_id':raw['documentId'],'revision_id':raw['revisionId'],'paragraphs':len(ps),'tables':result.count('<table>'),'heading_changes':changes,'snapshot':str(live.relative_to(root)),'html_paths':[str(d/(s+'.html')) for s in (base,version)]}
(d/(base+'-human-sync-20260922.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
