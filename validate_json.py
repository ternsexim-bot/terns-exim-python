import re, json, glob
ok = True
for f in sorted(glob.glob('templates/*.html')):
    c = open(f, encoding='utf-8').read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
    for i, m in enumerate(blocks):
        try:
            json.loads(m.strip())
        except Exception as e:
            print(f'INVALID  {f}  block#{i+1}  ::  {e}')
            ok = False
print('ALL JSON VALID' if ok else 'ERRORS ABOVE')
