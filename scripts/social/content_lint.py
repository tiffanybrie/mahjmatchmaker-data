"""Social content lint: a gate for captions before anything goes into Planoly (Tiffany, Oct 21).

Why: the posted Papaya hotline reel still showed the old 5-button profile row after she moved the profile UI to
X + heart only. Her standing rule: when a piece of content changes, scrub every other draft or final piece for the
same problem. This script is the caption half of that scrub (scripts/social/content_lint.py --images is not a thing:
images are checked by eye on contact sheets, see assets/social/README.md).

Checks (FAIL = exit 1):
  banned-word   crush / nope / pass (the profile UI says X, heart and "match", never swipe-app wording)
  code          TEACHMAHJ (teacher-only OMM code, doc 98) or any discount code other than MAHJMATCH
  old-profile   retired Papaya profile answers ("long-term mat partner", "coordinating racks", "beige tablecloth")
  icons         star / lightning / rewind glyphs (old 5-button row) in caption text
  naming        the tool is "Find Your Mat-ch" (Tiffany, Oct 21 11:26 FINAL; CLAUDE.md "Naming"): "Find Your Match" FAILS;
                "mat-ch card" FAILS (album cards are plain "match cards"). In art, "Your" is italic and the TM sits on the most
                prominent use only; captions are plain text, so "Find Your Mat-ch" (TM optional) is the caption form.
  length        Instagram/Facebook caption over 350 characters before the hashtags (no long colour-theory captions)
                Pinterest descriptions get 500 (Pinterest's own limit) since they are SEO copy.
RULES AUDIT GA1 (Oct 30, docs/RULES-ENFORCEMENT-AUDIT.md section 12), IG/FB captions (not Pinterest unless noted):
  mahjmatch-missing  IG/FB caption without MAHJMATCH typed out (Oct 26 11:56pm). Skipped when Tigre de Tartán is named
                     (TdT policy wins: the code may not sit next to their name).
  hashtag            no #MahjMatch (Oct 26 2:37pm); waived when Tigre de Tartán is named (see tdt-policy)
  banned-phrase      "saves you money", "every mat", "every brand", "all the mats", "still available", "still in stock",
                     "(affiliate)", Tinder/Hinge/Bumble/Bachelor (BRAND-GUIDE)
  short-brand        "Bam Bird" without Boutique, "My Fair" without Mahjong, "Mahjong Row" without "& Co"
  no-feature         Yellow Mountain / YMI / Kaleidoscope / Paige Spearin in an IG/FB caption
  tdt-policy         Tigre de Tartán (Tigre / Tartán / TdT / @tigredetartan) and MAHJMATCH (code or #MahjMatch) in the SAME
                     caption, ANY platform. Plain "Tartan" (mat names like Tartan Tidings) is not the brand.
                     (TdT affiliate policy Oct 29; Tiffany Oct 30 12:00am: the TdT code is shown only as an image)
  maison-mahj        Maison Mahj's code called "new" (Oct 29 11:07pm: not a new code)
  --codes-list       the doc 94 weekly typed codes list: exempt from the length check ONLY.
New-kind hits on content that already existed on Oct 30 are listed in config/social/content_lint_baseline.json and
reported as WARN (cleanup is on docs/DESK.md); anything new FAILs.
Reminder boxes ("🛑 TIFFANY ... 🛑" up to the ———— line) are instructions to Tiffany: they are checked for codes and
banned words but do not count toward length.

Usage:
  python3 scripts/social/content_lint.py                       # every repo caption file (assets/**/*caption*.txt, s2 captions.json)
  python3 scripts/social/content_lint.py --planoly a.json b.json   # Planoly list_post_groups exports (saved JSON)
  python3 scripts/social/content_lint.py path/to/caption.txt ...   # specific files
  --only-ig   skip Pinterest posts   --warn   report only, always exit 0
Posted/archived captions are listed in ARCHIVE below: they are reported as INFO, not FAIL.
"""
import sys, os, re, json, glob, argparse, datetime

NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ALLOWED_CODES = {'MAHJMATCH'}
BANNED = re.compile(r"\b(crush(?:es|ed|ing)?|nope[sd]?|pass(?:es|ed)?)\b", re.I)
OLD_PROFILE = re.compile(r"long[- ]term mat partner|coordinating racks|beige tablecloth", re.I)
FYM_OLD = re.compile(r"find\s+your\s+match\b", re.I)
MATCH_CARD = re.compile(r"mat-ch\s+cards?", re.I)
ICONS = re.compile('[★☆⚡↺↻⟲⟳\U0001F31F⭐]')  # ★ ☆ ⚡ ↺ ↻ ⟲ ⟳ 🌟 ⭐
CODE_AFTER_WORD = re.compile(r"\bcodes?\b\s*[:\-]?\s*[\"'“]?([A-Z][A-Z0-9]{3,})\b")
CODE_SHAPE = re.compile(r"\b([A-Z]{3,}\d{1,3}|TEACHMAHJ)\b")
MAHJMATCH = re.compile(r"(?<!#)\bMAHJMATCH\b", re.I)      # the code typed out (the #MahjMatch hashtag does not count)
MAHJMATCH_ANY = re.compile(r"MAHJMATCH", re.I)               # code OR hashtag (TdT policy: neither next to their name)
HASHTAG = re.compile(r"#mahjmatch\b", re.I)
BANNED_PHRASE = re.compile(r"saves? you money|\bevery mats?\b(?!-)|\bevery brands?\b|\ball the mats\b|still available|still in stock|"
                           r"\(affiliate\)|\btinder\b|\bhinge\b|\bbumble\b|\bbachelor(?:ette)?\b", re.I)
SHORT_BRAND = re.compile(r"\bBam Bird\b(?! Boutique)|\bMy Fair\b(?! Mahjong)|\bMahjong Row\b(?!\s*(?:&|&amp;|and)\s*Co)")
NO_FEATURE = re.compile(r"yellow mountain|\bYMI\b|kaleidoscope|paige spearin", re.I)
TDT = re.compile(r"\btigre\b|tart[áÁ]n|\bTdT\b|@tigredetartan", re.I)
MAISON_NEW = re.compile(r"maison mahj[^.\n]{0,80}\bnew\b[^.\n]{0,20}\bcode|\bnew\b[^.\n]{0,20}\bcode[^.\n]{0,80}maison mahj", re.I)
NEW_KINDS = {'mahjmatch-missing', 'hashtag', 'banned-phrase', 'short-brand', 'no-feature', 'tdt-policy', 'maison-mahj'}
BASELINE_PATH = os.path.join(R, 'config', 'social', 'content_lint_baseline.json')
LIMIT = {'instagram': 350, 'facebook': 350, 'pinterest': 500, 'file': 350}
# Already posted: kept for the record, linted as INFO only. Add a path here only once the post is live.
ARCHIVE = {
    'assets/social/papaya-spritz-launch/caption-carousel.txt',   # posted Oct 21 (intro carousel)
    'assets/social/papaya-spritz-launch/caption-reel.txt',       # posted Oct 21 (hotline reel, v11)
    'assets/social/papaya-spritz-launch/caption-intro.txt',      # posted Oct 21 (intro carousel, short caption)
}


def split_box(text):
    """Return (instructions, caption). The 🛑 box runs up to the first line of em dashes."""
    if '🛑' not in text:
        return '', text
    m = re.search(r'^\s*[—\-_]{6,}\s*$', text, re.M)
    if not m:
        return text, ''          # whole thing is instructions (story reminder with no caption)
    return text[:m.start()], text[m.end():]


def before_hashtags(caption):
    lines = caption.strip().split('\n')
    while lines and (not lines[-1].strip() or re.fullmatch(r'(#\S+\s*)+', lines[-1].strip())):
        lines.pop()
    body = '\n'.join(lines)
    return re.sub(r'(\s#\w+)+\s*$', '', body).strip()


def lint(text, platform='file', codes_list=False):
    out = []
    box, cap = split_box(text)
    for part, where in ((cap, 'caption'), (box, 'reminder box')):
        if not part:
            continue
        for m in BANNED.finditer(part):
            out.append(('banned-word', f'"{m.group(0)}" in {where}'))
        for m in OLD_PROFILE.finditer(part):
            out.append(('old-profile', f'"{m.group(0)}" in {where}'))
        for m in FYM_OLD.finditer(part):
            out.append(('naming', f'"{m.group(0)}" in {where} -> "Find Your Mat-ch"'))
        for m in MATCH_CARD.finditer(part):
            out.append(('naming', f'"{m.group(0)}" in {where} -> "match card" (album cards are not the tool)'))
        for m in ICONS.finditer(part):
            out.append(('icons', f'{m.group(0)!r} in {where}'))
        codes = {c for c in CODE_AFTER_WORD.findall(part)} | set(CODE_SHAPE.findall(part))
        for c in sorted(codes - ALLOWED_CODES):
            out.append(('code', f'{c} in {where} (only MAHJMATCH)'))
    if cap:
        body = before_hashtags(cap); lim = LIMIT.get(platform, 350)
        if len(body) > lim and not codes_list:
            out.append(('length', f'{len(body)} chars before hashtags (limit {lim})'))
        social = platform in ('instagram', 'facebook', 'file')
        tdt = TDT.search(cap)
        if tdt and MAHJMATCH_ANY.search(cap):
            out.append(('tdt-policy', f'"{tdt.group(0)}" and MAHJMATCH in the same caption (TdT code only as an image)'))
        for m in MAISON_NEW.finditer(cap):
            out.append(('maison-mahj', f'"{m.group(0)[:60]}": Maison Mahj\'s code is not new'))
        if social:
            if not tdt and not MAHJMATCH.search(cap):
                out.append(('mahjmatch-missing', 'caption has no MAHJMATCH typed out'))
            if not tdt and not HASHTAG.search(cap):
                out.append(('hashtag', 'no #MahjMatch'))
            for m in BANNED_PHRASE.finditer(cap):
                out.append(('banned-phrase', f'"{m.group(0)}"'))
            for m in SHORT_BRAND.finditer(cap):
                out.append(('short-brand', f'"{m.group(0)}" -> full brand name'))
            for m in NO_FEATURE.finditer(cap):
                out.append(('no-feature', f'"{m.group(0)}" (never featured on social)'))
    return out


