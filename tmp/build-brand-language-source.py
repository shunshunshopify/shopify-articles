from pathlib import Path
import json,re,html
root=Path('/Users/garrypanda/Documents/shopify-articles')
stem='brand-building-first-steps-language-20260922'
ps=json.loads((root/'drafts/.trusted-read-brand-language-source-20260922/document-outline.json').read_text())['paragraphs']
template=(root/'article-template.html').read_text()
ids=dict(zip(['P00006','P00022','P00025','P00029','P00049','P00052','P00060','P00064','P00066','P00080','P00105','P00109','P00112','P00131','P00151','P00156','P00160','P00167','P00170','P00174','P00177','P00180','P00202','P00211','P00214'],['sec-learn','brand-first-decision','why-not-name-logo-first','one-page-brand-core','define-target-and-problem','target-beyond-demographics','desired-change','value-and-difference','feature-to-value','compare-alternatives','credible-reason','write-brand-concept','four-elements-summary','concept-template','concept-check','validate-and-revise','name-logo-timing','choose-name-after-concept','trademark-search','design-logo-after-name','apply-core-consistently','common-brand-launch-mistakes','sec-faq','sec-summary','sec-references']))
def inline(t):
    out=[];pos=0
    for m in re.finditer(r'\[([^\]]+)\]\((https?://[^)]+)\)',t):
        out.extend([html.escape(t[pos:m.start()]),'<a href="'+html.escape(m[2],quote=True)+'">'+html.escape(m[1])+'</a>']);pos=m.end()
    out.append(html.escape(t[pos:]));return ''.join(out)
out=[];listopen=False;i=2
while i<len(ps):
    p=ps[i];t=p['text'].replace('[HORIZONTAL_RULE]','');pid=p['paragraphId'];i+=1
    if not t.strip():continue
    if pid=='P00013':
        if listopen:out.append('</ul>');listopen=False
        out.append('<div class="toc">\n<h2 class="no-style">目次</h2>\n<ol>')
        for q in ps:
            if q['paragraphId'] in ['P00022','P00049','P00064','P00109','P00160','P00180','P00202','P00211']:
                tx=q['text'].replace('[HORIZONTAL_RULE]','');tx=re.sub(r'^\d+\. ','',tx)
                if q['paragraphId']=='P00211':tx='まとめ'
                out.append('<li><a href="#'+ids[q['paragraphId']]+'">'+inline(tx)+'</a></li>')
        out.append('</ol>\n</div>');i=21;continue
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
            out.append('<tr>'+''.join('<'+tag+'>'+inline(' '.join(v))+'</'+tag+'>' for ci,v in cells.items())+'</tr>')
            if ri==0:out.append('</thead>')
        out.append('</tbody></table></div>');continue
    if p['isListItem']:
        if not listopen:out.append('<ul>');listopen=True
        out.append('<li>'+inline(t)+'</li>');continue
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
body='\n'.join(out)
prefix=template.split('<!-- ▼▼▼ ここから本文')[0]
suffix=template[template.index('<!-- 構造化データ（JSON-LD）'):]
title=ps[1]['text']
brief=(root/f'drafts/{stem}-brief.md').read_text()
meta=json.loads(re.search(r'## 機械検証用メタデータ\s*```json\s*(.*?)\s*```',brief,re.S)[1])['meta_description']
suffix=suffix.replace('HEADLINE',title).replace('DESCRIPTION',meta)
result=prefix+'\n'+body+'\n'+suffix
(root/f'drafts/{stem}.html').write_text(result)
(root/f'drafts/{stem}-source.html').write_text(result)
(root/f'drafts/{stem}-heading-ids.json').write_text(json.dumps(ids,ensure_ascii=False,indent=2))
print('Wrote native-source HTML; paragraphs',len(ps),'tables',body.count('<table>'),'links',body.count('<a '))
