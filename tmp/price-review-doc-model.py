from html.parser import HTMLParser
from pathlib import Path
import json, re, sys

class Node:
    def __init__(self, tag='', attrs=None):
        self.tag, self.attrs, self.children = tag, dict(attrs or []), []
    def text(self):
        return ''.join(c if isinstance(c, str) else ('\n' if c.tag == 'br' else c.text()) for c in self.children)
    def all(self, tag):
        for c in self.children:
            if isinstance(c, Node):
                if c.tag == tag: yield c
                yield from c.all(tag)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.root=Node(); self.stack=[self.root]
    def handle_starttag(self, tag, attrs):
        n=Node(tag, attrs); self.stack[-1].children.append(n)
        if tag not in {'img','hr','br','meta','link','input','source','wbr'}: self.stack.append(n)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag: self.stack=self.stack[:i];break
    def handle_data(self, data): self.stack[-1].children.append(data)

def clean(s): return re.sub(r'\s+', ' ', s).strip()

def paragraph(n, role='NORMAL_TEXT', bullet=None):
    text=clean(n.text()); marks=[]
    for tag, kind in [('a','link'),('strong','bold'),('b','bold'),('em','italic')]:
        for x in n.all(tag):
            label=clean(x.text()); start=text.find(label)
            if not label or start<0: continue
            value=x.attrs.get('href') if kind=='link' else True
            if kind=='link':
                if not value or value.startswith('#'):continue
                if value.startswith('/'):value='https://www.solstar.co.jp'+value
            marks.append({'start':start,'end':start+len(label),'kind':kind,'value':value})
    return {'kind':'paragraph','text':text,'role':role,'bullet':bullet,'marks':marks}

def blocks(n, in_toc=False):
    out=[]
    for c in n.children:
        if not isinstance(c,Node):continue
        if c.tag in ['style','script']:continue
        if c.tag in ['h1','h2','h3','h4']:
            role={'h1':'TITLE','h2':'HEADING_1','h3':'HEADING_2','h4':'HEADING_3'}[c.tag]
            out.append(paragraph(c,role))
        elif c.tag=='p':
            if clean(c.text()):out.append(paragraph(c))
            for im in c.all('img'):out.append({'kind':'image','url':im.attrs['src'],'alt':im.attrs.get('alt','')})
        elif c.tag in ['ul','ol']:
            for li in c.children:
                if isinstance(li,Node) and li.tag=='li':out.append(paragraph(li,bullet='number' if c.tag=='ol' else 'bullet'))
        elif c.tag=='table':
            rows=[]
            for tr in c.all('tr'):
                cells=[paragraph(x) for x in tr.children if isinstance(x,Node) and x.tag in ['th','td']]
                if cells:rows.append(cells)
            out.append({'kind':'table','rows':rows})
        elif c.tag=='img':out.append({'kind':'image','url':c.attrs['src'],'alt':c.attrs.get('alt','')})
        else:out.extend(blocks(c,in_toc or c.attrs.get('class')=='toc'))
    return out

source=Path(sys.argv[1]);p=Parser();p.feed(source.read_text())
title='価格の心理学とは？ECで使える価格設定8選と検証方法'
model=[{'kind':'paragraph','text':title,'role':'TITLE','marks':[],'bullet':None}]+blocks(p.root)
print(json.dumps({'title':title,'blocks':model},ensure_ascii=False))
