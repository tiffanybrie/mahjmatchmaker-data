// Mahjong Row & Co. ended our affiliate account Nov 5 2026: neutralise the code on /mahjong-row-and-co-discount-code.
// Run inside the open CM6 code block in Squarespace. Returns counts; nothing saved until you click Save.
window.MMMRC = function () {
  const v = document.querySelector('.cm-editor .cm-content').cmTile.view;
  let s = v.state.doc.toString(); const before = s.length; const rep = {};
  const NOTE = '<p><strong>Note:</strong> Mahjong Row &amp; Co. is no longer offering our code.</p>';
  const sub = (k, re, to) => { const m = s.match(re); rep[k] = m ? m.length : 0; s = s.replace(re, to); };
  sub('perk', /<p><strong>A thank-you for Mahj Matchmaker readers:<\/strong> use code <span class="code">MAHJMATCH<\/span> for 10% off at Mahjong Row &amp; Co\.<\/p>/g, NOTE);
  sub('verified', /<p style="font-size:14px;opacity:\.75;margin:6px 0 14px">&#10003; Code verified [^<]*<\/p>/g, '');
  sub('ref_q_amp', /\?sca_ref=[^"&#]*&/g, '?');
  sub('ref_amp', /&(amp;)?sca_ref=[^"&#]*/g, '');
  sub('ref_q', /\?sca_ref=[^"&#]*/g, '');
  sub('rel', /(href="https:\/\/mahjongrowandco\.com[^"]*"[^>]*?)rel="sponsored noopener"/g, '$1rel="noopener"');
  sub('dek', / Plus, my Mahjong Row &amp; Co\. discount code for readers\./g, '');
  sub('h2', /<h2>Mahjong Row &amp; Co\. Discount Code<\/h2>/g, '<h2>Shop Mahjong Row &amp; Co.</h2>');
  sub('faq_html', /Yes\. Code MAHJMATCH saves 10% on eligible Mahjong Row &amp; Co\. products\. Enter it in the discount code box at checkout\./g, 'Not through us any more: Mahjong Row &amp; Co. is no longer offering our code.');
  sub('faq_ld', /Yes\. Code MAHJMATCH saves 10% on eligible Mahjong Row & Co\. products\. Enter it in the discount code box at checkout\./g, 'Not through us any more: Mahjong Row & Co. is no longer offering our code.');
  const left = []; let i = -1; while ((i = s.indexOf('MAHJMATCH', i + 1)) >= 0) left.push(s.slice(Math.max(0, i - 80), i + 40));
  rep.sca_left = (s.match(/sca_ref/g) || []).length;
  v.dispatch({ changes: { from: 0, to: v.state.doc.length, insert: s } });
  return { rep, left, before, after: s.length };
};
