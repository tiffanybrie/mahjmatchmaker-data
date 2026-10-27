"""Run before ANY partner email/graphics send (Tiffany Oct 27 3:08am: never again be missing a brand without knowing).
Compares the partner email list with the graphics manifest; exits 1 if any partner lacks a graphic or any graphic lacks
a route (email or a named DM). Name variants are normalised (text in parentheses dropped)."""
import csv, json, re, sys
R = '/home/claude/mahjmatchmaker-data'
norm = lambda s: re.sub(r'\s*\(.*\)', '', s).strip().lower()
emails = {norm(r['brand']): r['brand'] for r in csv.DictReader(open(f'{R}/config/fym-partners-email-list-oct26.csv'))}
graphics = {norm(e['brand']): e['brand'] for e in json.load(open(f'{R}/site/livepatch/partner-kit-oct27/manifest.json'))}
DM_ONLY = {'virora mahjong': 'Instagram DM (no email; Tiffany sends, draft in DESK)'}
no_graphic = [emails[k] for k in emails if k not in graphics]
no_route = [graphics[k] for k in graphics if k not in emails and k not in DM_ONLY]
print(f'{len(emails)} brands on the email list, {len(graphics)} graphics, {len(DM_ONLY)} DM-only')
for k, v in DM_ONLY.items(): print('  DM only:', graphics.get(k, k), '->', v)
for b in no_graphic: print('  MISSING GRAPHIC:', b)
for b in no_route: print('  GRAPHIC WITH NO WAY TO SEND:', b)
sys.exit(1 if no_graphic or no_route else 0)
