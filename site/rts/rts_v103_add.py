"""RTS v103: add the 'Mood board style: Rackin' Rudolph (Amazon version)' card to Ready for you now.
Usage: python3 rts_v103_add.py SRC.html OUT.html
"""
import json, sys
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf-8').read()
ID = 'l-moodboard-rudolph'
AMZ = '/_blob/1c8c8761dc066974faf5748634191ede'
PIN = '/_blob/864df9725b24461779c163b9f8fb24c0'
DESC = f"""This is our new MOOD BOARD STYLE, modeled on your Heron board, rebuilt on Rackin' Rudolph. One board becomes every format. Nothing is posted anywhere.

Amazon / Instagram (1080x1350), Amazon items only:
{AMZ}

Pinterest (1000x1500), same board:
{PIN}

The rules:
- The mat is the star: biggest, center right, at least about 75% of it visible.
- Tiles go in the corners, never in the middle: the round tile pile overlaps the mat's upper-left corner, and the flat faces shot angles off its lower-right.
- The tablecloth gets its own decent-size photo, never under the mat. The lamp stays small in a corner.
- Every product gets a short lowercase handwritten label with a little arrow pointing to it, and labels never sit on a product.
- Header is our wordmark, the title in Caprasimo, a Playfair italic tagline, and "shop the look" in small Bitter caps.
- Standard layouts for 5, 7 and 9 items. Story = the same board revealed one item per tap. Reel = items pop on one by one.
- Amazon version: Amazon items only, no URL or code, no Amazon logo, and our wordmark stays (Amazon's influencer policy expects your own logo). One thing to check: Amazon says not to alter its product images, and we cut them out. Your own photos are the safest.

The labels use a free font, since your Canva font (Adventures Unlimited) can't be used outside Canva. The white scalloped rack is left off until you pick one. Full rules are in doc 79.

On your yes, this becomes the standard for every board. Nothing gets posted to Amazon until you say so."""

new_look = ["Mood board style: Rackin' Rudolph (Amazon version)", DESC, "", ID]
assert s.count('LOOK=[[') == 1
s = s.replace('LOOK=[[', 'LOOK=[' + json.dumps(new_look) + ',[', 1)
old = '"h-rest",'
i = s.find('NOW=[')
j = s.find(old, i)
assert i >= 0 and j > i and ID not in s[i:s.find(']', i)]
s = s[:j + len(old)] + '"' + ID + '",' + s[j + len(old):]
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s))
