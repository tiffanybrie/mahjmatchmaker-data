// Oct 19 color fix: rainbow order + separate Orange and Yellow. String transforms on a code block's editor source.
// Idempotent: re-running on already-transformed source changes nothing.
(function(root){
const ORDER=['red','orange','yellow','green','blue','purple','pink','brown','ivory','holiday','neutral','masculine'];
const COL={orange:{label:'Orange',c:'#e07a2c',sw:['#b8501a','#fde0c8','#f5a868','#e07a2c']},
           yellow:{label:'Yellow',c:'#e2b93b',sw:['#b08812','#fff4c4','#f7dc6f','#e2b93b']}};
const ORANGE=['papaya-spritz','solara','sunset','sierra'];   // Tiffany's filing, Oct 19
const YELLOW=['pippa','sorbet','sunday-tile-set'];
const TO_BROWN=['tortoise'];                                  // Classic Tortoise
function keyOf(href){ if(/\/holiday-mahjong-matches$/.test(href)) return 'holiday';
  const m=href.match(/^\/([a-z-]+)-mahjong-tile-matches$/); return m? m[1]:null; }
function rank(k){ const i=ORDER.indexOf(k); return i<0? 999:i; }
const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');

// Reorder a run of sibling <a ...> chips inside a container; split yellow-orange into two chips.
function reorderChips(s, containerOpen, chipTag){
  let pos=0, n=0;
  while(true){
    const a=s.indexOf(containerOpen,pos); if(a<0) break;
    const start=a+containerOpen.length;
    // the chips run until the container's first '</div>' that isn't inside a chip (chips have inner spans only, no divs)
    const end=s.indexOf('</div>',start);
    const inner=s.slice(start,end);
    const chips=inner.match(new RegExp('<a [^>]*?'+chipTag+'[\\s\\S]*?<\\/a>','g'))||[];
    if(!chips.length){ pos=end; continue; }
    let out=[];
    for(const c of chips){
      const href=(c.match(/href="([^"]+)"/)||[])[1]||'';
      if(keyOf(href)==='yellow-orange'){
        for(const k of ['orange','yellow']){
          const v=COL[k];
          let x=c.replace(/href="[^"]+"/,`href="/${k}-mahjong-tile-matches"`)
                 .replace(/Yellow &amp; Orange|Yellow & Orange/,v.label)
                 .replace(/border:2px solid #[0-9a-f]{6}/i,`border:2px solid ${v.c}`)
                 .replace(/--c:#[0-9a-f]{6}/i,`--c:${v.c}`)
                 .replace(/conic-gradient\(from -45deg,#[0-9a-f]{6} 0 0\.4%,#[0-9a-f]{6} 0\.9% 24\.6%,#[0-9a-f]{6} 25\.1% 49\.6%,#[0-9a-f]{6} 50\.1% 74\.6%,#[0-9a-f]{6} 75\.1% 100%\)/i,
                   `conic-gradient(from -45deg,${v.sw[0]} 0 0.4%,${v.sw[1]} 0.9% 24.6%,${v.sw[2]} 25.1% 49.6%,${v.sw[3]} 50.1% 74.6%,${v.sw[0]} 75.1% 100%)`);
          out.push(x);
        }
      } else out.push(c);
    }
    // de-dup (idempotent) then stable sort: known colors by ORDER, others keep relative order after
    const seen=new Set(); out=out.filter(c=>{const h=(c.match(/href="([^"]+)"/)||[])[1]; if(seen.has(h)) return false; seen.add(h); return true;});
    const idx=out.map((c,i)=>({c,i,k:keyOf((c.match(/href="([^"]+)"/)||[])[1]||'')}));
    idx.sort((x,y)=>(rank(x.k)-rank(y.k))||(x.i-y.i));
    const rebuilt=idx.map(o=>o.c).join('');
    // preserve any non-chip text between/after chips (none expected) by replacing only the chips span
    const first=inner.indexOf(chips[0]); const lastC=chips[chips.length-1]; const last=inner.lastIndexOf(lastC)+lastC.length;
    const newInner=inner.slice(0,first)+rebuilt+inner.slice(last);
    s=s.slice(0,start)+newInner+s.slice(end); pos=start+newInner.length; n++;
  }
  return [s,n];
}

// Grouped "All Albums by Color": split yellow-orange, move Tortoise to Brown, rainbow order.
function regroup(s){
  const H=/<h3 class="mmalb-ch" id="color-([a-z-]+)">[\s\S]*?<\/h3>\s*(?:<div class="mmalb-g">[\s\S]*?<\/div>|<p class="mmalb-sub">[\s\S]*?<\/p>)/g;
  const units=[]; let m; while((m=H.exec(s))) units.push({k:m[1],html:m[0],a:m.index,b:m.index+m[0].length});
  if(!units.length) return [s,0];
  const card=(html,slug)=>{const r=new RegExp('<a class="mmalb-c" href="/'+esc(slug)+'-mahjong-tile-matches">[\\s\\S]*?<\\/a>'); const x=html.match(r); return x?x[0]:null;};
  const grid=u=>u.html.slice(u.html.indexOf('<div class="mmalb-g">')+21, u.html.lastIndexOf('</div>'));
  const mk=(k,label,cards)=>`<h3 class="mmalb-ch" id="color-${k}"><a href="/${k}-mahjong-tile-matches">${label}</a></h3><div class="mmalb-g">${cards.join('')}</div>`;
  let byK={}; units.forEach(u=>byK[u.k]=u);
  const yo=byK['yellow-orange'];
  if(yo){
    const g=grid(yo);
    const o=ORANGE.map(x=>card(g,x)).filter(Boolean), y=YELLOW.map(x=>card(g,x)).filter(Boolean);
    const moved=TO_BROWN.map(x=>card(g,x)).filter(Boolean);
    const placed=new Set([...ORANGE,...YELLOW,...TO_BROWN]);
    const rest=(g.match(/<a class="mmalb-c"[\s\S]*?<\/a>/g)||[]).filter(c=>!placed.has((c.match(/href="\/([a-z0-9-]+)-mahjong-tile-matches"/)||[])[1]));
    rest.forEach(c=>y.push(c)); // anything unplanned lands in Yellow and is reported by the README check
    byK['orange']={k:'orange',html:mk('orange','Orange',o)};
    byK['yellow']={k:'yellow',html:mk('yellow','Yellow',y)};
    delete byK['yellow-orange'];
    if(byK['brown'] && moved.length){ const b=byK['brown']; const gb=grid(b);
      const add=moved.filter(c=>!gb.includes(c.match(/href="[^"]+"/)[0]));
      b.html=b.html.slice(0,b.html.lastIndexOf('</div>'))+add.join('')+'</div>'; }
  }
  const ordered=Object.values(byK).sort((x,y)=>rank(x.k)-rank(y.k)).map(u=>u.html).join('\n');
  const a=units[0].a, b=units[units.length-1].b;
  return [s.slice(0,a)+ordered+s.slice(b), 1];
}

function home(s){ let n=0,r; [s,r]=reorderChips(s,'<div class="mmh-cols mmh-c5">','class="mmh-col"'); n+=r;
  // 12 chips now: 6 per row on desktop
  s=s.replace('.mmh-cols.mmh-c5{grid-template-columns:repeat(5,minmax(0,1fr))}','.mmh-cols.mmh-c5{grid-template-columns:repeat(6,minmax(0,1fr))}');
  [s,r]=regroup(s); n+=r; return [s,n]; }
function mtm(s){ let n=0,r; [s,r]=reorderChips(s,'<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px">','href="/'); n+=r; [s,r]=regroup(s); n+=r; return [s,n]; }
function colorPage(s){ return reorderChips(s,'<div class="mmcol-chips">','href="/'); }
root.MMCOLOR2={home,mtm,colorPage,regroup,reorderChips,ORDER};
})(typeof window!=='undefined'?window:globalThis);
