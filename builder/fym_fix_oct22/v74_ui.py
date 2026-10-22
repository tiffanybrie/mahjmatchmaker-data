"""FYM v74 (built from v73). Usage: python3 builder/fym_fix_oct22/v74_ui.py <build_dir>
Tiffany's desktop test notes (Oct 22 4:44am, DESK "FYM Sunday build" item 6): rename the card formats.
 "Love triangle" (the spread: hero mat, tile pile, racks) -> "Mood board"
 "Mood board" (stacked close-up bands: tiles / mat / racks) -> "Close up"
Only the button labels change; the view keys ('tri', 'stack') and saved state stay the same.
The racks-step heading "Love triangle" (shown before a mat is chosen) is a step title, not a card format, and stays.
Gate [38] checks the labels."""
import sys
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read()
old = "const VIEWS=[['tri','Love triangle'],['stack','Mood board']];"
assert h.count(old) == 1, 'VIEWS not found exactly once'
h = h.replace(old, "const VIEWS=[['tri','Mood board'],['stack','Close up']];")
open(P, 'w').write(h)
print('v74 card format labels renamed')
