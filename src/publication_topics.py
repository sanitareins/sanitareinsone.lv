"""Curated thematic assignments shared by all publication views."""
import json
from pathlib import Path
TOPICS=json.loads(Path('src/data/publication-topics.json').read_text())
THEMES=('infrastructure','memory','folklore','language','participation')
def apply_publication_topics(nodes,records):
 ids={r['id'] for r in records}
 assert set(TOPICS)==ids, f'Publication mapping mismatch: {ids ^ set(TOPICS)}'
 for theme in THEMES:
  nodes[theme]['groups']=[[label,[i for i in group if i not in ids and i!='scienceforukraine-report']] for label,group in nodes[theme]['groups']]
 for r in records:
  key=r['id'];m=TOPICS[key]
  assert m['themes'] and all(t in THEMES for t in m['themes']),key
  n=nodes.setdefault(key,{'groups':[]})
  n.update(title=r['title'],type=m['type'],primary_topic=m['themes'][0])
  n['related']=list(dict.fromkeys(m['themes']+[t for t in n.get('related',[]) if t not in THEMES]))
  for theme in m['themes']:
   groups=nodes[theme]['groups']
   group=next((g for g in groups if g[0]==m['group']),None)
   if group is None:
    group=[m['group'],[]];groups.append(group)
   group[1].append(key)
 for theme in THEMES:
  nodes[theme]['groups']=[g for g in nodes[theme]['groups'] if g[1]]
 # The earlier report node stays available for historic hashes, while lists use its canonical citation.
 for n in nodes.values():
  for label,group in n.get('groups',[]):
   group[:]=list(dict.fromkeys('publication-68' if i=='scienceforukraine-report' else i for i in group))
 return nodes
