import re,sys
t=open('ocr/book.txt',encoding='utf-8').read()
pages=re.split(r'=====OCRPAGE p(\d+)=====\n',t)[1:]
pg={int(pages[i]):pages[i+1] for i in range(0,len(pages),2)}
a,b=int(sys.argv[1]),int(sys.argv[2])
skip=('الجامعة الافتراضي','SYRIAN','الجمهورية العربية','وزارة التعليم','والمكان الزمان')
for n in range(a,b+1):
    lines=[l for l in pg[n].split('\n') if l.strip() and not any(s in l for s in skip)]
    print(f"\n### p{n}\n"+'\n'.join(lines))
