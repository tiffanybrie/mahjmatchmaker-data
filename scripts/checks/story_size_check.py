"""Story size gate (from the 2026-11-24 stories miss: IG 9 + FB Page 9 stories were posted off-frame and had to be
taken down and rebuilt as native 9:16, Tiffany 10:45-10:48am). A Planoly story upload MUST be 1080x1920 (native 9:16);
anything else gets cropped/boxed oddly by Instagram/Facebook. This gate refuses any story-tagged image that isn't
exactly 1080x1920, BEFORE it is uploaded to Planoly as a story draft.

Run this on the folder (or files) you are about to hand to Planoly as a story group. With no args it scans every
file under assets/social/**/ whose path contains a story marker (story, stories, story-916, intro-story) -- the
repo's existing naming convention for story-frame folders -- and reports every one that is not 1080x1920.

Usage:
  python3 scripts/checks/story_size_check.py                  # scan the whole repo's story-tagged folders
  python3 scripts/checks/story_size_check.py <file1> <file2>  # check specific files before upload
  python3 scripts/checks/story_size_check.py --dir <folder>   # check every image in one folder
"""
import sys, glob, os
from PIL import Image

STORY_MARKERS = ('story', 'stories', 'story-916', 'intro-story', 'story-frames')
GOOD = (1080, 1920)
EXTS = ('.jpg', '.jpeg', '.png')

def is_story_path(p):
    parts = p.lower().replace('\\', '/').split('/')
    return any(any(m in part for m in STORY_MARKERS) for part in parts)

def collect_default():
    out = []
    for f in glob.glob('assets/social/**/*', recursive=True):
        if f.lower().endswith(EXTS) and is_story_path(f):
            out.append(f)
    return sorted(out)

def collect_dir(d):
    out = []
    for f in glob.glob(os.path.join(d, '**', '*'), recursive=True):
        if f.lower().endswith(EXTS):
            out.append(f)
    return sorted(out)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--dir' and len(args) > 1:
        files = collect_dir(args[1])
    elif args:
        files = args
    else:
        files = collect_default()

    bad = []
    checked = 0
    for f in files:
        try:
            im = Image.open(f)
        except Exception as e:
            bad.append((f, 'could not open: %s' % e))
            continue
        checked += 1
        if im.size != GOOD:
            bad.append((f, 'size %dx%d, needs %dx%d' % (im.size[0], im.size[1], GOOD[0], GOOD[1])))

    for f, why in bad:
        print('FAIL', f, '-', why)
    print('story size gate: checked %d file(s) -' % checked, 'PASS' if not bad else 'FAIL %d' % len(bad))
    sys.exit(1 if bad else 0)
