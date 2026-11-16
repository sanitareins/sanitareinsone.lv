"""English interface and descriptive copy. Source titles and personal names stay original."""
import json,re
from pathlib import Path
# Longest phrases take precedence; never apply to URLs or identifiers.
PAIRS='''
Digitālās humanitārās zinātnes un pētniecības infrastruktūra	Digital humanities and research infrastructure
Atmiņu mantojums un dzīves pierakstīšana	Memory heritage and life writing
Folkloras arhīvi un digitālā folkloristika	Folklore archives and digital folkloristics
Valodu tehnoloģijas	Language technologies
Zinātne un sabiedrība	Science and society
Plenārrunas un aicinātas uzstāšanās	Keynote and invited presentations
Referāti, plenārdiskusijas un plakātreferāti	Conference papers, plenary discussions and posters
Publiskas lekcijas, semināri un diskusijas	Public lectures, workshops and discussions
Publiskas lekcijas un semināri	Public lectures and workshops
Brīvprātīgās iniciatīvas un zinātnes aktīvisms	Voluntary initiatives and science activism
Dalība padomēs un ekspertīze	Boards, advisory roles and expertise
Pētniecības tīkli un asociācijas	Research networks and associations
Apbalvojumi un pagodinājumi	Awards and honours
Pasākumu organizēšana	Event organisation
Sabiedriskās zinātnes aktivitātes	Citizen science activities
Sabiedrības iesaiste un sabiedriskā zinātne	Public engagement and citizen science
Zinātnes aktīvisms un solidaritāte	Science activism and solidarity
Platformas, digitālie resursi un krājumi	Platforms, digital resources and collections
Digitālie resursi un krājumi	Digital resources and collections
Digitālās platformas un resursi	Digital platforms and resources
Pētniecības infrastruktūras	Research infrastructures
Pētniecības infrastruktūra	Research infrastructure
Pētniecības un attīstības projekti	Research and development projects
Notiekošie projekti	Current projects
Noslēgušies projekti	Completed projects
Noslēdzies projekts	Completed project
Agrākā darbība šajā resursā	Former involvement in this resource
Latviešu folkloras krātuves Autobiogrāfiju krājums	Autobiography Collection of the Archives of Latvian Folklore
LU Digitālo humanitāro zinātņu centrs	Digital Humanities Centre, University of Latvia
CLARIN Latvija	CLARIN Latvia
Akadēmiskais profils	Academic profile
Visas akadēmiskās uzstāšanās	All academic presentations
Akadēmiskās uzstāšanās	Academic presentations
Uzstāšanās pētniecības tēmās	Presentations by research theme
Sarunas un tikšanās	Talks and meetings
Tikšanās, lasījumi un sarunas	Meetings, readings and conversations
Tikšanās ar lasītājiem	Meetings with readers
Skolās, bibliotēkās un citviet	In schools, libraries and elsewhere
Skolās un bibliotēkās	In schools and libraries
Bērnu literatūra	Children’s literature
Dokumentālā literatūra	Documentary writing
Citas aktivitātes	Other activities
Publicitāte medijos	Media coverage
Publicitāte	Media coverage
Publikācijas	Publications
Pētniecība	Research
Rakstniecība	Creative Writing
Kontakti	Contact
Projekti	Projects
Sākumlapa	Home
Sākums	Home
Saistītās tēmas	Related themes
Saistītie resursi	Related resources
Darbības virzieni	Areas of activity
Datu kopas	Datasets
Datu kopa	Dataset
Uzstāšanās	Presentations
Iniciatīvas	Initiatives
Lomas	Roles
Loma	Role
Centrs	Centre
Infrastruktūras attīstība	Infrastructure development
Infrastruktūra	Infrastructure
Rīki	Tools
Rīks	Tool
Sabiedriskā zinātne / citizen science	Citizen science
Sabiedriskā zinātne Latvijā	Citizen science in Latvia
Sabiedriskā zinātne un DH	Citizen science and DH
Sabiedriskā zinātne	Citizen science
Zinātnes komunikācija	Science communication
Sabiedrības iesaiste	Public engagement
Jauna iniciatīva	New initiative
Digitālā platforma, kur pētījumi un datu kopas pārtop interaktīvās spēlēs.	A digital platform turning research and datasets into interactive games.
Iniciatīva un digitālā platforma	Initiative and digital platform
Sadarbības platforma	Collaboration platform
Digitālā platforma	Digital platform
Digitāls resurss	Digital resource
Digitālais resurss	Digital resource
Krājums	Collection
Projekts un krājums	Project and collection
Projekts	Project
Projekta mājaslapa	Project website
Finansētāja projekta apraksts	Funder’s project description
Par projektu	About the project
Pilnais nosaukums	Full title
Projekta numurs	Project number
Finansētājs	Funder
Finansējums	Funding
Programma	Programme
Periods	Period
Koordinators	Coordinator
Mana loma	My role
LU loma	University of Latvia’s role
Partneri	Partners
Galvenā izpildītāja, institucionālā koordinatore	Principal investigator, institutional coordinator
Latvijas partnerības koordinatore	Latvian partnership coordinator
Vadošā izpildītāja un LFMI koordinatore	Lead investigator and ILFA coordinator
Grupas vadītāja, vadošā pētniece	Group leader, senior researcher
Projekta vadītāja līdz 2024. gada maijam	Project lead until May 2024
Projekta vadītāja	Project lead
Vadošā pētniece	Senior researcher
Zinātnes komunikācijas vadītāja	Science communication manager
Lektore	Lecturer
Eiropas Savienības Atveseļošanas un noturības mehānisms; valsts budžets	EU Recovery and Resilience Facility; national budget
Eiropas Reģionālās attīstības fonds	European Regional Development Fund
Latvijas Zinātnes padome	Latvian Council of Science
LR Izglītības un zinātnes ministrija	Ministry of Education and Science of Latvia
Valsts pētījumu programma	National research programme
Eiropas Savienība	European Union
Latvijas Universitāte	University of Latvia
Atvērtās zināšanu ekosistēmas sabiedriskās zinātnes attīstībai	Open knowledge ecosystems for the development of citizen science
Latviskā identitāte un zināšanu stratēģijas kā sabiedrības noturības resurss	Latvian identity and knowledge strategies as a resource for societal resilience
Digitālie resursi un mākslīgā intelekta tehnoloģijas latviešu valodas ilgtspējai	Digital resources and artificial intelligence technologies for the sustainability of Latvian
Latvijas 20.–21. gadsimta vēsture: sociālā morfoģenēze, mantojums un izaicinājumi	Latvian history in the 20th and 21st centuries: social morphogenesis, legacy and challenges
Latvijas 20.–21. gadsimta vēsture	Latvian history in the 20th and 21st centuries
Atvērtas un FAIR principiem atbilstīgas digitālo humanitāro zinātņu ekosistēmas attīstība Latvijā	Development of an open and FAIR digital humanities ecosystem in Latvia
Valodu tehnoloģiju iniciatīva	Language technology initiative
Mūsdienu latviešu valodas izpēte un valodas tehnoloģiju attīstība	Research on contemporary Latvian and development of language technologies
Digitālie resursi humanitārajām zinātnēm: integrācijas un attīstība	Digital resources for the humanities: integration and development
Digitālie resursi humanitārajām zinātnēm	Digital resources for the humanities
Sevis dokumentēšana: inovatīvi modeļi autobiogrāfiskā naratīva interpretācijā un izpratnē	Documenting the self: innovative models for interpreting and understanding autobiographical narrative
Stiprinot zināšanu sabiedrību: starpdisciplināras pieejas sabiedrības iesaistei digitālā kultūras mantojuma radīšanā	Empowering a knowledge society: interdisciplinary approaches to public involvement in the production of digital cultural heritage
Stiprinot zināšanu sabiedrību	Empowering a knowledge society
Kultūras mantojums apdraudējuma apstākļos	Cultural heritage at risk
Centra vadītāja. Pētniecība, izglītība, digitālās infrastruktūras attīstība un starptautiskā sadarbība.	Head of the centre. Research, education, digital infrastructure development and international collaboration.
Digitālās humanitārās zinātnes Latvijā.	Digital humanities in Latvia.
Digitālā pētniecības infrastruktūra mākslas un humanitārajām zinātnēm.	Digital research infrastructure for the arts and humanities.
Valodas resursu un tehnoloģiju infrastruktūra.	Infrastructure for language resources and technologies.
Latviešu tautas teiku meklēšanai, analīzei un kartēšanai. Pētera Šmita krājuma digitālā platforma. Resurss izstrādē.	A platform for searching, analysing and mapping Latvian folk legends from Pēteris Šmits’s collection. Resource under development.
Sabiedrības iesaiste runas datu vākšanā un pārbaudē latviešu valodas tehnoloģijām.	Public participation in collecting and validating speech data for Latvian language technologies.
Sabiedriskās zinātnes iniciatīvas humanitārajās un mākslas zinātnēs.	Citizen science initiatives in the humanities and arts.
Sadarbības platforma humanitārajām un mākslas zinātnēm Latvijā.	A collaboration platform for the humanities and arts in Latvia.
Krājumā ietilpst arī Pandēmijas dienasgrāmatas.	The collection also includes the Pandemic Diaries.
Sabiedrības iesaiste autobiogrāfisko materiālu vākšanā, digitalizēšanā un rokrakstu atšifrēšanā.	Public participation in collecting and digitising autobiographical materials and transcribing manuscripts.
Sabiedrības iesaiste humanitāro un mākslas zinātņu pētījumos: manuskriptu pārrakstīšana, ieskaņošana un materiālu papildināšana.	Public participation in humanities and arts research: transcribing manuscripts, making recordings and enriching collections.
Aicinājums rakstīt un iesūtīt dienasgrāmatas par ikdienas pieredzi pandēmijā.	A call to write and submit diaries documenting everyday experiences during the pandemic.
Folkloras manuskriptu atšifrēšanas kampaņa.	A campaign to transcribe folklore manuscripts.
Autobiogrāfiju krājuma kampaņas	Autobiography Collection campaigns
Pandēmijas dienasgrāmatu kampaņa	Pandemic Diaries campaign
iesaisties.lv kampaņas	iesaisties.lv campaigns
Pandēmijas dienasgrāmatas	Pandemic Diaries
ECSA sabiedriskās zinātnes vēstniece Latvijā	ECSA Citizen Science Ambassador for Latvia
LU zinātnes vēstniece	University of Latvia science ambassador
Agrākā loma	Former role
Pašreizējā loma	Current role
savienot cilvēkus, zinātni un mākslu	connecting people, science and art
Plenārdiskusija	Plenary discussion
Keynote referāts	Keynote presentation
Plakātreferāts	Conference poster
Priekšlasījums	Conference presentation
Profesionāla sesija	Professional session
Priekšlasījuma ieraksts	Presentation recording
Referāts konferences programmā	Presentation in the conference programme
Posters konferences programmā	Poster in the conference programme
SIEF programma un tēzes	SIEF programme and abstracts
Konferences programma	Conference programme
Konferences mājaslapa	Conference website
DARIAH atklāšanas diskusijas programma	DARIAH opening discussion programme
Atvērt avotu	View source
Analizēt korpusu	Explore corpus
Aizvērt detaļas	Close details
Aizvērt	Close
Sakļaut tēmu	Collapse theme
Rādīt mazāk	Show less
Rādīt pārējos	Show more
Saistītie materiāli	Related materials
saistītie materiāli atvērti.	related materials opened.
saistītie materiāli	related materials
Intervijas un portreti	Interviews and profiles
Radio un raidieraksti	Radio and podcasts
Raksti, recenzijas un ziņas	Articles, reviews and news
Televīzija un video	Television and video
Visi	All
Intervija	Interview
Portrets	Profile
Radio saruna	Radio discussion
Raidieraksts	Podcast
TV sižets	TV report
Vēstule redakcijai	Letter to the editor
Zinātnisks raksts	Research article
Nodaļa grāmatā	Book chapter
Monogrāfija	Monograph
Priekšvārds	Preface
Recenzija	Review
Pozīcijas dokuments	Position paper
Vadlīnijas	Guidelines
Ziņojumi	Reports
Ziņojums	Report
Raksti kultūras medijos	Writing in cultural media
Publikācija	Publication
Ziņa par balvu	Award news
Ziņa par grāmatu	Book news
Ziņa par iestudējumu	Theatre news
Ziņa par nomināciju	Nomination news
Ziņa par pētījumu	Research news
Ziņa par tikšanos	Meeting report
Pasākuma pieteikums	Event announcement
Ziņa	News
Raksts	Article
Saruna	Conversation
LSM.lv Kultūras redakcija	LSM.lv Culture desk
LSM.lv Ziņu redakcija	LSM.lv News desk
Plašāka informācija: research.lu.lv	More information: research.lu.lv
Apbalvojumi un nominācijas	Awards and nominations
Visas grāmatas	All books
Grāmatas	Books
Māksliniece: Aleksandra Runde	Illustrator: Aleksandra Runde
Ilustrācijas: Aleksandra Runde	Illustrations: Aleksandra Runde
Ilustrācijas: Kristīne Jurjāne	Illustrations: Kristīne Jurjāne
Sanita Reinsone (teksts)	Sanita Reinsone (text)
Aleksandra Runde (ilustrācijas)	Aleksandra Runde (illustrations)
Kristīne Jurjāne (ilustrācijas)	Kristīne Jurjāne (illustrations)
Foto:	Photo:
Teātris un Radioteātris	Theatre and radio theatre
Kolekcija un izrāde	Collection and theatre production
Latvijas Nacionālais teātris	Latvian National Theatre
Latvijas Radio Radioteātris	Latvian Radio Theatre
Valmieras teātra izrāde	Valmiera Theatre production
Ādama Purmaļa dzīvesstāsts	Ādams Purmalis’s life story
Autobiogrāfiju krājums	Autobiography Collection
Klausīties 1. daļu	Listen to part 1
Klausīties 2. daļu	Listen to part 2
12 sievietes par dzīvi mājās, mežā, cietumā	12 women on life at home, in the forest and in prison
Mazsalaciešu dzīve, tikumi un ieradumi Ā. Purmaļa autobiogrāfijā 19. un 20. gs. mijā	Life, customs and habits in Mazsalaca in Ā. Purmalis’s autobiography at the turn of the 20th century
Kā Igaunijas leļļi bēga uz Latviju	How Estonian dolls escaped to Latvia
Skola / divas mācību stundas	School
Skola / sākumskola	School / primary classes
Skola / tikšanās ar autori	School / author visit
Tikšanās ar skolēniem Briselē: Uccle	Meeting with students in Brussels: Uccle
Tikšanās ar sākumskolas skolēniem Briselē: Berkendael	Meeting with primary school students in Brussels: Berkendael
Tikšanās ar skolēniem	Meeting with students
Tikšanās bibliotēkā	Library meeting
Tikšanās ar jauniešiem par folkloru, apmaldīšanos un pētniecību	Meeting with young people about folklore, getting lost and research
Saruna par “Meža meitām” un atmiņu dokumentēšanu	Discussion about “Meža meitas” and documenting memories
Saruna par dienasgrāmatām	Discussion about diaries
Bibliotēka / atklāšanas pasākums	Library / opening event
Bibliotēka / tikšanās ar autori	Library / author visit
Bibliotēka	Library
Literāri lasījumi	Literary readings
Prozas lasījumi	Prose readings
Literatūras festivāls	Literature festival
Grāmatu svētki	Book festival
Skolēnu apmeklējums	Student visit
Skolēnu seminārs	Student workshop
Profesionāla lekcija	Professional lecture
Profesionāls seminārs	Professional seminar
Praktisks seminārs	Practical workshop
Publisks seminārs	Public workshop
Sabiedriskās zinātnes pasākums	Citizen science event
Muzejs / profesionāla diskusija	Museum / professional discussion
Muzejs / seminārs	Museum / workshop
Paneļdiskusija	Panel discussion
Stāstu vakars	Storytelling evening
Ukrainas stāstu vakars	Ukrainian storytelling evening
Tiešsaistes lekcija vēsturniekiem	Online lecture for historians
Tiešsaistē; vēsturnieku auditorija	Online; audience of historians
Tiešsaistē	Online
tiešsaistē	online
Norvēģu seminārs	Norwegian seminar
Reģionālo muzeju simpozijs	Regional museums symposium
Ceļā uz DARIAH-LV	Towards DARIAH-LV
CLARIN–DARIAH pavasara konference	CLARIN–DARIAH Spring Conference
uzaicināta plenārdiskusijas dalībniece	invited plenary panellist
līdzorganizatore un runātāja	co-organiser and speaker
līdzdalībniece (Researcher)	contributor (researcher)
un līdzautori	and co-authors
Rīga	Riga
Reikjavīka	Reykjavík
Islande	Iceland
Islandē	Iceland
Roma	Rome
Viļņa	Vilnius
Lietuva	Lithuania
Lietuvā	Lithuania
Latvija	Latvia
Igaunija	Estonia
Iguanija	Estonia
Getingene	Göttingen
Vācija	Germany
Vācijā	Germany
Portugāle	Portugal
Koimbra	Coimbra
Madride	Madrid
Spānija	Spain
Somija	Finland
Bangkoka	Bangkok
Taizeme	Thailand
Aberdīna	Aberdeen
Skotija	Scotland
Apvienotā Karaliste	United Kingdom
Timišoara	Timișoara
Rumānija	Romania
Uz saturu	Skip to content
Galvenā navigācija	Main navigation
Atrašanās vieta	Breadcrumb
Izvēlne +	Menu +
Izvēlne	Menu
Uz lapas sākumu	Back to top
Uz augšu	Back to top
Publikācijas tēmas	Publication themes
Atvērt Nature attēlu pilnā izmērā	Open the Nature image at full size
ResearchGames.eu – atvērt jaunā cilnē	ResearchGames.eu – open in a new tab
Šobrīd	Current
Iepriekš	Previous
kopš 2026. gada	since 2026
kopš 2025. gada	since 2025
kopš 2021	since 2021
kopš 2020	since 2020
kopš 2014	since 2014
Nr.	No.
'''
TRANSLATIONS=dict(line.split('\t',1) for line in PAIRS.strip().splitlines())
S=json.loads(Path('src/data/content.json').read_text())
def block(section,i,english):TRANSLATIONS[S[section]['blocks'][i]['text']]=english
block('home',5,'I am a humanities researcher interested in digital humanities, digital cultural heritage, citizen science and participatory research methods. I also study folklore, life-writing traditions and oral history. Alongside my research, I write children’s literature.')
TRANSLATIONS[S['home']['blocks'][5]['text'].split(' Līdztekus pētniecībai')[0]]='I am a humanities researcher interested in digital humanities, digital cultural heritage, citizen science and participatory research methods. I also study folklore, life-writing traditions and oral history.'
TRANSLATIONS['Strādāju LU Humanitāro zinātņu fakultātē kā asociētā tenūrprofesore un Digitālo humanitāro zinātņu centra vadītāja.']='I am a tenured associate professor at the Faculty of Humanities, University of Latvia, and head of the Digital Humanities Centre.'
block('books',1,'Research is at the centre of my professional life as a humanities scholar, but in my spare time I enjoy writing for children. Two of my children’s books have been published. In 2025, “Draugi un kaimiņi” received the Latvian Literature Award and the LSM.lv readers’ choice award, as well as a nomination for the International Jānis Baltvilks Prize in Children’s Literature and Book Art.')
block('books',2,'Alongside my creative writing, I visit libraries and schools to meet young readers. Our conversations go beyond my books and explore a wide range of questions, mostly connected with life writing. Why do we keep diaries, and what makes them valuable? When can we write our life stories and memories? What did people write in their diaries 100, 50 or 30 years ago? What is a family’s documentary heritage, and why should we preserve it? Conversations with young people bring my creative and research work together.')
block('books',12,'“Draugi un kaimiņi” is a mischievous coming-of-age story set in a small Latvian town in the early 1990s. Two best friends, girls aged ten or eleven, love spending their free time in a corner of a meadow beneath a great willow tree, a place they call the Jungle. It is both an exciting playground and a refuge when life at home becomes unbearable. The town authorities plan to build a factory on the site. The Jungle must be saved! Their rescue mission does not go quite as planned, but along the way the friends get to know their colourful neighbours and learn much more about themselves.')
block('books',13,'Aleksandra Runde’s illustrations, with their playful lines, two-colour palette and expressive characters, vividly complement a story that captures the atmosphere of the early 1990s.')
block('books',14,'The book is available from Jānis Roze bookshops.')
block('books',24,'Folklore researcher Sanita Reinsone’s book grew out of conversations with her children during summers in northern Vidzeme and visits to Estonia. It is written as a storyteller’s account of legendary events: a tale that interprets reality through fairy-tale techniques, freely combining knowledge and imagination. In this story, Estonia and Latvia, where much of the action takes place, are lands where the worlds of people and dolls exist side by side. By presenting Estonia as a “land of dolls”, the author introduces children to the regions, language and traditions of Latvia’s real neighbouring country.')
for i,en in {7:'Latvian Literature Award 2025: best original children’s book in Latvian',8:'LSM.lv readers’ choice award 2025',9:'Nomination for the International Jānis Baltvilks Prize in Children’s Literature and Book Art 2025',10:'Selected for the Children’s, Young Adults’ and Parents’ Jury collection 2025 (age 9+) '}.items():TRANSLATIONS[S['books']['blocks'][i]['text'].replace('✨','').strip()]=en.strip()
block('activities',3,'The world changed on 24 February 2022. Two days after Russia launched its full-scale invasion of Ukraine, I opened a Twitter account to collect information about international support available to Ukrainian scholars and students. Together with colleagues, I developed this initiative into #ScienceForUkraine. Within a week, the initiative had become an international volunteer organisation involving more than 100 people from 30 countries. #ScienceForUkraine represents collective strength, empathy and the wish to help. Since 2 August 2023, #ScienceForUkraine has been a registered NGO in Latvia. I am part of its leadership team.')
# Original paragraph has non-breaking spaces in the published source.
block('activities',7,'Citizen science is a field in which I have been actively involved since 2014, when the digital archive garamantas.lv was established and we began developing public engagement initiatives. In autumn 2023, I was nominated as Latvia’s citizen science ambassador by the European Citizen Science Association. Together with other researchers, I have been developing the Facebook page “Citizen Science in Latvia” and working to make citizen science better known and more widely used in research.')
TRANSLATIONS['Vairāk par #ScienceForUkraine var uzzināt mūsu']='Find out more about #ScienceForUkraine on our'
TRANSLATIONS['mājas lapā']='website'
TRANSLATIONS['un citos sociālajos tīklos.']='and other social media.'
TRANSLATIONS['Laipni aicināti arī izlasīt #ScienceForUkraine pirmo trīs mēnešu darbības ziņojumu']='You can also read the report on the first three months of #ScienceForUkraine'
TRANSLATIONS['šeit']='here'
TRANSLATIONS['No 2020. līdz 2022. gadam man bija gods darboties kā zinātnes komunikācijas koordinatorei COST akcijā Nep4Dissent (CA16213). Šajā laikā ieguvu vērtīgu praktisko pieredzi zinātnes kounikācijas jomā, sekojot līdzi un ziņojot par dinamisku pētniecības tīklu, izveidojot "']='From 2020 to 2022, I served as science communication coordinator for the COST Action Nep4Dissent (CA16213). I gained valuable practical experience by following and reporting on a dynamic research network, creating “'
TRANSLATIONS['," kā arī veicot padziļinātas intervijas ar izciliem zinātniekiem un citas aktivitātes.']='”, conducting in-depth interviews with outstanding scholars and undertaking other activities.'