def repo_files():
    fs = sorted(set(glob.glob(R + '/assets/**/*caption*.txt', recursive=True)))
    return [os.path.relpath(f, R) for f in fs]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--planoly', nargs='+', default=[])
    ap.add_argument('--only-ig', action='store_true')
    ap.add_argument('--warn', action='store_true')
    ap.add_argument('--codes-list', action='store_true', help='doc 94 typed codes list: exempt from the length check only')
    ap.add_argument('--write-baseline', action='store_true', help='record current new-kind hits as legacy WARN (Oct 30 only)')
    a = ap.parse_args()
    try:
        baseline = set(tuple(x) for x in json.load(open(BASELINE_PATH))['items'])
    except Exception:
        baseline = set()
    new_hits = []
    items = []   # (label, platform, text, archived)
    for p in a.planoly:
        d = json.load(open(p))
        for g in d.get('postGroups', []):
            for post in g.get('posts', []):
                if post.get('status') == 'published':
                    continue
                # reminder posts stay 'scheduled' forever; once the reminder went out and the date passed, it was posted
                if post.get('reminderSentAt') and (post.get('scheduleDate') or '') < NOW:
                    continue
                if a.only_ig and post.get('platform') == 'pinterest':
                    continue
                pt = (post.get('providerSettings') or {}).get('postType', '')
                label = f"planoly {post.get('platform')} {pt} {post.get('status')} {post.get('scheduleDate') or 'no date'} {post['postId']}"
                items.append((label, post.get('platform', 'instagram'), post.get('caption') or '', False))
    paths = a.paths or ([] if a.planoly else repo_files() + ['assets/reels/s2/captions.json'])
    for p in paths:
        full = p if os.path.isabs(p) else os.path.join(R, p)
        rel = os.path.relpath(full, R)
        if full.endswith('.json'):
            for k, v in json.load(open(full)).items():
                items.append((f'{rel}[{k}]', 'file', v, rel in ARCHIVE))
        else:
            items.append((rel, 'file', open(full).read(), rel in ARCHIVE))
    fails = infos = 0
    warns = 0
    for label, plat, text, archived in items:
        probs = lint(text, plat, a.codes_list)
        for kind, msg in probs:
            tag = 'INFO' if archived else 'FAIL'
            if tag == 'FAIL' and kind in NEW_KINDS:
                new_hits.append([label, kind])
                if (label, kind) in baseline:
                    tag = 'WARN'
            fails += tag == 'FAIL'; infos += tag == 'INFO'; warns += tag == 'WARN'
            print(f'{tag} [{kind}] {label}: {msg}')
    if a.write_baseline:
        json.dump({'_about': 'Legacy hits of the Oct 30 GA1 checks on content that existed before them: WARN, not FAIL. '
                             'Cleanup is a DESK item; remove lines as they are fixed. Never add new lines.',
                   'written': NOW, 'items': sorted(set(map(tuple, new_hits)))}, open(BASELINE_PATH, 'w'), indent=1, ensure_ascii=False)
        print(f'baseline written: {len(set(map(tuple, new_hits)))} legacy hits -> {os.path.relpath(BASELINE_PATH, R)}')
    print(f'content_lint: {len(items)} captions, {fails} FAIL, {warns} WARN (legacy, baseline), {infos} INFO (archived/posted)')
    sys.exit(1 if fails and not a.warn else 0)


if __name__ == '__main__':
    main()
