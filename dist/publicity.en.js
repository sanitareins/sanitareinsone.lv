(()=>{
 const buttons=[...document.querySelectorAll('[data-publicity-filter]')];
 const groups=[...document.querySelectorAll('[data-media-group]')];
 if(!groups.length)return;
 const expanded=new Set();let filter='all';
 function update(){
  groups.forEach(group=>{
   const key=group.dataset.mediaGroup,rows=[...group.querySelectorAll('[data-publicity]')];
   const matches=rows.filter(row=>filter==='all'||row.dataset.publicity.split(' ').includes(filter));
   rows.forEach(row=>{row.hidden=!matches.includes(row)||(!expanded.has(key)&&matches.indexOf(row)>=4);});
   group.hidden=matches.length===0;
   group.querySelector('.media-group-count').textContent=String(matches.length);
   const more=group.querySelector('[data-show-more]');more.hidden=matches.length<=4;
   more.setAttribute('aria-expanded',String(expanded.has(key)));
   more.textContent=expanded.has(key)?'Show less':`Show more (${Math.max(0,matches.length-4)})`;
  });
  document.querySelectorAll('[data-publicity-feature]').forEach(el=>{el.hidden=filter!=='all'&&!el.dataset.publicityFeature.split(' ').includes(filter);});
 }
 buttons.forEach(button=>button.addEventListener('click',()=>{
  filter=button.dataset.publicityFilter;expanded.clear();
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  update();
 }));
 groups.forEach(group=>group.querySelector('[data-show-more]').addEventListener('click',()=>{
  const key=group.dataset.mediaGroup;
  if(expanded.has(key))expanded.delete(key);else expanded.add(key);
  update();
 }));
 update();
})();
