from pathlib import Path
import json,html,re,shutil
from chronology import date_key, sort_records
from projects import apply_projects, project_catalogue, status_marker
from publicity import catalogue as media_catalogue, add_media_to_graph
from academic_outreach import catalogue as academic_catalogue
from meetings import catalogue as meeting_catalogue
from publication_topics import TOPICS as PUBLICATION_TOPICS, apply_publication_topics
from bibliography import RECORDS, BY_ID, reference_html, normalize_source, apply_to_graph
D=Path('dist');S=json.loads(Path('src/data/content.json').read_text());e=html.escape
nav=[('petnieciba.html','Pētniecība'),('gramatas.html','Rakstniecība'),('kontakti.html','Kontakti')]
profile='https://research.lu.lv/lv/persons/sanita-reinsone/'
original='https://www.sanitareinsone.lv/lv/'
def a(u,t,cls=''):
 extra=' target="_blank" rel="noopener noreferrer"' if u.startswith('http') else ''
 return '<a href="'+e(u,quote=True)+'"'+extra+(' class="'+cls+'"' if cls else '')+'>'+t+'</a>'
def shell(filename,title,body,script=''):
 links=''.join('<a href="'+u+'"'+(' aria-current="page"' if filename==u else '')+'>'+t+'</a>' for u,t in nav)
 content='''<!doctype html><html lang="lv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff"><link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><meta name="description" content="Sanita Reinsone – zinātniece un rakstniece. Pētniecība, grāmatas, publikācijas un sarunas."><title>'''+e(title)+' · Sanita Reinsone</title><link rel="stylesheet" href="style.css?v=160"><script defer src="main.js?v=160"></script><script data-goatcounter="https://sanitareinsone.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script></head><body><a class="skip" href="#saturs">Uz saturu</a><div class="wrap"><header class="header"><a class="brand" href="index.html">Sanita Reinsone</a><nav id="nav" aria-label="Galvenā navigācija">'+links+'</nav><div class="header-controls">'+a('https://www.sanitareinsone.lv/en','EN ↗','language')+'<button class="menu" type="button" aria-label="Atvērt izvēlni" aria-expanded="false" aria-controls="nav"><svg class="menu-lines" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg><svg class="menu-close" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="m6 6 12 12M6 18 18 6"/></svg></button></div></header><main id="saturs">'+body+'</main><footer class="footer"><div class="footer-links">'+a('publikacijas.html','Publikācijas')+a('projekti.html','Projekti')+a('sarunas.html','Sarunas un tikšanās')+a('uzstasanas.html','Akadēmiskās uzstāšanās')+a('darbiba.html','Citas aktivitātes')+a('publicitate.html','Publicitāte')+'</div><div class="footer-bottom"><span>© 2026 Sanita Reinsone</span>'+a('index.html','Sākumlapa ↑')+'</div></footer></div><button class="back-to-top" type="button" aria-label="Uz lapas sākumu" title="Uz augšu" hidden><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg></button>'+script+'</body></html>'
 
 if filename=='index.html':
  content=content.replace('<a class="brand" href="index.html">Sanita Reinsone</a>','')
  content=content.replace('<header class="header">','<header class="header home-header">')
  content=content.replace('© 2026 Sanita Reinsone','© 2026')
 for glyph in ['↗','↑','↓','←','→']:content=content.replace(glyph,'')
 (D/filename).write_text(content.replace(chr(0x2014),chr(0x2013)))
def intro(title,kicker='',crumb=None):
 return '<section class="page-intro"><nav class="breadcrumb" aria-label="Atrašanās vieta">'+a('index.html','Sākums')+'<span>/</span>'+(a(crumb[0],e(crumb[1]))+'<span>/</span>' if crumb else '')+'<span>'+e(title)+'</span></nav>'+('<p class="kicker">'+e(kicker)+'</p>' if kicker else '')+'<h1>'+e(title)+'</h1></section>'
