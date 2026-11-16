(()=>{
'use strict';
const root=document.getElementById('sr-research-world');
if(!root)return;
const nodes=/*RESEARCH_DATA*/;
const topics=["infrastructure", "memory", "folklore", "language", "participation"];
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const wireProgress=new Map();
let scrollWires=[],wireFrame=0;
const expandedGroups=new Set();
let selected=null;const opened=new Set();let instance=0;
 cancelAnimationFrame(wireFrame);wireFrame=0;scrollWires=[];
const area=root.querySelector('.world-content');
function pastMarker(n){
 return n.past_label?'<span class="past-marker" role="img" aria-label="'+esc(n.past_label)+'" title="'+esc(n.past_label)+'"></span>':'';
}
function projectFacts(p){
 return '<dl class="project-facts">'+p.facts.map(([label,value])=>'<div><dt>'+esc(label)+'</dt><dd>'+esc(value)+'</dd></div>').join('')+'</dl>'+(p.summary?'<p class="graph-meta">'+esc(p.summary)+'</p>':'');
}
function featureCard(f){
 if(!f)return '';
 return '<aside class="media-feature"><figure><img src="'+esc(f.image)+'" alt="Sanita Reinsone" loading="lazy"><figcaption>'+esc(f.credit)+'</figcaption></figure><div><p class="media-feature-label">'+esc(f.label)+'</p><h4><a href="'+esc(f.url)+'" target="_blank" rel="noopener noreferrer">'+esc(f.title)+'</a></h4><p class="graph-meta">'+esc(f.meta)+'</p></div></aside>';
}
function canExpand(n){
 return !n.project&&!n.direct_link&&Boolean(n.description||n.feature||n.corpus_url||(n.groups||[]).some(([,ids])=>ids.length));
}
function detail(id,index=0){
 const n=nodes[id],uid='graph-detail-'+id;if(!canExpand(n))return '';
 return '<section class="graph-detail" id="'+uid+'" style="--wide-order:'+ (Math.floor(index/2)*2+1)+';--narrow-order:'+(index*2+1)+'" aria-label="'+esc(n.title)+'"><div class="graph-detail-top"><h3 class="graph-detail-heading"><span class="graph-detail-label">'+esc(n.title)+'</span></h3><button type="button" data-close-detail="true" aria-label="Aizvērt detaļas"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="m6 6 12 12M6 18 18 6"/></svg></button></div>'+(n.project?projectFacts(n.project):n.bibliography?'<p class="graph-meta bibliography-reference">'+n.bibliography.reference_html+'</p>':n.meta?'<p class="graph-meta">'+esc(n.meta)+'</p>':'')+(n.url?'<a class="graph-source'+(n.external_icon?' graph-source--external':'')+'" href="'+esc(n.url)+'"'+(/^https?:/.test(n.url)?' target="_blank" rel="noopener noreferrer"':'')+'>'+esc(n.source||'Atvērt avotu')+(n.external_icon?'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>':'')+'</a>':'')+featureCard(n.feature)+(n.description?'<p class="graph-meta">'+esc(n.description)+'</p>':'')+(n.corpus_url?'<p><a class="graph-source" href="'+esc(n.corpus_url)+'" target="_blank" rel="noopener noreferrer">Analizēt korpusu</a></p>':'')+(n.groups||[]).map(([label,ids])=>'<div class="graph-connections"><h4>'+esc(label)+'</h4><div>'+ids.filter(x=>x!==id).map(x=>(!canExpand(nodes[x]))?(nodes[x].url?'<a href="'+esc(nodes[x].url)+'" target="_blank" rel="noopener noreferrer">'+esc(nodes[x].title)+'</a>':'<span>'+esc(nodes[x].title)+'</span>'):'<button type="button" data-go="'+x+'">'+esc(nodes[x].title)+'</button>').join('')+'</div></div>').join('')+((n.related||[]).filter(x=>topics.includes(x)&&x!==selected).length?'<div class="graph-related"><span>Saistītās tēmas</span>'+(n.related||[]).filter(x=>topics.includes(x)&&x!==selected).map(x=>'<button type="button" data-topic="'+x+'">'+esc(nodes[x].title)+'</button>').join('')+'</div>':'')+'</section>';
}
function unit(id,index,categoryLabel){
 const isDatasetCategory=categoryLabel==='Datu kopas';
 const n=nodes[id],expanded=opened.has(id),bib=n.bibliography;
 if(n.project){
  const p=n.project,role=p.role||p.institution_role||'';
  const body='<span class="graph-unit-type">Projekts'+pastMarker(n)+'</span><span class="graph-unit-title">'+esc(n.title)+'</span>'+(p.full_name&&p.full_name.trim().toLowerCase()!==p.short_name.trim().toLowerCase()?'<span class="graph-unit-project-name">'+esc(p.full_name)+'</span>':'')+(p.period?'<span class="graph-unit-meta">'+esc(p.period)+'</span>':'')+(role?'<span class="graph-unit-role">'+esc(role)+'</span>':'')+(p.funding?'<span class="graph-unit-funding">'+esc(p.funding)+'</span>':'')+(p.identifier?'<span class="graph-unit-funding">Nr. '+esc(p.identifier)+'</span>':'');
  const attrs=' class="graph-unit-button graph-project-link" data-unit="'+id+'" title="'+esc(p.full_name)+'"';
  const link=p.url?'<a'+attrs+' href="'+esc(p.url)+'" target="_blank" rel="noopener noreferrer">'+body+'</a>':'<div'+attrs+'>'+body+'</div>';
  return '<article class="graph-unit graph-unit--project" style="--wide-order:'+(Math.floor(index/2)*2)+';--narrow-order:'+(index*2)+'">'+link+'</article>';
 }

 const content=(isDatasetCategory?'':'<span class="graph-unit-type">'+esc(n.type)+pastMarker(n)+'</span>')+'<span class="graph-unit-title">'+esc(n.title)+(bib?.descriptor&&!isDatasetCategory?' ['+esc(bib.descriptor)+'].':bib&&!/[.!?]$/.test(n.title)?'.':'')+'</span>'+(bib?'<span class="graph-unit-authors">'+esc(bib.preview_authors_year||bib.authors_year)+'</span>':'')+'<span class="graph-unit-meta">'+(bib?bib.tail_html+(bib.doi?' <span class="graph-doi">https://doi.org/'+esc(bib.doi)+'</span>':''):esc(n.meta||''))+'</span>';
 if(!canExpand(n)&&n.url)return '<article class="graph-unit" style="--wide-order:'+(Math.floor(index/2)*2)+';--narrow-order:'+(index*2)+'"><a class="graph-unit-button graph-project-link" data-unit="'+id+'" href="'+esc(n.url)+'" target="_blank" rel="noopener noreferrer">'+content+'</a></article>';
 if(!canExpand(n))return '<article class="graph-unit graph-unit--static" style="--wide-order:'+(Math.floor(index/2)*2)+';--narrow-order:'+(index*2)+'"><div class="graph-unit-button" data-unit="'+id+'">'+content+'</div></article>';
 return '<article class="graph-unit'+(bib?' graph-unit--publication':n.project?' graph-unit--project':'')+'" style="--wide-order:'+(Math.floor(index/2)*2)+';--narrow-order:'+(index*2)+'"><button class="graph-unit-button" type="button" data-unit="'+id+'" aria-expanded="'+expanded+'"'+(expanded?' aria-controls="graph-detail-'+id+'"':'')+'>'+content+'</button></article>'+(expanded?detail(id,index):'');
}
function category(label,ids,index){
 const key=selected+':'+index;
 if(ids.slice(4).some(id=>opened.has(id)))expandedGroups.add(key);
 const expanded=expandedGroups.has(key),items=expanded?ids:ids.slice(0,4),listId='graph-list-'+index;
 return '<section class="graph-category"><h2 class="graph-category-title"><span class="graph-heading-label">'+esc(label)+'</span></h2><div class="graph-unit-list" id="'+listId+'">'+items.map((id,index)=>unit(id,index,label)).join('')+'</div>'+(ids.length>4?'<button class="graph-show-more" type="button" data-more="'+key+'" aria-expanded="'+expanded+'" aria-controls="'+listId+'">'+(expanded?'Rādīt mazāk':'Rādīt pārējos ('+(ids.length-4)+')')+'</button>':'')+'</section>';
}
function panel(){
 if(!selected)return '';
 const n=nodes[selected],visible=new Set((n.groups||[]).flatMap(([,ids])=>ids)),outside=Array.from(opened).find(id=>!visible.has(id));
 return '<section class="graph-panel" id="research-branch" aria-label="'+esc(n.title)+': saistītie materiāli">'+(outside?'<div class="graph-linked-detail">'+detail(outside)+'</div>':'')+'<div class="graph-categories">'+(n.groups||[]).map(([label,ids],index)=>category(label,ids,index)).join('')+'</div><div class="graph-panel-end"><button type="button" class="graph-close" data-close="true" aria-label="Sakļaut tēmu" title="Sakļaut tēmu"><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m18 15-6-6-6 6"/></svg></button></div></section>';
}
function render(focusKey){
 instance=0;
 cancelAnimationFrame(wireFrame);wireFrame=0;scrollWires=[];
 area.innerHTML='<h1>Pētniecība</h1><div class="research-network"><svg class="research-wires" aria-hidden="true" focusable="false"></svg><div class="research-roots">'+topics.map(id=>'<button class="graph-topic'+(id===selected?' is-open':'')+'" type="button" data-topic="'+id+'" aria-expanded="'+(id===selected)+'" aria-controls="research-branch"><span class="graph-topic-title">'+esc(nodes[id].title)+'</span></button>'+(id===selected?panel():'')).join('')+'</div></div><p class="graph-status" aria-live="polite">'+(selected?esc(nodes[selected].title)+' – saistītie materiāli atvērti.':'')+'</p>';
 requestAnimationFrame(drawWires);
 if(focusKey){const target=root.querySelector(focusKey);if(target)target.focus({preventScroll:true});}
}
function drawWires(){
 const network=root.querySelector('.research-network'),svg=root.querySelector('.research-wires'),panel=root.querySelector('.graph-panel');
 if(!network||!svg)return;
 if(!selected||!panel){svg.replaceChildren();svg.setAttribute('height','0');return;}
 const bounds=network.getBoundingClientRect(),box=el=>{const b=el.getBoundingClientRect();return {x:b.left-bounds.left,y:b.top-bounds.top,w:b.width,h:b.height};};
 const width=network.clientWidth,height=network.clientHeight;
 svg.setAttribute('viewBox',`0 0 ${width} ${height}`);svg.setAttribute('width',width);svg.setAttribute('height',height);
 function nodeKey(el){
 let key;
 if(el.classList.contains('graph-topic'))key='topic:'+el.dataset.topic;
 else if(el.classList.contains('graph-unit-title'))key=selected+':unit:'+el.closest('[data-unit]').dataset.unit;
 else if(el.classList.contains('graph-detail-label'))key=selected+':detail:'+el.closest('.graph-detail').id;
 else if(el.classList.contains('graph-heading-label'))key=selected+':heading:'+el.textContent;
 else key=selected+':'+el.textContent;
 el.dataset.wireNode=key;return key;
 }
 function textPoint(el){const b=box(el),line=parseFloat(getComputedStyle(el).lineHeight)||b.h;return {x:b.x,y:b.y+Math.min(b.h,line)/2};}
 const edges=[],point=(x,y)=>`${Math.round(x*10)/10} ${Math.round(y*10)/10}`;
 function edge(source,target,d,reveal=target){
 const parts=d.match(/[MHV]|-?\d+(?:\.\d+)?/g);let x=0,y=0;
 for(let i=0;i<parts.length;){const command=parts[i++];if(command==='M'){x=+parts[i++];y=+parts[i++];}else if(command==='H')x=+parts[i++];else if(command==='V')y=+parts[i++];}
 edges.push({source,target,d,reveal,x,y,key:nodeKey(source)+'>'+nodeKey(target)});
}
 const chosen=root.querySelector('.graph-topic.is-open'),source=box(chosen),p=box(panel);
 for(const category of panel.querySelectorAll(':scope > .graph-categories > .graph-category')){
  const heading=category.querySelector(':scope > .graph-category-title .graph-heading-label'),h=box(heading),sx=source.x+source.w/2,tx=h.x,bus=h.y-16,tip=textPoint(heading);
  edge(chosen,heading,`M ${point(sx,source.y+source.h)} V ${p.y+12} H 12 V ${bus} H ${tx-10} V ${tip.y} H ${tx}`);
 }
 // Each branch is a complete source-to-target path, including the final item.
 for(const list of panel.querySelectorAll('.graph-unit-list')){
  const owner=list.parentElement,heading=owner.querySelector(':scope > .graph-category-title .graph-heading-label, :scope > h4 .graph-heading-label');if(!heading)continue;
  const h=box(heading),l=box(list),spine=l.x+1;
  for(const article of list.querySelectorAll(':scope > .graph-unit')){
   const button=article.querySelector(':scope > .graph-unit-button'),title=button.querySelector('.graph-unit-title'),t=box(title),a=box(article),y=textPoint(title).y;
   edge(heading,title,`M ${point(h.x+Math.min(14,h.w/2),h.y+h.h)} V ${l.y-14} H ${spine} V ${a.y-10} H ${a.x-8} V ${y} H ${t.x}`,article);
  }
 }
 for(const expanded of panel.querySelectorAll('.graph-detail')){
  const id=expanded.id.replace('graph-detail-',''),button=panel.querySelector('[data-unit="'+id+'"]'),sourceNode=button?button.querySelector('.graph-unit-title'):chosen;
  const sourceBox=box(sourceNode),heading=expanded.querySelector('.graph-detail-label'),tip=textPoint(heading),d=box(expanded);
  if(button){
   const start=textPoint(sourceNode),card=box(button.closest('.graph-unit'));
   edge(sourceNode,heading,`M ${point(start.x,start.y)} H ${card.x-8} V ${d.y-12} H ${d.x+4} V ${tip.y} H ${tip.x}`,expanded);
  }else edge(sourceNode,heading,`M ${point(sourceBox.x+sourceBox.w/2,sourceBox.y+sourceBox.h)} V ${d.y-12} H ${d.x+4} V ${tip.y} H ${tip.x}`,expanded);
 }
 const ns='http://www.w3.org/2000/svg',make=(tag,attrs)=>{const el=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))el.setAttribute(k,v);return el;};
 let defs=svg.querySelector('defs');if(!defs){defs=make('defs',{});svg.prepend(defs);}
 const existing=new Map(Array.from(svg.querySelectorAll(':scope > g')).map(g=>[g.dataset.edge,g]));
 const previous=new Map(scrollWires.map(w=>[w.key,w]));
 scrollWires=[];
 for(const e of edges){
  let group=existing.get(e.key);existing.delete(e.key);
  if(!group){
   const id='wire-mask-'+(++instance),mask=make('mask',{id,maskUnits:'userSpaceOnUse',x:0,y:0,width,height});
   mask.append(make('path',{d:e.d,fill:'none',stroke:'white','stroke-width':5,pathLength:1,'stroke-dasharray':1,'stroke-dashoffset':1}));defs.append(mask);
   group=make('g',{'data-edge':e.key,'data-mask':id});
   group.append(make('path',{d:e.d,fill:'none',mask:`url(#${id})`,'data-source':nodeKey(e.source),'data-target':nodeKey(e.target)}));
   group.append(make('circle',{cx:e.x,cy:e.y,r:e.target.matches('.graph-heading-label,.graph-detail-label')?4.5:2.5,opacity:0}));svg.append(group);
  }
  const path=group.querySelector('path'),dot=group.querySelector('circle'),mask=defs.querySelector('#'+group.dataset.mask),ink=mask.querySelector('path');
  path.setAttribute('d',e.d);ink.setAttribute('d',e.d);dot.setAttribute('cx',e.x);dot.setAttribute('cy',e.y);mask.setAttribute('width',width);mask.setAttribute('height',height);
  // Cache orthogonal path segments; scrolling then requires no SVG geometry reads.
  const tokens=e.d.match(/[MHV]|-?\d+(?:\.\d+)?/g),segments=[];let x=0,y=0,length=0,startY=0;
  for(let i=0;i<tokens.length;){
   const command=tokens[i++];
   if(command==='M'){x=+tokens[i++];y=+tokens[i++];startY=y;continue;}
   const nx=command==='H'?+tokens[i++]:x,ny=command==='V'?+tokens[i++]:y,size=Math.abs(nx-x)+Math.abs(ny-y);
   if(size)segments.push({y,ny,size});length+=size;x=nx;y=ny;
  }
  scrollWires.push({key:e.key,ink,dot,segments,length,startY,endY:e.y,dotVisible:previous.get(e.key)?.dotVisible||false,network,current:previous.get(e.key)?.current??wireProgress.get(e.key)??0});
 }
 for(const group of existing.values()){defs.querySelector('#'+group.dataset.mask)?.remove();group.remove();}
 scheduleWires();
}
function scheduleWires(){if(!wireFrame)wireFrame=requestAnimationFrame(updateScrollWires);}
function updateScrollWires(){
 wireFrame=0;if(!scrollWires.length)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const networkTop=scrollWires[0].network.getBoundingClientRect().top;
 const frontier=window.innerHeight*.76-networkTop;
 const mobile=matchMedia('(max-width: 750px)').matches;
 const dotFrontier=window.innerHeight-24-networkTop;
 let moving=false;
 for(const w of scrollWires){
  let visible=0;
  if(frontier>=w.startY){
   for(const segment of w.segments){
    if(segment.y===segment.ny){if(frontier>=segment.y)visible+=segment.size;else break;}
    else if(frontier>=Math.max(segment.y,segment.ny))visible+=segment.size;
    else{visible+=segment.size*Math.max(0,Math.min(1,(frontier-segment.y)/(segment.ny-segment.y)));break;}
   }
  }
  // Keep completed connections when the reader scrolls back up or expands an item.
  const goal=reduced?1:Math.max(wireProgress.get(w.key)||0,w.length?visible/w.length:1);
  wireProgress.set(w.key,goal);
  w.current=reduced?1:w.current+(goal-w.current)*.12;
  if(Math.abs(goal-w.current)<.0005)w.current=goal;else moving=true;
  w.ink.setAttribute('stroke-dashoffset',1-w.current);
  // On small screens, show the endpoint as soon as its text enters view.
  // The slower line animation continues independently.
  if(mobile&&dotFrontier>=w.endY)w.dotVisible=true;
  w.dot.setAttribute('opacity',(reduced||(mobile?w.dotVisible:w.current>=.999))?1:0);
 }
 if(moving)scheduleWires();
}
window.addEventListener('scroll',scheduleWires,{passive:true});

