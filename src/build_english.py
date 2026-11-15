"""Build matching English pages without a server, absolute paths or duplicated assets."""
from pathlib import Path
from html.parser import HTMLParser
import html,json,re
from english_dictionary import translate
D=Path('dist')
PAGES={'index.html':'index.html','petnieciba.html':'research.html','gramatas.html':'writing.html','kontakti.html':'contact.html','publikacijas.html':'publications.html','projekti.html':'projects.html','sarunas.html':'talks-and-meetings.html','uzstasanas.html':'academic-presentations.html','darbiba.html':'other-activities.html','publicitate.html':'media.html','draugi-un-kaimini.html':'draugi-un-kaimini.html','kus-mul-patarei.html':'kus-mul-patarei.html','meza-meitas.html':'meza-meitas.html','adama-stasts.html':'adama-stasts.html'}
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
def local_link(url):
 if re.match(r'^(?:https?:|mailto:|tel:|data:|#)',url):return url
 path,sep,tail=url.partition('?')
 path,hashsep,frag=path.partition('#')
 if path in PAGES:return PAGES[path]+(hashsep+frag)+(sep+tail)
 if path.startswith('assets/'):return '../'+url
 if path=='style.css':return '../'+url
 if path in ('main.js','publicity.js'):return '../'+path.replace('.js','.en.js')+(sep+tail)
 return url
class EnglishHTML(HTMLParser):
 def __init__(self,filename):super().__init__(convert_charrefs=True);self.filename=filename;self.out=[];self.stack=[];self.skip_language=False
 def handle_decl(self,s):self.out.append('<!'+s+'>')
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);classes=a.get('class','').split()
  protected=bool(self.stack and self.stack[-1][1]) or 'bibliography-reference' in classes or (tag in ('h3','h4') and self.filename=='publicitate.html')
  language=tag=='a' and 'language' in classes
  if language:
   a={'href':'../'+self.filename,'class':'language','lang':'lv','hreflang':'lv','data-language-switch':'true','aria-label':'Latviešu valoda'};self.skip_language=True
  else:
   for k,v in list(a.items()):
    if v is None:continue
    if k in ('href','src'):a[k]=local_link(v)
    elif k in ('aria-label','title','alt','content') and not (k=='content' and a.get('name') in ['viewport','theme-color']):a[k]=translate(v)
    elif k=='lang' and v=='lv':a[k]='en'
   if tag=='html':a['lang']='en'
  self.out.append('<'+tag+''.join(' '+k+('="'+html.escape(v,quote=True)+'"' if v is not None else '') for k,v in a.items())+'>')
  if tag not in VOID:self.stack.append((tag,protected,language))
 def handle_startendtag(self,t,a):
  self.handle_starttag(t,a)
  if t not in VOID:self.handle_endtag(t)
 def handle_endtag(self,t):
  self.out.append('</'+t+'>')
  if self.stack and self.stack[-1][0]==t:
   _,_,language=self.stack.pop()
   if language:self.skip_language=False
 def handle_data(self,s):
  if self.skip_language:
   if s.strip():self.out.append('LV')
   return
  protected=self.stack and self.stack[-1][1]
  # The data itself is translated; academic and media source titles remain original.
  self.out.append(html.escape(s if protected else translate(s),quote=False))
 def handle_entityref(self,s):self.out.append('&'+s+';')
 def handle_charref(self,s):self.out.append('&#'+s+';')
 def handle_comment(self,s):self.out.append('<!--'+s+'-->')
def translate_node(value,key=''):
 if isinstance(value,list):return [translate_node(x,key) for x in value]
 if isinstance(value,dict):return {k:translate_node(v,k) for k,v in value.items()}
 if isinstance(value,str):
  if key in ['url','corpus_url']:return local_link(value)
  if key in ['id','doi','sort_date','issued','authors_year','preview_authors_year','reference_html','tail_html']:return value
  if key=='image' and value.startswith('assets/'):return '../'+value
  return translate(value)
 return value

def build():
 en=D/'en';en.mkdir(exist_ok=True)
 for lv,english in PAGES.items():
  source=(D/lv).read_text()
  # The Latvian switch always points to the matching English page.
  source=re.sub(r'<a href="https://www.sanitareinsone.lv/en"[^>]*class="language"[^>]*>.*?</a>', '<a href="en/'+english+'" class="language" lang="en" hreflang="en" data-language-switch="true" aria-label="English">EN</a>',source)
  (D/lv).write_text(source)
  parser=EnglishHTML(lv);parser.feed(source)
  result=''.join(parser.out)
  result=result.replace('<head>','<head><link rel="alternate" hreflang="lv" href="../'+lv+'"><link rel="alternate" hreflang="en" href="'+english+'">')
  (en/english).write_text(result)
  # Reciprocal hreflang links on Latvian pages.
  (D/lv).write_text(source.replace('<head>','<head><link rel="alternate" hreflang="lv" href="'+lv+'"><link rel="alternate" hreflang="en" href="en/'+english+'">'))
 source=(D/'research.js').read_text();marker='const nodes=';start=source.index(marker)+len(marker);data,end=json.JSONDecoder().raw_decode(source[start:]);template=source[:start]+'/*RESEARCH_DATA*/'+source[start+end:]
 translated=translate_node(data)
 # Keep bibliography and media titles in their original language.
 for key,node in data.items():
  if node.get('bibliography') or key.startswith(('lsm-','lr-','media-','nature-','science-sfu')):
   translated[key]['title']=node['title']
 (en/'research.js').write_text(translate(template).replace('/*RESEARCH_DATA*/',json.dumps(translated,ensure_ascii=False)))
 for name in ['main','publicity']:(D/(name+'.en.js')).write_text(translate((D/(name+'.js')).read_text()))
 (D/'.nojekyll').write_text('')
 print('Built',len(PAGES),'English pages with matching language links.')
if __name__=='__main__':build()
