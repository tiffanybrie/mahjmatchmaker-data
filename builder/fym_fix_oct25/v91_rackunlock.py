"""FYM v91 (Tiffany Oct 25 20:02): after picking a rack (✓) the rack deck, Brand and colour chips locked ("Tap a ✓ rack below to unpick
it and keep swiping") — she wanted to go back and find a different tortoise. Now the deck never locks: swipe / ♥ any time, filters
always work; the ✓ picks only choose the 2 racks for the card, and a 3rd pick swaps out the older one (toast says which).
Usage: python3 v91_rackunlock.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b):
    global h
    assert h.count(a) == 1, a[:100]; h = h.replace(a, b)
rep(" if(k==='r'&&S.rpick.length)return `<div class=\"acts pk\"><p class=\"rlock\">Tap a \\u2713 rack below to unpick it and keep swiping.</p></div>`;\n", "")
rep("if(S.rpick.length>=2){toast('2 of 2 picked: tap a \\u2713 rack to unpick it first');return;}S.rpick.push(id);",
    "if(S.rpick.length>=2){const old=S.rpick.shift();toast('Swapped '+rackLabel(old)+' for '+rackLabel(id));}S.rpick.push(id);")
rep("'2 of 2 picked. Tap a \\u2713 to unpick it.'", "'2 of 2 picked. Tap another suitor to swap it in, or tap a \\u2713 to unpick it.'")
# the deck no longer turns into the picked-racks preview: it keeps swiping; your picks show with \u2713 in the rack suitors and on the card
rep("function deck(k){if(k==='r'&&S.rpick.length)return rpickView();const q=queue(k);", "function deck(k){const q=queue(k);")
rep("p:'Tap a rack suitor to see it with your mat. Tap a second one to see both. Tap a \\u2713 to unpick it.'",
    "p:'Tap a rack suitor to pick it (\\u2713). Pick up to 2. A third swaps one out, and you can keep swiping anytime.'")
open(P, 'w').write(h); print('ok')
