import html,re,unicodedata,json
from pathlib import Path
from chronology import date_key

def normalized(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode())
def catalogue(blocks,nodes):
 groups={'Referāti, plenārdiskusijas un plakātreferāti':[],'Publiskas lekcijas un semināri':[]};group=None
 for b in blocks:
  if b['tag']=='h2':
   if b['text']=='Publicitāte medijos':break
   group=next(iter(groups)) if b['text']=='Akadēmiski priekšlasījumi' else b['text']
  elif group in groups and b['tag']=='li':groups[group].append((b['text'],re.sub(r'^<li>|</li>$','',b['html'])))
 existing=[normalized(text) for items in groups.values() for text,body in items]
 ids=set(i for n in nodes.values() for label,items in n.get('groups',[]) if label=='Uzstāšanās' for i in items)
 for id in sorted(ids,key=lambda key:(nodes[key].get('meta',''),key)):
  n=nodes[id]
  matching=any(normalized(n['title']) in text for text in existing)
  if matching and id not in ('sief2025-diaries','iaba2019-autobiography'):continue
  target='Publiskas lekcijas un semināri' if n.get('type')=='Profesionāla sesija' else next(iter(groups))
  meta=n.get('meta','')
  date_match=re.match(r'^(\d[^·]*?(?:19|20)\d{2}\.?)(?:\s*·\s*|\s+)(.*)$',meta)
  date,context=(date_match[1],date_match[2]) if date_match else ('',meta)
  if n['title'] in context:context=context.replace(n['title'],'').strip(' .·')
  parts=[html.escape(part) for part in [date,n['title'],n.get('type',''),context] if part]
  body='<p>'+ ' · '.join(parts)
  if n.get('url'):body+=' · <a href="'+html.escape(n['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+html.escape(n.get('source','Atvērt avotu'))+'</a>'
  body+='</p>'
  if matching:
   for name,entries in groups.items():
    groups[name]=[(n.get('sort_date','')+' '+n.get('meta',''),body) if normalized(n['title']) in normalized(text) else (text,original) for text,original in entries]
  else:groups[target].append((n.get('sort_date','')+' '+n.get('meta',''),body))
 invited=json.loads(Path('src/data/invited-presentations.json').read_text())
 invited_titles={normalized(r['title']) for r in invited}
 # The Rome appearance is an invited plenary discussion, not a keynote lecture.
 invited_titles.add(normalized(nodes['rome']['title']))
 keynotes=[]
 for name,items in groups.items():
  retained=[]
  for text,body in items:
   combined=normalized(text+' '+re.sub(r'<[^>]+>','',body))
   if normalized(nodes['rome']['title']) in combined:keynotes.append((text,body))
   elif not any(title in combined for title in invited_titles):retained.append((text,body))
  groups[name]=retained
 for r in invited:
  body='<p>'+html.escape(r['date']+'. '+r['title']+'. '+r['context'])
  if r.get('url'):body+=' · <a href="'+html.escape(r['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+html.escape(r['source'])+'</a>'
  keynotes.append((r['date'],body+'</p>'))
 result='<section class="section academic-section academic-keynotes"><h2>Plenārrunas un aicinātas uzstāšanās</h2><ul class="academic-list">'+''.join('<li>'+body+'</li>' for text,body in sorted(keynotes,key=lambda x:date_key(x[0]),reverse=True))+'</ul></section>'
 for title,items in groups.items():
  by_year={}
  for text,body in sorted(items,key=lambda x:date_key(x[0]),reverse=True):
   year=str(date_key(text)[0]) if date_key(text)[0] else 'Datums precizējams'
   by_year.setdefault(year,[]).append(body)
  result+='<section class="section academic-section"><h2>'+title+'</h2>'
  for year,entries in by_year.items():
   result+='<details class="publicity-group academic-year"><summary><span>'+year+'</span><span class="media-group-count">'+str(len(entries))+'</span><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><ul class="academic-list">'+''.join('<li>'+body+'</li>' for body in entries)+'</ul></details>'
  result+='</section>'
 return result