def paragraphs(key,indices):return ''.join(S[key]['blocks'][i]['html'] for i in indices)
def source_html(key):
 s=normalize_source(S[key]['html']) if key=='publications' else S[key]['html'];s=re.sub(r'<h1>.*?</h1>','',s,count=1,flags=re.S)
 if key in ('projects','publications','outreach'):
  def newest_list(match):
   items=re.findall(r'<li>.*?</li>',match[1],flags=re.S)
   return '<ul>'+''.join(sorted(items,key=lambda item:date_key(re.sub(r'<[^>]+>',' ',item)),reverse=True))+'</ul>' if items else match[0]
  s=re.sub(r'<ul>(.*?)</ul>',newest_list,s,flags=re.S)
 return s
def content_sections(key,start_tag='h2'):
 # The first heading anchors the content after the old site's table of contents.
 s=source_html(key);idx=s.find('<'+start_tag+'>')
 return s[idx:] if idx>=0 else s
research_titles=[('infrastructure', 'Digitālās humanitārās zinātnes un pētniecības infrastruktūra'), ('memory', 'Atmiņu mantojums un dzīves pierakstīšana'), ('folklore', 'Folkloras arhīvi un digitālā folkloristika'), ('language', 'Valodu tehnoloģijas'), ('participation', 'Zinātne un sabiedrība')]
def themes():return '<div class="theme-grid">'+''.join(a('petnieciba.html#'+id,'<h3>'+t+'</h3>','theme-tile') for id,t in research_titles)+'</div>'
def bookcard(id,title,meta,img,cover=False):return a(id+'.html','<div class="book-image'+(' cover' if cover else '')+'"><img src="assets/'+img+'" alt="'+e(title)+'" loading="lazy"></div><p class="meta">'+e(meta)+'</p><h3>'+e(title)+' ↗</h3>','book-card')
def doccard(id,title,sub,meta):return a(id+'.html','<img class="document-cover" src="assets/'+('meza-meitas-cover.png' if id=='meza-meitas' else 'adama-stasts-book.png')+'" alt="'+e(title)+' – grāmata" loading="lazy"><p class="meta">'+e(meta)+'</p><h3>'+e(title)+' ↗</h3><p>'+e(sub)+'</p>','document-card')
bookgrid='<div class="book-grid">'+bookcard('draugi-un-kaimini','Draugi un kaimiņi','2024 · Jānis Roze','book4.jpg')+bookcard('kus-mul-patarei','Kus mul patarei!','2017 · Liels un Mazs','book8.jpg',True)+'</div>'
docgrid='<div class="document-grid">'+doccard('meza-meitas','Meža meitas','12 sievietes par dzīvi mājās, mežā, cietumā','2015 / 2022 · Dienas Grāmata')+doccard('adama-stasts','Ādama stāsts','Mazsalaciešu dzīve, tikumi un ieradumi Ā. Purmaļa autobiogrāfijā 19. un 20. gs. mijā','2008 / 2011 · Zinātne')+'</div>'
science_intro=S['home']['blocks'][5]['text'].split(' Līdztekus pētniecībai')[0]
children_link=a('gramatas.html#bernu-literatura','<span>Bērnu literatūra</span><svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M7 13 5 4l9 6h4l9-6-2 9c2 2 3 4 3 7 0 6-6 9-12 9S4 26 4 20c0-3 1-5 3-7Z"/><path d="M11 17v2m10-2v2m-7 3 2 2 2-2m-2 2v2M2 20l7 1m-7 4 7-1m21-4-7 1m7 4-7-1"/></svg>','children-link')
current_role='Strādāju LU Humanitāro zinātņu fakultātē kā asociētā tenūrprofesore un Digitālo humanitāro zinātņu centra vadītāja.'
home='<section class="hero has-portrait"><div class="hero-main"><h1 class="hero-title">Sanita Reinsone</h1><div class="hero-intro">'+'<p>'+e(science_intro)+'</p><p class="current-role">'+e(current_role)+'</p><div class="hero-links">'+a(profile,'<span>Akadēmiskais profils</span><svg class="external-link-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg>','text-link external-resource-link')+children_link+'</div>'+'</div></div><figure class="intro-photo"><div class="intro-photo-crop"><img src="assets/portrait-brown-original.png" alt="Sanita Reinsone" width="1200" height="1722" fetchpriority="high"></div></figure></section>'
home+='<section class="section"><div class="section-head"><h2>Pētniecība</h2></div>'+themes()+'</section>'


