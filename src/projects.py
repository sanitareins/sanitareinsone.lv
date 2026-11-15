"""Shared project metadata for compact cards and expanded project records."""
import json,html,re
from datetime import date
from pathlib import Path
from chronology import date_key
PROJECTS=json.loads(Path('src/data/projects.json').read_text())
FIELDS=[('Pilnais nosaukums','full_name'),('Periods','period'),('Programma','programme'),('Finansējums','funding'),('Koordinators','coordinator'),('Mana loma','role'),('LU loma','institution_role'),('Partneri','partners'),('Projekta numurs','identifier')]
def past_label(p):
 dates=re.findall(r'(\d{2})\.(\d{2})\.(\d{4})',p.get('dates',''))
 if dates:
  day,month,year=map(int,dates[-1]);ended=date(year,month,day)<date.today()
 else:
  years=re.findall(r'(?:19|20)\d{2}',p.get('period',''));ended=bool(years) and int(years[-1])<date.today().year
 return 'Noslēdzies projekts'+(' · '+p['period'] if p.get('period') else '') if ended else ''
def status_marker(label):
 if not label:return ''
 value=html.escape(label,quote=True)
 return '<span class="past-marker" role="img" aria-label="'+value+'" title="'+value+'"></span>'
def facts(p):
 result=[]
 for label,key in FIELDS:
  value=(p.get('dates') or p.get('period')) if key=='period' else p.get(key)
  if value:result.append((label,value))
 return result
def apply_projects(nodes):
 for p in PROJECTS:
  if p['id'] not in nodes:continue
  n=nodes[p['id']];p['sort_date']=n.get('sort_date',p['period'])
  n['past_label']=past_label(p);n['title']=p['short_name'];n['meta']=' · '.join(x for x in [p['period'],p.get('role') or p.get('institution_role')] if x);n['project']=dict(p,facts=facts(p));n.pop('description',None)
  if not n.get('sort_date') and p['period']:n['sort_date']=p['period']
  if not p['url']:n.pop('url',None)
  elif p['url']:n['url']=p['url'];n['source']=p.get('url_label','Projekta mājaslapa')
 return nodes
def project_catalogue():
 e=html.escape;groups={'current':'','past':''}
 arrow='<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'
 for p in sorted(PROJECTS,key=lambda p:date_key(p.get('sort_date') or p['period']),reverse=True):
  role=p.get('role') or p.get('institution_role') or ''
  name=e(p['short_name'])
  if p['url']:name='<a href="'+e(p['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+name+'</a>'
  full='<p class="project-full-name">'+e(p['full_name'])+'</p>' if p['full_name'].strip().casefold()!=p['short_name'].strip().casefold() else ''
  facts=''
  if p.get('funding'):facts+='<div><dt>Finansētājs</dt><dd>'+e(p['funding'])+'</dd></div>'
  if p.get('identifier'):facts+='<div><dt>Nr.</dt><dd>'+e(p['identifier'])+'</dd></div>'
  link='<a class="project-site-link" href="'+e(p['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(p.get('url_label','Projekta mājaslapa'))+arrow+'</a>' if p['url'] else ''
  groups['past' if past_label(p) else 'current']+='<article class="project-record" id="project-'+p['id']+'"><span class="project-period">'+e(p['period'])+'</span><div><h3 class="project-name">'+name+status_marker(past_label(p))+'</h3>'+full+('<p class="project-preview-role">'+e(role)+'</p>' if role else '')+('<dl class="project-compact-facts">'+facts+'</dl>' if facts else '')+link+'</div></article>'
 chevron='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
 sections=''
 for key,label in [('current','Notiekošie projekti'),('past','Noslēgušies projekti')]:
  if groups[key]:sections+='<details class="project-status-group"'+(' open' if key=='current' else '')+'><summary><h2>'+label+'</h2>'+chevron+'</summary>'+groups[key]+'</details>'
 return '<section class="section project-catalogue"><div class="section-head"><h2>Pētniecības un attīstības projekti</h2></div>'+sections+'</section>'
