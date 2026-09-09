import re,sys
t=open('ocr/book.txt',encoding='utf-8').read()
pages=re.split(r'=====OCRPAGE p(\d+)=====\n',t)[1:]
pg={int(pages[i]):pages[i+1] for i in range(0,len(pages),2)}
for term in sys.argv[1:]:
    hits=[]
    for n,txt in pg.items():
        for m in re.finditer(re.escape(term), txt):
            s=txt[max(0,m.start()-70):m.end()+70].replace('\n',' ')
            hits.append((n,s))
    print(f"\n=== {term} : {len(hits)} hits, pages {sorted(set(h[0] for h in hits))[:25]}")
    for n,s in hits[:6]: print(f"  p{n}: …{s}…")
