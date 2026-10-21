/**
 * Mahj Matchmaker site search log (Oct 2026).
 * What people type into the site search, and which searches come back EMPTY.
 *
 * Set up (one time, about 2 minutes):
 *  1. Make a new Google Sheet (name it "Mahj Matchmaker searches").
 *  2. Extensions > Apps Script. Delete what is there, paste this whole file, Save.
 *  3. Deploy > New deployment > gear icon > "Web app".
 *     Execute as: Me.   Who has access: Anyone.   Deploy, then Authorize.
 *  4. Copy the Web app URL (ends in /exec) and send it to Claude. Claude puts it in the
 *     Code Injection snippet as window.MM_SEARCH_LOG_URL.
 *
 * Stores ONLY: the search text, how many results it got, the page it was typed on, and the time.
 * No names, emails, IP addresses or anything else about the visitor (the site never sends any).
 * Tabs: "searches" (one row per search), "top searches" and "no results" (live summaries).
 */
const SHEET = 'searches';

function doPost(e) {
  try {
    const body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const q = String(body.q || '').replace(/\s+/g, ' ').trim().slice(0, 100);
    if (!q) return ok_();
    const n = Number(body.results_count);
    const page = String(body.page || '').slice(0, 120);
    const ts = String(body.ts || '').slice(0, 30);
    const sh = sheet_();
    sh.appendRow([new Date(), q, isFinite(n) ? n : '', page, ts]);
  } catch (err) {
    // ignore bad posts
  }
  return ok_();
}

function doGet() {
  return ContentService.createTextOutput('Mahj Matchmaker search log is on.');
}

function ok_() {
  return ContentService.createTextOutput('ok');
}

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET);
  if (!sh) {
    sh = ss.insertSheet(SHEET, 0);
    sh.appendRow(['when', 'search', 'results', 'page', 'visitor clock']);
    sh.setFrozenRows(1);
    sh.setColumnWidth(2, 260);
    summaries_(ss);
  }
  return sh;
}

function summaries_(ss) {
  let top = ss.getSheetByName('top searches');
  if (!top) {
    top = ss.insertSheet('top searches');
    top.getRange('A1').setFormula(
      '=QUERY(searches!B:C,"select lower(B), count(B), max(C) where B is not null group by lower(B) ' +
      'order by count(B) desc label lower(B) \'search\', count(B) \'times\', max(C) \'results\'",1)');
  }
  let none = ss.getSheetByName('no results');
  if (!none) {
    none = ss.insertSheet('no results');
    none.getRange('A1').setFormula(
      '=QUERY(searches!B:C,"select lower(B), count(B) where C = 0 group by lower(B) ' +
      'order by count(B) desc label lower(B) \'search with no results\', count(B) \'times\'",1)');
  }
}

/** Run once from the editor (Run > setup) if you want the tabs before the first search arrives. */
function setup() {
  sheet_();
}
