from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':780,'height':1688})
    c.add_init_script("document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.zoom='2'})")
    pg=c.new_page(); pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    print(pg.evaluate("()=>[innerWidth,document.documentElement.clientWidth,matchMedia('(max-width:500px)').matches]"))
    pg.screenshot(path='z.png'); b.close()
