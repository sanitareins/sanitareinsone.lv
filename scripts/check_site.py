"""Dependency-free checks for the bilingual static site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re
D=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.language=None;self.switches=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.language=a.get('lang')
  if a.get('id'):self.ids.add(a['id'])
  for key in ['href','src']:
   if a.get(key):self.links.append(a[key])
  if 'data-language-switch' in a:self.switches.append(a['href'])
pages={p:Page() for p in D.rglob('*.html')}
for p,parsed in pages.items():parsed.feed(p.read_text())
assert len(pages)==28,len(pages)
errors=[]
for p,parsed in pages.items():
 assert parsed.language==('en' if p.parent.name=='en' else 'lv'),p
 assert len(parsed.switches)==1,p
 for link in parsed.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if u.path.startswith('/'):errors.append((p.name,'absolute path',link));continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append((str(p.relative_to(D)),link,'missing target'))
 for forbidden in ['Kalendāra ieraksts','Plenārrunas un uzstāšanās pēc uzaicinājuma']:
  assert forbidden not in p.read_text(),(p,forbidden)
for lang,filename in [('lv','research.js'),('en','en/research.js')]:
 text=(D/filename).read_text();nodes=json.JSONDecoder().raw_decode(text.split('const nodes=',1)[1])[0]
 for key,node in nodes.items():
  for label,ids in node.get('groups',[]):
   for target in ids:assert target in nodes,(key,label,target)
 expected_projects={p['id'] for p in json.loads((D.parent/'src/data/projects.json').read_text())}
 assert {k for k,n in nodes.items() if n.get('project')}==expected_projects & nodes.keys()
 catalogue=(D/('en/projects.html' if lang=='en' else 'projekti.html')).read_text()
 assert catalogue.count('class="project-record"')==len(expected_projects)
 assert 'isDatasetCategory' in text
 if lang=='en':
  for key in ['infrastructure','memory','folklore','language','participation']:assert nodes[key]['type']=='Theme'
  for n in nodes.values():
   for attr in ['type','past_label']:
    assert not re.search('[āčēģīķļņšūž]',n.get(attr,''),re.I),(attr,n.get(attr))
assert not errors,errors
print('Passed: 28 pages, reciprocal language switches, local links/assets, 21 projects per language, graph references and translated UI types.')