function closeTopic(){
 // Theme links originate on the homepage; collapsing returns to its full view.
 window.location.assign('index.html');
}
function setTopic(id){
 if(selected===id){closeTopic();return;}
 wireProgress.clear();selected=id;opened.clear();history.replaceState(null,'','#'+selected);render('[data-topic="'+selected+'"]');
}
root.addEventListener('click',event=>{
 const button=event.target.closest('button');if(!button||!root.contains(button))return;
 if(button.dataset.more){const key=button.dataset.more;if(expandedGroups.has(key)){expandedGroups.delete(key);opened.clear();}else expandedGroups.add(key);render('[data-more="'+key+'"]');return;}
 if(button.dataset.topic){setTopic(button.dataset.topic);return;}
 if(button.dataset.close){closeTopic();return;}
 if(button.dataset.closeDetail){const id=Array.from(opened)[0];opened.clear();render(id?'[data-unit="'+id+'"]':undefined);return;}
 if(button.dataset.go){const id=button.dataset.go;opened.clear();opened.add(id);const host=nodes[id].primary_topic||topics.find(t=>(nodes[t].groups||[]).some(([,ids])=>ids.includes(id)));if(host&&host!==selected){selected=host;wireProgress.clear();}history.replaceState(null,'','#'+id);render();requestAnimationFrame(()=>root.querySelector('#graph-detail-'+id)?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'nearest'}));return;}
 if(button.dataset.unit){const id=button.dataset.unit,wasOpen=opened.has(id);opened.clear();if(!wasOpen)opened.add(id);history.replaceState(null,'',opened.size?'#'+id:'#'+selected);render('[data-unit="'+id+'"]');}
});
function findPath(start,target,seen=new Set()){
 if(start===target)return [start];if(seen.has(start))return null;seen.add(start);
 for(const [,ids] of nodes[start]?.groups||[]){for(const child of ids){const path=findPath(child,target,seen);if(path)return [start,...path];}}
 return null;
}
function fromHash(){
 wireProgress.clear();
 const requested=location.hash.slice(1),id=requested==='dh-infrastructure'?'infrastructure':requested==='diaries'?'autobiography':requested;selected=topics.includes(id)?id:null;opened.clear();
 if(!selected&&nodes[id]){
  // Prefer a direct match, then follow nested branches while avoiding graph cycles.
  const contextualTopic=new URLSearchParams(location.search).get('tema');
  selected=(topics.includes(contextualTopic)&&(nodes[contextualTopic].groups||[]).some(([,ids])=>ids.includes(id))?contextualTopic:null)||nodes[id].primary_topic||topics.find(t=>(nodes[t].groups||[]).some(([,ids])=>ids.includes(id)))||null;
  if(selected)opened.add(id);
  else for(const topic of topics){const path=findPath(topic,id);if(path){selected=topic;opened.add(id);break;}}
 }
 render();
}
window.addEventListener('hashchange',fromHash);window.addEventListener('resize',()=>requestAnimationFrame(drawWires));
if(typeof ResizeObserver!=='undefined')new ResizeObserver(()=>requestAnimationFrame(drawWires)).observe(area);
fromHash();
})();
