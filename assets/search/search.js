/* Mahj Matchmaker site search (Oct 21 2026). Vanilla JS, no dependencies.
 * Loaded site-wide from Settings > Developer Tools > Code Injection > Header (see
 * site/livepatch/search/header-injection.html). Adds a search button to the Squarespace header
 * (desktop + mobile), opens a full-screen overlay, and loads search-index.json (same folder)
 * only when search is first opened.
 *   Open: header icon, "/" or Cmd/Ctrl+K, or ?mmq=<query> on any page. Close: Esc, X, or Back.
 *   Tracking: no GA4 on the site, so queries POST to window.MM_SEARCH_LOG_URL when it is set
 *   ({q, results_count, page, ts}, nothing personal). If gtag ever exists, GA4 events fire too.
 *   Gallery deep links: /mahjong-mats#<img key> scrolls to that mat and highlights it.
 */
(function () {
  'use strict';
  if (window.__mmSearch) return;
  window.__mmSearch = 1;
  var me = document.currentScript;
  var BASE = (me && me.src ? me.src : '').replace(/[^\/]*$/, '');
  var IDX_URL = window.MM_SEARCH_INDEX_URL || BASE + 'search-index.json';
  var TH = IDX_URL.replace(/[^\/]*$/, '') + 'thumbs/';
  var GALLERY = '/mahjong-mats';
  var D = null, DOCS = null, loading = null, ov, inp, res, lb, lastQ = '', pushed = false, logT = null, lastLogged = '';
  var STOPQ = { mat: 1, mats: 1, mahjong: 1, mahj: 1, the: 1, and: 1, tile: 1, tiles: 1, set: 1, sets: 1, by: 1, of: 1, a: 1, game: 1, for: 1, with: 1 };
  var DOT = { pink: '#f2a7c3', red: '#d24b4b', orange: '#f29a5c', yellow: '#efc94c', green: '#5fa36a', teal: '#2fb3a6',
    blue: '#4a78c2', purple: '#a58ad8', neutral: '#eadfcb', earthy: '#a3754f', dark: '#2e3a4c', bw: 'linear-gradient(90deg,#111 50%,#fff 50%)',
    pastel: '#f6d3e0', brights: 'conic-gradient(#f06,#fc0,#0c6,#09f,#f06)', florals: '#e58fb0', animal: '#c69a5a', simple: '#cfd8e3',
    holiday: '#c0392b' };
  var COLOURQ = {};

  /* ---------- text helpers ---------- */
  function fold(s) {
    s = String(s || '');
    try { s = s.normalize('NFD').replace(/[̀-ͯ]/g, ''); } catch (e) {}
    return s.toLowerCase().replace(/❤️?/g, ' heart ').replace(/&/g, ' and ').replace(/['’]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function lev(a, b, max) {
    var m = a.length, n = b.length;
    if (Math.abs(m - n) > max) return max + 1;
    var prev = [], pp = null, cur, i, j;
    for (j = 0; j <= n; j++) prev[j] = j;
    for (i = 1; i <= m; i++) {
      cur = [i]; var best = i;
      for (j = 1; j <= n; j++) {
        var c = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c);
        if (pp && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) cur[j] = Math.min(cur[j], pp[j - 2] + 1);
        if (cur[j] < best) best = cur[j];
      }
      if (best > max) return max + 1;
      pp = prev; prev = cur;
    }
    return prev[n];
  }

  /* ---------- index ---------- */
  function load() {
    if (D) return Promise.resolve(D);
    if (loading) return loading;
    loading = fetch(IDX_URL, { credentials: 'omit' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) { D = j; build(); return D; })
      .catch(function (e) { loading = null; throw e; });
    return loading;
  }
  function doc(type, i, fields, extra) {
    var toks = [], seen = {};
    fields.forEach(function (f) {
      fold(f[0]).split(' ').forEach(function (t) {
        if (!t) return;
        VOCAB[t] = 1;
        var k = t + '|' + f[1];
        if (seen[k]) return; seen[k] = 1;
        toks.push([t, f[1]]);
      });
    });
    var d = { t: type, i: i, toks: toks, name: fold(fields[0][0]) };
    for (var k in extra) d[k] = extra[k];
    return d;
  }
  var VOCAB = {}, VLIST = [];
  function build() {
    DOCS = [];
    var A = D.a, L = D.sec || {};
    Object.keys(L).forEach(function (k) {
      COLOURQ[k] = k;
      fold(L[k]).split(' ').forEach(function (w) { if (w.length > 2 && w !== 'and') COLOURQ[w] = k; });
    });
    COLOURQ.peach = 'orange'; COLOURQ.coral = 'orange'; COLOURQ.mustard = 'yellow'; COLOURQ.gold = 'yellow'; COLOURQ.aqua = 'teal'; COLOURQ.turquoise = 'teal';
    COLOURQ.lilac = 'purple'; COLOURQ.lavender = 'purple'; COLOURQ.ivory = 'neutral'; COLOURQ.cream = 'neutral';
    COLOURQ.brown = 'earthy'; COLOURQ.tan = 'earthy'; COLOURQ.navy = 'blue'; COLOURQ.black = 'bw'; COLOURQ.white = 'bw';
    COLOURQ.moody = 'dark'; COLOURQ.christmas = 'holiday'; COLOURQ.pastel = 'pastel'; COLOURQ.bright = 'brights'; COLOURQ.floral = 'florals';
    delete COLOURQ.multicolor; delete COLOURQ.prints; delete COLOURQ.retired;
    D.m.forEach(function (m, i) {
      DOCS.push(doc('m', i, [[m[1], 10], [m[2], 6], [(m[5] || []).map(function (c) { return L[c] || c; }).join(' ') + ' ' + (m[9] || ''), 3]],
        { rank: m[4] ? -2 : 0 }));
    });
    (D.x || []).forEach(function (x, i) {
      DOCS.push(doc('x', i, [[x[0], 10], [x[1], 6], [x[6] || '', 3]], { rank: -1.5 }));
    });
    A.forEach(function (a, i) {
      DOCS.push(doc('a', i, [[a[1], 10], [a[2], 5], [(a[4] || []).join(' ') + (a[5] === 2 ? ' holiday christmas hanukkah winter' : '') + (a[5] === 1 ? ' colour color guide hub' : ''), 3], [a[7], 0.6]],
        { rank: a[5] === 0 ? 1 : 0 }));
    });
    D.p.forEach(function (p, i) {
      var nm = p[2] === 'brand' ? p[7] : p[1];
      DOCS.push(doc('p', i, [[nm, 10], [p[2] === 'brand' ? p[1] + ' discount code promo code coupon ' + (p[5] || '') : p[1], 4], [p[3], 0.8]],
        { rank: p[2] === 'brand' ? 0.5 : 0 }));
    });
    VLIST = Object.keys(VOCAB);
  }
  /* does the whole site have a word that equals / starts with q? then typo matching is off for q */
  function known(q, last) {
    if (VOCAB[q]) return true;
    if (!(last || q.length >= 3)) return false;
    for (var i = 0; i < VLIST.length; i++) if (VLIST[i].indexOf(q) === 0) return true;
    return false;
  }
  /* best match of one query word in one result: [score, strong]. strong = exact/prefix hit in a main field */
  function matchTok(q, toks, last, fuzzy) {
    var best = 0, strong = false, i, t, s, w;
    for (i = 0; i < toks.length; i++) {
      t = toks[i][0]; w = toks[i][1]; s = 0;
      if (t === q) s = 1;
      else if (t.indexOf(q) === 0 && (q.length >= 3 || last)) s = 0.8;
      else if (fuzzy && q.length >= 4) {
        var tol = q.length >= 8 ? 2 : 1;
        if (lev(q, t, tol) <= tol) s = 0.55;
        else if (last && t.length > q.length && lev(q, t.slice(0, q.length), 1) <= 1) s = 0.45;
        else if (q.length >= 8 && t.length >= 5 && t.length >= q.length * 0.4 && q.indexOf(t) === 0) s = 0.4; /* "papayaspritz" */
      }
      if (s * w > best) best = s * w;
      if (s >= 0.8 && w >= 3) strong = true;
    }
    return [best, strong];
  }
  function search(qs) {
    var q = fold(qs);
    if (!q) return null;
    var qt = q.split(' '), need = qt.filter(function (t) { return !STOPQ[t]; });
    if (!need.length) need = qt;
    var fz = qt.map(function (t, k) { return !known(t, k === qt.length - 1); });
    var col = null;
    qt.forEach(function (t) { if (COLOURQ[t]) col = COLOURQ[t]; });
    var out = { a: [], m: [], b: [], p: [] };
    DOCS.forEach(function (d) {
      var sc = 0, ok = true, strong = true;
      for (var k = 0; k < qt.length; k++) {
        var t = qt[k], r = matchTok(t, d.toks, k === qt.length - 1, fz[k]);
        if (!r[0]) { if (need.indexOf(t) > -1) { ok = false; break; } continue; }
        sc += r[0];
        if (!r[1] && need.indexOf(t) > -1) strong = false;
      }
      if (!ok || sc <= 0) return;
      if (d.name === q) sc += 20; else if (d.name.indexOf(q) === 0) sc += 12; else if ((' ' + d.name + ' ').indexOf(' ' + q + ' ') > -1) sc += 8;
      sc += d.rank;
      if (col && d.t === 'm') { var secs = D.m[d.i][5] || []; var p = secs.indexOf(col); if (p === 0) sc += 10; else if (p > 0) sc += 7 - Math.min(p, 4) * 0.5; }
      var g = d.t === 'm' || d.t === 'x' ? 'm' : d.t === 'a' ? 'a' : (D.p[d.i][2] === 'brand' ? 'b' : 'p');
      out[g].push([sc, d, strong]);
    });
    var top = 0;
    ['a', 'm', 'b', 'p'].forEach(function (g) {
      out[g].sort(function (x, y) { return y[0] - x[0] || (x[1].name < y[1].name ? -1 : 1); });
      if (out[g].length) top = Math.max(top, out[g][0][0]);
    });
    /* weak hits (typo matches, descriptions) must be reasonably close to the best result */
    ['a', 'm', 'b', 'p'].forEach(function (g) {
      var gt = out[g].length ? out[g][0][0] : 0;
      out[g] = out[g].filter(function (r) { return r[2] || (r[0] >= gt * 0.3 && r[0] >= top * 0.2); });
    });
    /* a tile set search ("papaya spritz", "lagoon") lists that album's mats in Tiffany's order, top picks first */
    out.album = null;
    if (out.a.length && out.a[0][0] >= 9 && out.a[0][0] >= top - 0.01 && out.a[0][1].t === 'a' && D.a[out.a[0][1].i][5] !== 1 && (!out.a[1] || out.a[0][0] - out.a[1][0] >= 4)) {
      var ai = out.a[0][1].i, ord = D.a[ai][8] || [], have = {}, lead = [];
      out.m.forEach(function (r) { have[r[1].t + r[1].i] = r; });
      ord.forEach(function (v, pos) {
        var key = v >= 0 ? 'm' + v : 'x' + (-v - 1), r = have[key];
        if (!r) r = [0, DOCS.filter(function (d) { return d.t === key.charAt(0) && d.i === +key.slice(1); })[0], true];
        if (r[1]) { lead.push(r); have[key] = null; }
      });
      out.album = ai;
      out.m = lead.concat(out.m.filter(function (r) { return have[r[1].t + r[1].i]; }));
    }
    out.n = out.a.length + out.m.length + out.b.length + out.p.length;
    return out;
  }

  /* ---------- urls ---------- */
  function matImg(key, full) {
    if (!full && (D.nt || []).indexOf(key) < 0) return TH + 'm/' + key + '.webp';
    var b = D.mb; if (D.ib && D.ib[key]) b = b.replace(/@[0-9a-f]+\//, '@' + D.ib[key] + '/');
    return b + key + '.webp';
  }
  function th(u) { return !u ? '' : u.charAt(0) === '@' ? TH + u.slice(1) : u; }
  function albumLink(ai) { var a = D.a[ai]; return a ? '<a href="' + esc(a[0]) + '">' + esc(a[1].replace(/ \(holiday\)$/, '')) + (a[5] === 2 ? ' holiday' : '') + ' album</a>' : ''; }
  var PREF = null; /* album the current search is about: listed first on each mat */
  function albumsLine(list) {
    list = (list || []).filter(function (a) { return D.a[a] && D.a[a][5] !== 1; });
    if (PREF != null && list.indexOf(PREF) > 0) list = [PREF].concat(list.filter(function (a) { return a !== PREF; }));
    if (!list.length) return '';
    var s = list.slice(0, 2).map(albumLink).join(', ');
    if (list.length > 2) s += ' <span class="mms-more">+' + (list.length - 2) + ' more</span>';
    return '<div class="mms-al">In the ' + s + '</div>';
  }
  function chips(secs) {
    var L = D.sec || {}, h = '';
    (secs || []).slice(0, 3).forEach(function (c) {
      if (!L[c]) return;
      h += '<span class="mms-chip"><i style="background:' + (DOT[c] || '#ccc') + '"></i>' + esc(L[c]) + '</span>';
    });
    return h;
  }

  /* ---------- render ---------- */
  var LIMIT = { a: 6, m: 24, b: 6, p: 6 }, shown = {};
  function rMat(d) {
    if (d.t === 'x') {
      var x = D.x[d.i];
      return '<li class="mms-it mms-mat"><button type="button" class="mms-th" data-x="' + d.i + '" aria-label="See ' + esc(x[0]) + ' bigger"><img src="' + esc(th(x[5])) + '" alt="" loading="lazy" decoding="async"></button>' +
        '<div class="mms-tx"><button type="button" class="mms-nm" data-x="' + d.i + '">' + esc(x[0]) + '</button><div class="mms-br">' + esc(x[1]) + (x[4] ? ' <span class="mms-ret">Retired</span>' : '') + '</div>' +
        albumsLine(x[2]) + '<div class="mms-acts">' + (x[3] ? '<a class="mms-btn" href="' + esc(x[3]) + '" target="_blank" rel="sponsored noopener">Shop</a>' : '') +
        (x[2] && D.a[x[2][0]] ? '<a class="mms-btn mms-ghost" href="' + esc(D.a[x[2][0]][0]) + '">See the match</a>' : '') + '</div></div></li>';
    }
    var m = D.m[d.i];
    return '<li class="mms-it mms-mat"><button type="button" class="mms-th" data-m="' + d.i + '" aria-label="See ' + esc(m[1]) + ' bigger"><img src="' + esc(matImg(m[0])) + '" alt="" loading="lazy" decoding="async"></button>' +
      '<div class="mms-tx"><button type="button" class="mms-nm" data-m="' + d.i + '">' + esc(m[1]) + '</button><div class="mms-br">' + esc(m[2]) + (m[4] ? ' <span class="mms-ret">Retired</span>' : '') + '</div>' +
      '<div class="mms-chips">' + chips(m[5]) + '</div>' + albumsLine(m[7]) +
      '<div class="mms-acts">' + (m[3] ? '<a class="mms-btn" href="' + esc(m[3]) + '" target="_blank" rel="sponsored noopener">Shop</a>' : '') +
      '<a class="mms-btn mms-ghost" href="' + GALLERY + '#' + esc(m[0]) + '">See in gallery</a></div></div></li>';
  }
  function rAlbum(d) {
    var a = D.a[d.i];
    var sub = a[5] === 1 ? 'Colour guide' : (a[2] ? esc(a[2]) : '') + (a[6] ? (a[2] ? ' · ' : '') + a[6] + ' mat match' + (a[6] === 1 ? '' : 'es') : '');
    return '<li class="mms-it mms-alb"><a class="mms-card" href="' + esc(a[0]) + '"><span class="mms-th">' + (a[3] ? '<img src="' + esc(th(a[3])) + '" alt="" loading="lazy" decoding="async">' : '') + '</span>' +
      '<span class="mms-tx"><span class="mms-nm">' + esc(a[1]) + '</span><span class="mms-br">' + sub + '</span></span></a></li>';
  }
  function rPage(d) {
    var p = D.p[d.i], brand = p[2] === 'brand';
    return '<li class="mms-it mms-pg"><a class="mms-card" href="' + esc(p[0]) + '"><span class="mms-th">' + (p[4] ? '<img src="' + esc(p[4]) + '" alt="" loading="lazy" decoding="async">' : '') + '</span>' +
      '<span class="mms-tx"><span class="mms-nm">' + esc(brand ? p[7] : p[1]) + '</span>' +
      (brand ? '<span class="mms-br">' + (p[5] ? '<span class="mms-code">' + esc(p[5]) + '</span>' + (p[6] ? ' ' + esc(p[6]) + '% off' : '') : 'Brand guide') + '</span>' :
        '<span class="mms-ds">' + esc(p[3]) + '</span>') + '</span></a></li>';
  }
  var TITLES = { a: 'Tile set albums', m: 'Mats', b: 'Brands & codes', p: 'Articles & pages' };
  function render(q) {
    if (!D) return;
    lastQ = q;
    var r = search(q);
    if (!r) { res.innerHTML = idle(); return; }
    PREF = r.album;
    /* groups in order of their best hit (albums win ties); a brand search puts the brand + code card first */
    var bias = { a: 4, m: 0, b: 1, p: -2 };
    var order = ['a', 'm', 'b', 'p'].sort(function (x, y) {
      function t(g) { return r[g].length ? r[g][0][0] + bias[g] : -1e9; }
      return t(y) - t(x);
    });
    if (r.album != null) order = ['a', 'm'].concat(order.filter(function (g) { return g !== 'a' && g !== 'm'; }));
    var h = '';
    if (!r.n) {
      h = '<div class="mms-empty"><p>No matches for <b>' + esc(q) + '</b> yet.</p><p>Try a tile set (Lagoon), a brand (Sunday Mahjong) or a colour (pink).</p>' +
        '<p><a class="mms-btn mms-ghost" href="' + GALLERY + '">Browse every mat by colour</a> <a class="mms-btn mms-ghost" href="/request-an-album">Request an album</a></p></div>';
    }
    order.forEach(function (g) {
      var L = r[g]; if (!L.length) return;
      var lim = shown[g] || LIMIT[g];
      var ttl = g === 'm' && r.album != null ? 'Mats <span class="mms-sub">' + esc(D.a[r.album][1].replace(/ \(holiday\)$/, '')) + ' matches first, in my order</span>' : TITLES[g];
      h += '<section class="mms-grp mms-g-' + g + '"><h3>' + ttl.replace(/( <span class="mms-sub">|$)/, ' <small>' + L.length + '</small>$1') + '</h3><ul>';
      L.slice(0, lim).forEach(function (x) { h += g === 'm' ? rMat(x[1]) : g === 'a' ? rAlbum(x[1]) : rPage(x[1]); });
      h += '</ul>' + (L.length > lim ? '<button type="button" class="mms-showall" data-g="' + g + '">Show all ' + L.length + '</button>' : '') + '</section>';
    });
    res.innerHTML = h;
    res.scrollTop = 0;
    queueLog(q, r.n);
  }
  function idle() {
    var s = ['Papaya Spritz', 'Sunday Mahjong', 'Lagoon', 'pink', 'holiday', 'leopard', 'MAHJMATCH'];
    return '<div class="mms-idle"><p>Search ' + (D ? D.m.length + ' mats, ' + D.a.filter(function (a) { return a[5] === 0; }).length + ' tile set albums and every brand code' : 'mats, tile sets and brands') + '.</p><div class="mms-sugg">' +
      s.map(function (x) { return '<button type="button" data-q="' + esc(x) + '">' + esc(x) + '</button>'; }).join('') + '</div></div>';
  }

  /* ---------- tracking ---------- */
  function queueLog(q, n) {
    clearTimeout(logT);
    logT = setTimeout(function () { sendLog(q, n); }, 1200);
  }
  function sendLog(q, n) {
    clearTimeout(logT);
    q = String(q || '').trim().slice(0, 100);
    if (q.length < 2 || q.toLowerCase() === lastLogged) return;
    lastLogged = q.toLowerCase();
    try {
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'search', { search_term: q });
        if (!n) window.gtag('event', 'search_no_results', { search_term: q });
      }
    } catch (e) {}
    var url = window.MM_SEARCH_LOG_URL;
    if (!url) return;
    var body = JSON.stringify({ q: q, results_count: n, page: location.pathname, ts: new Date().toISOString() });
    try {
      if (navigator.sendBeacon && navigator.sendBeacon(url, new Blob([body], { type: 'text/plain;charset=UTF-8' }))) return;
    } catch (e) {}
    try { fetch(url, { method: 'POST', mode: 'no-cors', body: body, headers: { 'Content-Type': 'text/plain;charset=UTF-8' }, keepalive: true }); } catch (e) {}
  }

  /* ---------- overlay ---------- */
  var ICON = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>';
  function makeOverlay() {
    if (ov) return;
    ov = document.createElement('div');
    ov.className = 'mms-ov'; ov.hidden = true;
    ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Search Mahj Matchmaker');
    ov.innerHTML = '<div class="mms-top"><label class="mms-field">' + ICON + '<input type="search" class="mms-in" placeholder="Search mats, brands, tile sets" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" aria-label="Search"></label>' +
      '<button type="button" class="mms-x" aria-label="Close search">Close</button></div><div class="mms-res" aria-live="polite"></div>' +
      '<div class="mms-lb" hidden><div class="mms-lbin"><button type="button" class="mms-lbx" aria-label="Close photo">&times;</button><img alt=""><div class="mms-lbtx"></div></div></div>';
    document.body.appendChild(ov);
    inp = ov.querySelector('.mms-in'); res = ov.querySelector('.mms-res'); lb = ov.querySelector('.mms-lb');
    var t = null;
    inp.addEventListener('input', function () { shown = {}; clearTimeout(t); var v = inp.value; t = setTimeout(function () { render(v); }, D && D.m.length > 0 ? 60 : 0); });
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); if (D) { var r = search(inp.value); sendLog(inp.value, r ? r.n : 0); } inp.blur(); } });
    ov.querySelector('.mms-x').addEventListener('click', function () { close(); });
    res.addEventListener('click', function (e) {
      var b = e.target.closest('[data-q]');
      if (b) { inp.value = b.getAttribute('data-q'); render(inp.value); return; }
      var s = e.target.closest('.mms-showall');
      if (s) { shown[s.getAttribute('data-g')] = 1e4; render(lastQ); return; }
      var m = e.target.closest('[data-m],[data-x]');
      if (m) { photo(m.hasAttribute('data-m') ? 'm' : 'x', +(m.getAttribute('data-m') || m.getAttribute('data-x'))); return; }
      follow(e);
    });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.closest('.mms-lbx')) { lb.hidden = true; return; } follow(e); });
  }
  /* an internal link inside search: close the overlay first (same-page #anchors scroll after it closes) */
  function follow(e) {
    var a = e.target.closest('a[href]');
    if (!a || a.target === '_blank') return;
    var u = new URL(a.href, location.href);
    if (u.pathname === location.pathname && u.hash) {
      e.preventDefault(); close(true);
      setTimeout(function () { if (location.hash === u.hash) galleryJump(); else location.hash = u.hash; var el = document.getElementById(u.hash.slice(1)); if (el) el.scrollIntoView({ block: 'start' }); }, 30);
      return;
    }
    close(true);
  }
  function photo(kind, i) {
    var img = lb.querySelector('img'), tx = lb.querySelector('.mms-lbtx'), h;
    if (kind === 'm') {
      var m = D.m[i];
      img.src = matImg(m[0], true); img.alt = m[2] + ' ' + m[1] + ' mahjong mat';
      h = '<b>' + esc(m[1]) + '</b><span>' + esc(m[2]) + (m[4] ? ' · Retired' : '') + '</span><div class="mms-acts">' +
        (m[3] ? '<a class="mms-btn" href="' + esc(m[3]) + '" target="_blank" rel="sponsored noopener">Shop the mat</a>' : '') +
        '<a class="mms-btn mms-ghost" href="' + GALLERY + '#' + esc(m[0]) + '">See in gallery</a></div>';
    } else {
      var x = D.x[i];
      img.src = x[7] || th(x[5]); img.alt = x[1] + ' ' + x[0] + ' mahjong mat';
      h = '<b>' + esc(x[0]) + '</b><span>' + esc(x[1]) + '</span><div class="mms-acts">' +
        (x[3] ? '<a class="mms-btn" href="' + esc(x[3]) + '" target="_blank" rel="sponsored noopener">Shop the mat</a>' : '') +
        (D.a[x[2][0]] ? '<a class="mms-btn mms-ghost" href="' + esc(D.a[x[2][0]][0]) + '">See the match</a>' : '') + '</div>';
    }
    tx.innerHTML = h;
    lb.hidden = false;
    lb.querySelector('.mms-lbx').focus({ preventScroll: true });
  }
  function open(q) {
    makeOverlay();
    if (!ov.hidden) { if (q != null) { inp.value = q; render(q); } return; }
    ov.hidden = false;
    document.documentElement.classList.add('mms-lock');
    try { history.pushState({ mms: 1 }, ''); pushed = true; } catch (e) { pushed = false; }
    if (q != null) inp.value = q;
    setTimeout(function () { inp.focus(); }, 30);
    if (!D) res.innerHTML = '<div class="mms-idle"><p>Loading search&hellip;</p></div>';
    load().then(function () { if (inp.value.trim()) render(inp.value); else res.innerHTML = idle(); })
      .catch(function () { res.innerHTML = '<div class="mms-empty"><p>Search could not load. Please check your connection and try again.</p></div>'; });
  }
  function close(nav) {
    if (!ov || ov.hidden) return;
    if (inp.value.trim() && D) { var r = search(inp.value); sendLog(inp.value, r ? r.n : 0); }
    ov.hidden = true; lb.hidden = true;
    document.documentElement.classList.remove('mms-lock');
    if (pushed && !nav) { pushed = false; try { history.back(); } catch (e) {} }
    else if (pushed && nav) { pushed = false; try { history.replaceState(null, ''); } catch (e) {} }
  }
  window.addEventListener('popstate', function () { if (ov && !ov.hidden) { pushed = false; close(true); } });
  window.MMSearch = { open: open, close: close };

  /* ---------- header buttons ---------- */
  function addButtons() {
    var header = document.querySelector('header#header, header.header');
    var made = 0;
    if (header) {
      header.querySelectorAll('.header-display-desktop, .header-display-mobile').forEach(function (disp) {
        if (disp.querySelector('.mms-hbtn')) { made++; return; }
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'mms-hbtn'; b.setAttribute('aria-label', 'Search the site'); b.innerHTML = ICON;
        b.addEventListener('click', function (e) { e.preventDefault(); open(); });
        var burger = disp.querySelector('.header-burger'), title = disp.querySelector('.header-title');
        if (disp.classList.contains('header-display-mobile') && burger) burger.parentNode.insertBefore(b, burger);
        else if (title) title.appendChild(b);
        else if (burger) burger.parentNode.insertBefore(b, burger);
        else disp.appendChild(b);
        made++;
      });
    }
    if (!made && !document.querySelector('.mms-fab')) {
      var f = document.createElement('button');
      f.type = 'button'; f.className = 'mms-hbtn mms-fab'; f.setAttribute('aria-label', 'Search the site'); f.innerHTML = ICON;
      f.addEventListener('click', function () { open(); });
      document.body.appendChild(f);
    }
  }

  /* ---------- keyboard + deep link ---------- */
  document.addEventListener('keydown', function (e) {
    var t = e.target, typing = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); if (ov && !ov.hidden) inp.focus(); else open(); return; }
    if (e.key === '/' && !typing && !e.metaKey && !e.ctrlKey && !e.altKey) { e.preventDefault(); open(); return; }
    if (e.key === 'Escape' && ov && !ov.hidden) { e.preventDefault(); if (!lb.hidden) lb.hidden = true; else close(); }
  });
  function deepLink() {
    var q = null;
    try { q = new URLSearchParams(location.search).get('mmq'); } catch (e) {}
    if (q == null) return;
    try { var u = new URL(location.href); u.searchParams.delete('mmq'); history.replaceState(history.state, '', u.pathname + u.search + u.hash); } catch (e) {}
    open(q);
  }

  /* ---------- Mat Gallery: scroll to /mahjong-mats#<img key> ---------- */
  function galleryJump() {
    if (location.pathname.replace(/\/$/, '') !== GALLERY) return;
    var key = decodeURIComponent((location.hash || '').slice(1));
    if (!key || !/^[a-z0-9-]+$/.test(key)) return;
    var tries = 0;
    (function look() {
      var imgs = document.querySelectorAll('.mmg-card img[src*="/' + key + '.webp"]');
      if (!imgs.length) { if (++tries < 40) setTimeout(look, 250); return; }
      var card = null;
      imgs.forEach(function (im) { var c = im.closest('.mmg-card'); if (!card && c && c.offsetParent !== null) card = c; });
      if (!card) {
        /* hidden by a filter: reset to All, and show retired mats if it is retired */
        var all = document.querySelector('.mmg-chip[data-f="all"]'); if (all && all.getAttribute('aria-pressed') !== 'true') all.click();
        var c0 = imgs[0].closest('.mmg-card'), tog = document.querySelector('.mmg-tog');
        if (c0 && c0.getAttribute('data-r') && tog && tog.getAttribute('aria-pressed') === 'true') tog.click();
        var sel = document.querySelector('.mmg-brand-sel'); if (sel && sel.value) { sel.value = ''; sel.dispatchEvent(new Event('change')); }
        imgs = document.querySelectorAll('.mmg-card img[src*="/' + key + '.webp"]');
        imgs.forEach(function (im) { var c = im.closest('.mmg-card'); if (!card && c && c.offsetParent !== null) card = c; });
      }
      if (!card) return;
      card.scrollIntoView({ block: 'center', behavior: 'smooth' });
      card.classList.add('mms-hit'); window.__mmsJumped = key;
      setTimeout(function () { card.classList.remove('mms-hit'); }, 3200);
    })();
  }
  window.addEventListener('hashchange', galleryJump);

  function init() { addButtons(); deepLink(); galleryJump(); setTimeout(addButtons, 1500); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
