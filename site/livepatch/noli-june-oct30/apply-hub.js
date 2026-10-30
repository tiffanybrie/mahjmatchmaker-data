// Run in the Squarespace editor tab with the hub code block (.mmtk + #all-codes) open in CodeMirror 6.
// Usage: await MMNOLI(specUrl)  -> returns a report; dispatches only if EVERY find occurs exactly once.
window.MMNOLI = async function (specUrl) {
  const spec = await (await fetch(specUrl)).json();
  const v = document.querySelector('.cm-editor .cm-content').cmTile.view;
  let src = v.state.doc.toString(); const rep = [];
  for (const p of spec.codeBlockPatches) {
    const n = src.split(p.find).length - 1; rep.push([p.find.slice(0, 60), n]);
    if (n !== 1) return { ok: false, rep };
  }
  for (const p of spec.codeBlockPatches) src = src.replace(p.find, () => p.replace);
  v.dispatch({ changes: { from: 0, to: v.state.doc.length, insert: src } });
  return { ok: true, rep, len: src.length };
};
