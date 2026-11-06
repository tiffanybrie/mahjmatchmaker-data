// Hub /mahjong-discount-codes code block: drop Mahjong Row & Co. (ended Nov 5 2026). Run in the open CM6 code block.
window.MMHUBMRC = function () {
  const v = document.querySelector('.cm-editor .cm-content').cmTile.view;
  let s = v.state.doc.toString(); const rep = {};
  const sub = (k, re, to) => { const m = s.match(re); rep[k] = m ? m.length : 0; s = s.replace(re, to); };
  sub('ticker', /<a class="b27( dup)?" href="\/mahjong-row-and-co-discount-code"[^>]*><\/a>/g, '');
  sub('glance', /<li><a href="\/mahjong-row-and-co-discount-code"><strong>Mahjong Row &amp; Co\.<\/strong><\/a> &mdash; [^<]*<\/li>\s*/g, '');
  sub('allN', /All 39 mahjong discount codes at a glance/g, 'All 38 mahjong discount codes at a glance');
  sub('faqN', /at most of the 39 mahjong brands/g, 'at most of the 38 mahjong brands');
  sub('faqList', /Mahjong Row & Co\. \(10% off with MAHJMATCH\); /g, '');
  sub('date', /Updated November 4, 2026\./g, 'Updated November 5, 2026.');
  // ItemList: parse, drop, renumber
  const re = /<script type="application\/ld\+json">(\{[^<]*"@type": "ItemList"[^<]*)<\/script>/;
  const m = s.match(re); rep.itemlist = 0;
  if (m) {
    const j = JSON.parse(m[1]); const n0 = j.itemListElement.length;
    j.itemListElement = j.itemListElement.filter(x => !/mahjong-row-and-co/.test(x.url));
    j.itemListElement.forEach((x, i) => x.position = i + 1);
    j.numberOfItems = j.itemListElement.length; rep.itemlist = n0 + '->' + j.numberOfItems;
    s = s.replace(m[0], () => '<script type="application/ld+json">' + JSON.stringify(j, null, 0).replace(/":/g, '": ').replace(/,"/g, ', "') + '</script>');
  }
  rep.mrc_left = (s.match(/mahjong-row|Mahjong Row/g) || []).length;
  v.dispatch({ changes: { from: 0, to: v.state.doc.length, insert: s } });
  return rep;
};