home+='<section class="section"><div class="section-head"><h2>Akadēmiskās uzstāšanās</h2>'+a('uzstasanas.html','Visas akadēmiskās uzstāšanās')+'</div>'
for date,kind,title,url in sorted([
 ('14.06.2026 · Reikjavīka','Priekšlasījums · ISFNR2026','Restless Spirits, Restless Places: Landscape Agency in Smiltene’s Demonological Heritage','https://nomadit.co.uk/conference/isfnr2026/paper/92419'),
 ('26.05.2026 · Roma','Plenārdiskusija · DARIAH Annual Event','Digital Arts and Humanities With and For Society: Building Infrastructures of Engagement','https://www.dariah.eu/news/dariah-annual-event-2026-call-for-papers-now-open'),
 ('13.–16.06.2026 · Reikjavīka','Plakātreferāts · ISFNR2026 · Sanita Reinsone un līdzautori','Digital Infrastructures for Folk Narrative Research: Mapping Northern European Resources','https://nomadit.co.uk/conference/isfnr2026/paper/92373'),
 ('05.03.2026 · Rīga','Priekšlasījums · CLARIN–DARIAH pavasara konference','Ceļā uz DARIAH-LV','https://digitalhumanities.lv/en/events/clarin-dariah-spring-conference-2026/')],key=lambda item:date_key(item[0]),reverse=True):
 home+=a(url,'<span class="meta">'+e(date)+'</span><div><span class="kind">'+e(kind)+'</span><h3>'+e(title)+'</h3></div>','wide-row')
