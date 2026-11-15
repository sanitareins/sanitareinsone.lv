"""One chronological media catalogue, independent from academic contributions."""
import json,html,re
from pathlib import Path
from urllib.parse import urlsplit
GROUPS=[('interviews','Intervijas un portreti'),('audio','Radio un raidieraksti'),('video','Televīzija un video'),('articles','Raksti, recenzijas un ziņas')]
def date_label(value):
 parts=value.split('-')
 return '.'.join(reversed(parts))+('.' if len(parts)<3 else '')
def category(r):
 kind=r['kind'].lower()
 if any(t in kind for t in ['radio','raidierakst']):return 'audio'
 if any(t in kind for t in ['tv','video','televīz']):return 'video'
 if any(t in kind for t in ['intervija','saruna','portrets']):return 'interviews'
 return 'articles'
def records():
 data=json.load(open('src/data/lsm-publicity.json'))['records']+json.load(open('src/data/publicity-other.json'))['records']+json.load(open('src/data/scienceforukraine-media.json'))['records']
 seen=set();result=[]
 for r in data:
  key=r['url'].rstrip('/') if r['url'] else r['id']
  if key in seen:continue
  seen.add(key)
  r=dict(r,category=category(r))
  r['scienceforukraine']=r.get('scienceforukraine',False) or r['id'] in {'media-180868','media-159475','media-157300'} or r['id'].startswith(('nature-sfu','science-sfu'))
  result.append(r)
 return sorted(result,key=lambda r:r['date'],reverse=True)
def filters():
 return '<div class="publicity-filters" role="group" aria-label="Atlasīt publicitāti">'+''.join('<button type="button" data-publicity-filter="'+k+'" aria-pressed="'+str(k=='all').lower()+'">'+label+'</button>' for k,label in [('all','Visi'),('research','Pētniecība'),('writing','Rakstniecība'),('ukraine','#ScienceForUkraine')])+'</div>'
def row(r):
 e=html.escape
 tags=[]
 if r.get('topics'):tags.append('research')
 if r.get('writing'):tags.append('writing')
 if r.get('scienceforukraine'):tags.append('ukraine')
 title=e(r['title'])
 if r['url']:title='<a href="'+e(r['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+title+'</a>'
 return '<article class="publicity-row" data-publicity="'+' '.join(tags)+'" data-media-id="'+r['id']+'"><time datetime="'+r['date']+'">'+date_label(r['date'])+'</time><div><p class="publicity-meta">'+e(' · '.join(x for x in [r['kind'],r['outlet'],r.get('author','')] if x))+'</p><h3>'+title+'</h3></div></article>'
def catalogue():
 data=records();out=filters()
 for key,label in GROUPS:
  items=[r for r in data if r['category']==key]
  out+='<details class="publicity-group" data-media-group="'+key+'"><summary><span>'+label+'</span><span class="media-group-count">'+str(len(items))+'</span><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="publicity-list" id="media-list-'+key+'">'+''.join(row(r) for r in items)+'</div><button class="publicity-more" type="button" data-show-more="'+key+'" aria-controls="media-list-'+key+'" aria-expanded="false" hidden>Rādīt pārējos</button></details>'
 return out
def add_media_to_graph(nodes):
 extra=json.load(open('src/data/publicity-other.json'))['records']
 for r in extra:
  if not r.get('topics'):continue
  key=next((k for k,n in nodes.items() if r['url'] and n.get('url','').rstrip('/')==r['url'].rstrip('/')),r['id'])
  n=nodes.setdefault(key,{'groups':[]})
  n.update(title=r['title'],type=r['kind'],meta=' · '.join(x for x in [date_label(r['date']),r.get('author',''),r['outlet']] if x),related=r['topics'],sort_date=date_label(r['date']),url=r['url'],source=r['outlet'])
  for theme in r['topics']:
   group=next((g for g in nodes[theme]['groups'] if g[0]=='Publicitāte'),None)
   if group is None:group=['Publicitāte',[]];nodes[theme]['groups'].append(group)
   if key not in group[1]:group[1].append(key)
  if r.get('scienceforukraine'):
   group=next(g for g in nodes['scienceforukraine']['groups'] if g[0]=='Publicitāte')
   if key not in group[1]:group[1].append(key)
 return nodes
