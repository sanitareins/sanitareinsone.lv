"""Complete collected meeting catalogue; private calendar details stay in source data."""
import json,re,html
from pathlib import Path
from collections import Counter
from chronology import date_key

def display_date(r):
 raw=r['date']
 if r['id']=='SR-020':return '12.2024'
 if r['id']=='SR-035':return '29.04. · gads precizējams'
 match=re.search(r'\d{2}\.\d{2}\.\d{4}',raw)
 if match:return match[0]
 year=re.search(r'(?:19|20)\d{2}',raw)
 return year[0]+(' · datums precizējams' if r['id']=='USR-002' else '') if year else 'Datums precizējams'

def catalogue():
 records=[r for r in json.loads(Path('src/data/meetings.json').read_text())['records'] if not r['id'].startswith('CONF26-') and r['id'] not in {'SR-035','CAL-031'}]
 professional={'SR-002','SR-011','SR-014','SR-017','SR-032','SR-033','SR-034','SR-035','CAL-001','CAL-004','CAL-005','CAL-011','CAL-013','CAL-023','CAL-028','CAL-033','CAL-034','CAL-035','CAL-036','CAL-037','CAL-038'}
 groups=[('Tikšanās, lasījumi un sarunas',[r for r in records if r['id'] not in professional|{'SR-036','SR-037'}]),('Publiskas lekcijas, semināri un diskusijas',[r for r in records if r['id'] in professional])]
 e=html.escape;out=''
 for label,items in groups:
  counts=Counter(str(date_key(display_date(r))[0]) if date_key(display_date(r))[0] else 'Datums precizējams' for r in items)
  out+='<section class="meeting-group"><h2>'+label+'</h2>';year=None
  for r in sorted(items,key=lambda r:date_key(display_date(r)),reverse=True):
   date=display_date(r);current=str(date_key(date)[0]) if date_key(date)[0] else 'Datums precizējams'
   if current!=year:
    if year is not None:out+='</div></details>'
    out+='<details class="meeting-year-group"'+(' open' if current=='2026' else '')+'><summary><h3 class="meeting-year">'+current+'</h3><span class="media-group-count">'+str(counts[current])+'</span><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="meeting-list">';year=current
   place=r['place'].split(', Avenue')[0].split(', Rue')[0]
   place=re.sub(r';[^;]*jāprecizē','',place).replace(' (pēc kalendāra apraksta)','').replace(' (saīsinājums kalendārā)','')
   if r['id']=='USR-003':place='Berģu Mūzikas un mākslas pamatskola'
   if place=='Vieta jāprecizē':place=r['title']
   title=e(place);urls=[s['url'] for s in r.get('sources',[]) if s.get('url')]
   if urls:title='<a href="'+e(urls[0],quote=True)+'" target="_blank" rel="noopener noreferrer">'+title+'</a>'
   status='Darba plāns · norise nav apstiprināta' if r['id']=='SR-037' else ''
   kind='Videosveiciens' if r['id']=='SR-036' else r['kind']
   out+='<article class="meeting-row" id="meeting-'+r['id']+'"><span class="meeting-date">'+e(date)+'</span><div><h4>'+title+'</h4>'+('<p>'+e(r['title'])+'</p>' if place!=r['title'] else '')+'<span class="meeting-kind">'+e(kind)+'</span>'+('<span class="meeting-status">'+e(status)+'</span>' if status else '')+'</div></article>'
  if year is not None:out+='</div></details>'
  out+='</section>'
 return out