home+='</section>'
home+='<section class="section project-update" aria-labelledby="spotlight-title"><p class="kicker">Jauna iniciatīva</p><h2 id="spotlight-title"><a href="https://researchgames.eu/" target="_blank" rel="noopener noreferrer" aria-label="ResearchGames.eu – atvērt jaunā cilnē"><img class="researchgames-logo" src="assets/researchgames-logo-black.png" alt="ResearchGames.eu" width="1120" height="205" loading="lazy"></a></h2><p class="spotlight-themes">Zinātnes komunikācija · Sabiedrības iesaiste</p><p>Digitālā platforma, kur pētījumi un datu kopas pārtop interaktīvās spēlēs.</p><div class="hero-links">'+a('https://researchgames.eu/','<span>ResearchGames.eu</span><svg class="external-link-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg>','text-link rg-external-link')+'</div></section>'
shell('index.html','Sākums',home)
# Research graph generated from the shared records, preserving source titles.
research_data=sort_records(apply_projects(apply_to_graph(apply_publication_topics(add_media_to_graph(json.loads(Path('src/data/research-records.json').read_text())),RECORDS))))
research_js=Path('src/research-graph-template.js').read_text().replace('/*RESEARCH_DATA*/',json.dumps(research_data,ensure_ascii=False))
(D/'research.js').write_text(research_js.replace(chr(0x2014),chr(0x2013)))
research='<div id="sr-research-world" lang="lv"><div class="world-content"></div></div>'
shell('petnieciba.html','Pētniecība',research,'<script src="research.js?v=160"></script>')
meeting_photos='<div class="meeting-photos"><figure><img src="assets/book0.jpg" alt="Sanita Reinsone Jāņa Baltvilka balvas nominantu lasījumos" loading="lazy"><figcaption>Jāņa Baltvilka balvas nominantu lasījumos, 2025. gada jūlijā. Foto: Evija Trifanova</figcaption></figure><figure><img src="assets/book1.jpg" alt="Sanita Reinsone tiekas ar lasītājiem Jūrmalas Centrālajā bibliotēkā" loading="lazy"><figcaption>Jūrmalas Centrālajā bibliotēkā, 2024. gada decembrī.</figcaption></figure></div>'
# Writing: original introductory text and complete book descriptions.
shell('gramatas.html','Rakstniecība',intro('Rakstniecība')+'<div class="writing-intro-row"><div class="page-lead">'+paragraphs('books',[1])+'</div><figure class="writing-illustration"><img src="assets/aleksandra-runde-illustration.png" alt="Aleksandras Rundes grāmatas ilustrācija: divi bērni ar ķerru." width="902" height="522" fetchpriority="high"><figcaption>Māksliniece: Aleksandra Runde<br><cite>Draugi un kaimiņi</cite></figcaption></figure></div><section class="section">'+'<h2 id="bernu-literatura">Bērnu literatūra</h2>'+bookgrid+'</section><section class="section"><div class="section-head"><h2>Dokumentālā literatūra</h2></div>'+docgrid+'</section><section class="section"><div class="section-head"><h2>Tikšanās ar lasītājiem</h2></div><div class="page-lead">'+paragraphs('books',[2])+'</div>'+meeting_photos+a('sarunas.html','Skolās un bibliotēkās ↗','text-link')+'</section>')
awards=''.join('<p>'+e(S['books']['blocks'][i]['text'].replace('✨','').strip())+'</p>' for i in range(7,11))
body=intro('Draugi un kaimiņi','Bērnu literatūra',('gramatas.html','Grāmatas'))+'<section class="page-body book-detail"><figure class="visual"><img src="assets/book4.jpg" alt="Draugi un kaimiņi – grāmata pie koka"><figcaption class="caption">Foto: laligaba.lv</figcaption></figure><div class="prose"><p class="meta">Sanita Reinsone (teksts)<br>Aleksandra Runde (ilustrācijas)<br>Jānis Roze, 2024</p>'+paragraphs('books',[12,13,14])+'<div class="awards"><h2>Apbalvojumi un nominācijas</h2>'+awards+'</div></div></section><div class="gallery"><img src="assets/book6.jpg" alt="Grāmatas Draugi un kaimiņi atvērums" loading="lazy"><img src="assets/book7.jpg" alt="Aleksandras Rundes ilustrācija grāmatā Draugi un kaimiņi" loading="lazy"></div><p class="caption">Ilustrācijas: Aleksandra Runde</p><section class="section">'+a('sarunas.html','Tikšanās ar lasītājiem ↗','text-link')+'</section>'
shell('draugi-un-kaimini.html','Draugi un kaimiņi',body)
body=intro('Kus mul patarei!','Bērnu literatūra',('gramatas.html','Grāmatas'))+'<section class="page-body book-detail"><figure class="visual"><img src="assets/book8.jpg" alt="Kus mul patarei! Kā Igaunijas leļļi bēga uz Latviju – grāmatas vāks"></figure><div class="prose"><h2>Kā Igaunijas leļļi bēga uz Latviju</h2><p class="meta">Sanita Reinsone (teksts)<br>Kristīne Jurjāne (ilustrācijas)<br>Liels un Mazs, 2017</p>'+paragraphs('books',[24])+'</div></section><div class="gallery"><img src="assets/book9.jpg" alt="Kristīnes Jurjānes ilustrācija grāmatā Kus mul patarei!" loading="lazy"><img src="assets/book10.jpg" alt="Grāmatas Kus mul patarei! atvērums" loading="lazy"></div><p class="caption">Ilustrācijas: Kristīne Jurjāne</p>'
shell('kus-mul-patarei.html','Kus mul patarei!',body)
for file,title,i in [('meza-meitas.html','Meža meitas',84),('adama-stasts.html','Ādama stāsts',86)]:
 if file=='adama-stasts.html':
  image='adama-stasts-book.png'
  related='<section class="book-related"><h2>Kolekcija un izrāde</h2>'+a('https://garamantas.lv/lv/collection/1119253/Adama-Purmala-dzivesstasts','Ādama Purmaļa dzīvesstāsts · Autobiogrāfiju krājums','book-related-link')+a('https://teatris.lv/izrade/adama-stasts/','Ādama stāsts · Latvijas Nacionālais teātris','book-related-link')+'</section>'
 else:
  image='meza-meitas-cover.png'
  related='<section class="book-related"><h2>Teātris un Radioteātris</h2>'+a('https://replay.lsm.lv/lv/skaties/ieraksts/ltv/196057/teatriszip-par-valmieras-teatra-izradi-meza-meitas','Meža meitas · Valmieras teātra izrāde · Teātris.zip','book-related-link')+a('https://radioteatris.lsm.lv/lv/radio-teatris/raidijumi/meza-meitas/','Meža meitas · Latvijas Radio Radioteātris','book-related-link')+'<div class="book-audio-parts">'+a('https://replay.lsm.lv/lv/klausies/ieraksts/lr/188906/valmieras-dramas-teatra-izrade-meza-meitas-1-dala','Klausīties 1. daļu')+a('https://replay.lsm.lv/lv/klausies/ieraksts/lr/188907/valmieras-dramas-teatra-izrade-meza-meitas-2-dala','Klausīties 2. daļu')+'</div></section>'
 body=intro(title,'Dokumentālā literatūra',('gramatas.html','Grāmatas'))+'<section class="page-body book-detail"><figure class="visual"><img src="assets/'+image+'" alt="'+e(title)+' – grāmata"></figure><div class="prose">'+paragraphs('publications',[i])+related+'<div class="approach-links">'+a('petnieciba.html#memory','Atmiņu mantojums un dzīves pierakstīšana')+a('gramatas.html','Visas grāmatas')+'</div></div></section>'
 shell(file,title,body)
