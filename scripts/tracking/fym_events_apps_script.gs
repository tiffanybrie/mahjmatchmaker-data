/**
 * Find Your Match anonymous event counter (Tiffany, Oct 2026).
 * Paste into a Google Sheet: Extensions > Apps Script. Then Deploy > New deployment >
 * type "Web app", Execute as "Me", Who has access "Anyone". Copy the Web app URL and send it to Claude.
 * Stores NO names, emails or IP addresses: only what was swiped/saved/clicked and when.
 */
const SHEET = 'events';
function doPost(e) {
  const sh = sheet_();
  let rows = [];
  try {
    const body = JSON.parse(e.postData.contents || '{}');
    const list = Array.isArray(body.events) ? body.events : [body];
    rows = list.slice(0, 50).map(ev => [
      new Date(), String(ev.t || '').slice(0, 20), String(ev.set || '').slice(0, 80),
      String(ev.mat || '').slice(0, 120), String(ev.rack || '').slice(0, 120),
      String(ev.x || '').slice(0, 120), String(ev.sid || '').slice(0, 12)
    ]);
  } catch (err) { rows = []; }
  if (rows.length) sh.getRange(sh.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
  return ContentService.createTextOutput('ok');
}
function doGet() { return ContentService.createTextOutput('Find Your Match counter is on.'); }
function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET);
  if (!sh) {
    sh = ss.insertSheet(SHEET);
    sh.appendRow(['when', 'event', 'tile set', 'mat', 'rack', 'extra', 'visit']);
    sh.setFrozenRows(1);
  }
  return sh;
}
