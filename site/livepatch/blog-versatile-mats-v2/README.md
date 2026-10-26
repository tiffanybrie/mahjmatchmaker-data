# Most Versatile Mahjong Mats: rewrite (APPROVED by Tiffany, Oct 25 8:19pm)

Her review rounds are logged in docs/ANSWERS.md (Oct 25 7:38pm, 7:52pm, 8:19pm). The preview for her was https://claude.ai/artifact/QmhrQMo5M9Eofn6raA5Atf.

**What changes:** the body of `/blog/most-versatile-mahjong-mats`, which is ONE code block. Order is now:
1. leather
2. lots of colors
3. earthy neutrals and greens
4. dark, layered blues and greens
5. retired favorites (with photos)
6. tips

Other details:
- Real mat photos, hosted on jsDelivr at 816082e and warmed (15 URLs, all 200).
- Tracked shop links: the Find Your Mat-ch `u` links (discount/MAHJMATCH redirect plus ref).
- Brand names link to the brand guide pages. "See it with" sets link to their albums (every link returns 200).
- The end box is "Meet our partner brands". The old OMM-only button and the disclosure line are gone, because the site footer covers disclosure.

## OPS: paste steps (Chrome, one tab, close it after)
1. Pages > Blog > "The Most Versatile Mahjong Mats" > Edit.
2. Double-click the post's one code block.
3. Save the current content first, as rollback text, to `site/livepatch/blog-versatile-mats-v2/rollback-<date>.html`.
4. Replace all of it with `live-block.html`. Fetch it in the page:
   ```
   const html = await (await fetch('https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@555f0bd188b34b2440e9647ceb0fae13ca39ac49/site/livepatch/blog-versatile-mats-v2/live-block.html')).text();
   const v=document.querySelector('.cm-editor .cm-content').cmTile.view; v.dispatch({changes:{from:0,to:v.state.doc.length,insert:html}})
   ```
   Then Escape, Save, Exit. Keep the post's title, date, author and SEO fields as they are.
5. Verify the live page:
   - `curl -s "https://www.mahjmatchmaker.com/blog/most-versatile-mahjong-mats?v=$RANDOM"` contains `Leather and leatherette`, `Dark, layered blues and greens` and `Test it in`, and does NOT contain `My most versatile Oh My Mahjong mats`.
   - On a 390px phone, all 19 images load and there's no sideways scroll.
6. Search Console > URL Inspection > the post URL > Request indexing.
7. Log it in HQ (area "Blog"). Close the tab.