# Wider academic/civic work remains available separately.
# The About page is removed after preserving its unique professional history below.
(D/'par-mani.html').unlink(missing_ok=True)
acts=content_sections('activities')
for text,id in [('Brīvprātīgās iniciatīvas un zinātnes aktīvisms','iniciativas'),('Dalība padomēs un ekspertīze','padomes'),('Pētniecības tīkli un asociācijas','tikli'),('Apbalvojumi un pagodinājumi','apbalvojumi'),('Pasākumu organizēšana','organizesana')]:
 acts=re.sub(r'<h2[^>]*>(.*?)</h2>',lambda m:'<h2 id="'+id+'">'+text+'</h2>' if html.unescape(re.sub(r'<[^>]+>','',m[1])).strip()==text else m[0],acts,flags=re.S)
activity_parts=re.split(r'(<h2[^>]*>.*?</h2>)',acts,flags=re.S)
acts=activity_parts[0]
for i in range(1,len(activity_parts),2):
 heading=activity_parts[i];body=activity_parts[i+1]
 match=re.search(r' id="([^"]+)"',heading);anchor=match[1] if match else ''
 heading=re.sub(r' id="[^"]+"','',heading)
 acts+='<details class="activity-group" id="'+anchor+'"><summary>'+heading+'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></summary><div class="activity-group-content">'+body+'</div></details>'
shell('darbiba.html','Citas aktivitātes',intro('Citas aktivitātes')+'<section class="page-body activities-page"><div class="source-content">'+acts+'</div></section>')
# Compact project catalogue first; related platforms remain available below it.
profile_arrow='<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'
profile_top='<div class="catalogue-profile">'+a(profile,'Akadēmiskais profils'+profile_arrow,'external-resource-link')+'<span>Plašāka informācija: research.lu.lv</span></div>'
resources='<details class="supporting-resources"><summary>Digitālās platformas un resursi</summary><div class="resource-grid">'+''.join(a(research_data[id]['url'],'<h3>'+e(research_data[id]['title'])+'</h3><p>'+e(research_data[id].get('meta',''))+'</p>'+'<span class="meta">'+e(research_data[id]['type'])+status_marker(research_data[id].get('past_label',''))+'</span>','resource-card') for id in ['digitalhumanities','teikas','researchgames','autobiography','humma-platform','garamantas','iesaisties','pasakas'])+'</div></details>'
activities='<details class="supporting-resources"><summary>Sabiedriskās zinātnes aktivitātes</summary>'+''.join(a(research_data[id]['url'],'<h3>'+e(research_data[id]['title'])+'</h3><p>'+e(research_data[id].get('meta',''))+'</p>','resource-card') for id in ['balsutalka','pandemic-diaries-campaign','autobiography-campaign','iesaisties-campaigns','simtgades-burtnieki'])+'</details>'
shell('projekti.html','Projekti',intro('Projekti','',('petnieciba.html','Pētniecība')).replace('class="page-intro"','class="page-intro catalogue-intro"')+profile_top+'<section class="page-body compact-projects">'+project_catalogue()+resources+'</section>')
# Complete collected bibliography, newest first, with all thematic mappings.
publications=sorted(RECORDS,key=lambda r:date_key(r.get('issued') or r['year']),reverse=True)
rows=''
for record in publications:
 id=record['id'];assignment=PUBLICATION_TOPICS[id]
 topic_links=''.join(a('petnieciba.html?tema='+theme+'#'+id,dict(research_titles)[theme]) for theme in assignment['themes'])
 rows+='<article class="wide-row publication-row" id="'+id+'"><div class="publication-year-type"><span class="meta">'+str(record['year'])+'</span><span class="kind">'+e(assignment['type'])+'</span></div><div><p class="bibliography-reference">'+reference_html(record)+'</p><nav class="publication-topics" aria-label="Publikācijas tēmas">'+topic_links+'</nav></div><span></span></article>'
