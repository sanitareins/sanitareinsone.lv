"""One author–date reference record and renderer for every publication view."""
from pathlib import Path
import json,re,html
RECORDS=json.loads(Path('src/data/bibliography.json').read_text())
DATASETS=json.loads(Path('src/data/dataset-bibliography.json').read_text())
BY_ID={r['id']:r for r in RECORDS+DATASETS}
def authors_year(r):
 date=str(r['year'])
 if r.get('date'):
  year,month,day=r['date'].split('-');months=['janvāris','februāris','marts','aprīlis','maijs','jūnijs','jūlijs','augusts','septembris','oktobris','novembris','decembris'];date=f"{year}, {int(day)}. {months[int(month)-1]}"
 return f"{r['authors']} ({date})."
def preview_authors_year(r):
 authors=r['authors']
 if len(authors)>160:
  authors=', '.join(authors.split(', ')[:4])+', u. c.'
 return authors_year(dict(r,authors=authors))
def title_html(r):
 t=html.escape(r['title'])
 if r.get('italic_title'):t='<em>'+t+'</em>'
 if r.get('descriptor'):t+=' ['+html.escape(r['descriptor'])+']'
 return t if r['title'].endswith(('?','!','.')) and not r.get('descriptor') else t+'.'
def reference_html(r,links=True):
 parts=[html.escape(authors_year(r)),title_html(r),r['tail_html']]
 if r['url']:
  u=html.escape(r['url'],quote=True)
  parts.append(f'<a href="{u}" target="_blank" rel="noopener noreferrer">{u}</a>' if links else u)
 return ' '.join(parts)
def plain_reference(r):return html.unescape(re.sub('<[^>]+>','',reference_html(r,False)))
def normalize_source(source):
 blocks=json.loads(Path('src/data/content.json').read_text())['publications']['blocks']
 for r in RECORDS:
  b=blocks[r['source_index']];citation='<p class="bibliography-reference">'+reference_html(r)+'</p>'
  if r.get('note'):citation+='<p class="bibliography-note">'+html.escape(r['note'])+'</p>'
  from publication_topics import TOPICS
  theme_names={'infrastructure':'Digitālās humanitārās zinātnes un pētniecības infrastruktūra','memory':'Atmiņu mantojums un dzīves pierakstīšana','folklore':'Folkloras arhīvi un digitālā folkloristika','language':'Valodu tehnoloģijas','participation':'Zinātne un sabiedrība'}
  citation+='<nav class="publication-topics" aria-label="Publikācijas tēmas">'+''.join('<a href="petnieciba.html?tema='+t+'#'+r['id']+'" data-publication-topic="'+t+'">'+html.escape(theme_names[t])+'</a>' for t in TOPICS[r['id']]['themes'])+'</nav>'
  replacement='<li>'+citation+'</li>' if b['tag']=='li' else citation
  assert b['html'] in source, r['id']
  source=source.replace(b['html'],replacement,1)
 return source
def apply_to_graph(nodes):
 for r in RECORDS+DATASETS:
  if r['id'] not in nodes:continue
  n=nodes[r['id']];n['title']=r['title'];n['meta']=plain_reference(r);n['sort_date']=r.get('issued',str(r['year']));n['url']=r['url'];n['source']='CLARIN repozitorija ieraksts' if r in DATASETS else 'DOI' if r['doi'] else 'Lasīt publikāciju';n['bibliography']=dict(authors_year=authors_year(r),preview_authors_year=preview_authors_year(r),descriptor=r.get('descriptor'),tail_html=r['tail_html'],doi=r['doi'],reference_html=reference_html(r,False))
 return nodes
