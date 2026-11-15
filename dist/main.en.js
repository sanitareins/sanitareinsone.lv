const toggle=document.querySelector('.menu');const nav=document.getElementById('nav');
if(toggle&&nav){toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close menu':'Open menu');nav.classList.toggle('open',open);});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&toggle.getAttribute('aria-expanded')==='true'){toggle.click();toggle.focus();}});}

const backToTop = document.querySelector('.back-to-top');
if (backToTop) {
  const updateBackToTop = () => {
    backToTop.hidden = window.scrollY < Math.max(500, window.innerHeight * .8);
  };
  window.addEventListener('scroll', updateBackToTop, {passive: true});
  window.addEventListener('resize', updateBackToTop);
  backToTop.addEventListener('click', () => {
    const heading = document.querySelector('h1') || document.getElementById('saturs');
    if (heading) { heading.setAttribute('tabindex', '-1'); heading.focus({preventScroll: true}); }
    window.scrollTo({top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
  });
  updateBackToTop();
}

// Open a collapsed activity section when following its navigation link.
(()=>{const reveal=hash=>{const section=document.getElementById(hash.slice(1));if(section?.matches('details.activity-group'))section.open=true;};
reveal(location.hash);window.addEventListener('hashchange',()=>reveal(location.hash));
document.querySelectorAll('.section-nav a[href^="#"]').forEach(link=>link.addEventListener('click',()=>reveal(link.hash)));})();

// Preserve the selected research theme and anchor when switching languages.
document.querySelectorAll('[data-language-switch]').forEach(link=>{const update=()=>{const target=new URL(link.getAttribute('href'),location.href);target.search=location.search;target.hash=location.hash;link.href=target.pathname+target.search+target.hash;};update();window.addEventListener('hashchange',update);});
