from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    print(pg.evaluate("()=>[typeof S,typeof drawCard,typeof matDeck,typeof codeLine,typeof D,typeof M,typeof R,typeof T, D.sets.length]"))
    print(pg.evaluate("()=>{const bs={};D.sets.forEach(s=>bs[s.maker]=(bs[s.maker]||0)+1);const mb={};Object.values(M).forEach(m=>{if(!m.hid)mb[m.bn]=(mb[m.bn]||0)+1});const rb={};Object.values(R).forEach(r=>rb[r.bn]=(rb[r.bn]||0)+1);return {bs,mb,rb}}"))
    b.close()