shell('publikacijas.html','Publikācijas',intro('Publikācijas','',('petnieciba.html','Pētniecība')).replace('class="page-intro"','class="page-intro catalogue-intro"')+profile_top+'<section class="page-body compact-publications">'+rows+'<div class="research-links">'+a(profile,'Akadēmiskais profils ↗')+'</div></section>')

# Every collected reader meeting and public event, grouped compactly by year.
shell('sarunas.html','Sarunas un tikšanās',intro('Sarunas un tikšanās','Skolās, bibliotēkās un citviet')+'<section class="page-body"><div class="page-lead">'+paragraphs('books',[2])+'</div><div class="research-links">'+a('mailto:sanita.reinsone@lu.lv','sanita.reinsone@lu.lv')+'</div><div class="meetings-catalogue">'+meeting_catalogue()+'</div>'+'<div class="research-links">'+a('publicitate.html','Publicitāte medijos')+a('uzstasanas.html','Akadēmiskās uzstāšanās')+'</div></section>')
# Public-facing media and academic contributions have separate catalogues and URLs.
feature=research_data['scienceforukraine']['feature']
feature_html='<aside class="media-feature media-feature--page" data-publicity-feature="research ukraine"><div><p class="media-feature-label">'+e(feature['label'])+'</p><h3>'+a(feature['url'],e(feature['title']))+'</h3><p class="meta">'+e(feature['meta'])+'</p></div><figure><a href="assets/nature-scienceforukraine-full.png" target="_blank" rel="noopener noreferrer" aria-label="Atvērt Nature attēlu pilnā izmērā"><img src="assets/nature-scienceforukraine-full.png" alt="Nature raksta atvērums ar virsrakstu un Sanitas Reinsones portretu, 11.09.2024." width="1280" height="646" loading="eager"></a><figcaption>11.09.2024. · Foto: Inga Pizāne</figcaption></figure></aside>'
subnav='<nav class="outreach-nav" aria-label="Materiālu veids"><a href="publicitate.html" aria-current="page">Publicitāte medijos</a><a href="uzstasanas.html">Akadēmiskās uzstāšanās</a></nav>'
shell('publicitate.html','Publicitāte',intro('Publicitāte')+subnav+'<section class="page-body">'+feature_html+media_catalogue()+'</section>','<script defer src="publicity.js?v=160"></script>')
subnav='<nav class="outreach-nav" aria-label="Materiālu veids"><a href="publicitate.html">Publicitāte medijos</a><a href="uzstasanas.html" aria-current="page">Akadēmiskās uzstāšanās</a></nav>'
shell('uzstasanas.html','Akadēmiskās uzstāšanās',intro('Akadēmiskās uzstāšanās','Pētniecība')+subnav+'<section class="page-body">'+academic_catalogue(S['outreach']['blocks'],research_data)+'<div class="research-links">'+a('petnieciba.html','Uzstāšanās pētniecības tēmās')+a(profile,'Akadēmiskais profils')+'</div></section>')
shell('kontakti.html','Kontakti',intro('Kontakti')+'<section class="page-body">'+a('mailto:sanita.reinsone@lu.lv','sanita.reinsone@lu.lv ↗','contact-address')+'<div class="social-links">'+a(profile,'research.lu.lv ↗')+a('https://orcid.org/0000-0003-1980-5450','ORCID ↗')+a('https://www.linkedin.com/in/sanita-reinsone/','LinkedIn ↗')+'</div></section>')
print('Built',len(list(D.glob('*.html'))),'pages; original portrait copied unchanged.')

from build_english import build as build_english
build_english()