block('publications',84,'Reinsone, Sanita. Meža meitas. 12 women on life at home, in the forest and in prison. Riga: Dienas Grāmata, 2015 (second edition, 2022). “Meža meitas” was staged at Valmiera Drama Theatre, directed by Mārtiņš Eihe (premiere: January 2018).')
block('publications',86,'Reinsone, Sanita. Ādama stāsts. Life, customs and habits in Mazsalaca in Ā. Purmalis’s autobiography at the turn of the 20th century. Riga: Zinātne, 2008 (second edition, 2011). “Ādama stāsts” was staged at the Latvian National Theatre, directed by Indra Roga (premiere: 2011).')

TRANSLATIONS['Vidzemes folkloras materiālu digitalizācija']='Digitisation of folklore materials from Vidzeme'
from english_extra import PAIRS as EXTRA_PAIRS
TRANSLATIONS.update(dict(line.split('\t',1) for line in EXTRA_PAIRS.strip().splitlines() if '\t' in line))
# Normalised whitespace makes preserved source markup and text share one translation.
def norm(s):return re.sub(r'\s+',' ',s).strip()
TRANSLATIONS={norm(k):v for k,v in TRANSLATIONS.items()}
PHRASES=sorted(TRANSLATIONS,key=len,reverse=True)
def translate(s):
 key=norm(s)
 if key in TRANSLATIONS:return TRANSLATIONS[key]
 # Replace known phrases in mixed metadata while preserving names and source titles.
 pattern='|'.join(re.escape(k) for k in PHRASES)
 return re.sub(r'(?<!\w)(?:'+pattern+r')(?!\w)',lambda m:TRANSLATIONS[m[0]],s)
