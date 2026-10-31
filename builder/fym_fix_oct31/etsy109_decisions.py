"""v109 (Oct 31 eve): by-eye decisions for the Etsy non-partner adds (BettyJuneJeannette, Piper Chase Studios) from
config/etsy-brands-oct31.json, made from contact sheets of every listing's images (scratchpad/feeds109/sheet_*.jpg).
idx -> (clean name, holiday?, image index to use, skip reason or '', hide reason or '')
Holiday = Christmas / Hanukkah / winter snowy only (CLAUDE.md). Instructional / bundle / tablecloth / duplicate listings skipped."""
BJJ = {
 0: ('Hippie Halloween', 0, 0, '', ''), 1: ('Pumpkin Spice Latte', 0, 0, '', ''), 2: ('The Wonder (Manger)', 1, 0, '', ''),
 3: ('Jingle Belle', 1, 0, '', ''), 4: ('USA', 0, 0, '', ''), 5: ('La La Flamingo Garden', 0, 0, '', ''), 6: ('Pink Fairway', 0, 0, '', ''),
 7: ('Kaleidoscope (Lilies)', 0, 0, '', ''), 8: ('On Holiday', 0, 0, '', ''), 9: ('Day Dreamer (Pink and Green)', 0, 1, '', ''),
 10: ('Noa (Hanukkah)', 1, 0, '', ''), 11: ('Fête (Peacock)', 0, 0, '', ''), 12: ('Sugarplum & Spruce', 1, 0, '', ''), 13: ('Lucy', 0, 0, '', ''),
 14: ('', 0, 0, 'instructional teacher mat', ''), 15: ('Pink and Green', 0, 0, '', ''), 16: ('Merry and Bright', 1, 0, '', ''),
 17: ('Holy Night', 1, 1, '', ''), 18: ('Gameday', 0, 0, '', ''), 19: ('Oh Little Town', 1, 0, '', ''), 20: ('Poppy (Green)', 0, 0, '', ''),
 21: ('', 0, 0, 'duplicate of La La Flamingo Garden (idx 5)', ''), 22: ('Benjamin Goes Snow Skiing', 1, 0, '', ''),
 23: ('Rebecca Jo (Hummingbird)', 0, 0, '', ''), 24: ('Anisa', 0, 0, '', ''), 25: ('', 0, 0, 'bundle (mat + bags)', ''),
 26: ('', 0, 0, 'bundle (mat + bags)', ''), 27: ('Junie', 0, 0, '', ''), 28: ('Collins', 0, 0, '', ''), 29: ('Merrye (Pink and Blue)', 0, 0, '', ''),
 30: ('Kristen (USA)', 0, 0, '', ''), 31: ('', 0, 0, 'instructional version of Lucy', ''), 32: ('Dreidel Darling', 1, 0, '', ''),
 33: ('Jingle All the Way', 1, 0, '', ''), 34: ('Away in a Manger', 1, 1, '', ''), 35: ('My Lucky', 0, 0, '', ''),
 36: ('Day Dreamer (Blue and Green)', 0, 0, '', ''), 37: ('Hey Punkin', 0, 1, '', ''), 38: ('James (Pastel Floral)', 0, 1, '', ''),
 39: ('Candy Corn Crush', 0, 0, '', ''), 40: ('Lemon Chinoiserie', 0, 0, '', ''), 41: ('', 0, 0, 'tablecloth, not a mat', ''),
 42: ('Kiki', 0, 0, '', ''), 43: ('Cherry Blossom Garden', 0, 1, '', ''), 44: ('Blythe', 0, 0, '', ''), 45: ("Gentleman's Mat", 0, 0, '', ''),
 46: ('Tennis Lessons at the Club', 0, 0, '', ''), 47: ('', 0, 0, 'bundle (mat + bags)', ''),
 48: ('', 0, 0, 'likely duplicate of Elizabeth already in FYM (same name)', ''), 49: ('Hollywood', 0, 0, '', ''),
 50: ('Ghosts N Bows', 0, 0, '', ''), 51: ('Christmas Nativity', 1, 0, '', ''), 52: ('', 0, 0, 'instructional (instructor-approved) Christmas mat', ''),
 53: ('Cozy Christmas', 1, 0, '', ''), 54: ('Lemon Print', 0, 0, '', ''), 55: ('Chinoiserie Scalloped', 0, 0, '', ''),
 56: ('Striped (Green and Pink)', 0, 0, '', ''), 57: ('Christmas Peacock Poinsettia', 1, 0, '', ''), 58: ('Pink Rose Bamboo', 0, 0, '', ''),
 59: ('Blue and Red Damask', 0, 0, '', ''), 60: ('', 0, 0, 'instructional version of a Christmas mat', ''), 61: ('Pink and Orange', 0, 0, '', ''),
 62: ('Alex (Americana)', 0, 0, '', ''), 63: ('Lauren (Pink Ladybug)', 0, 0, '', ''), 64: ('', 0, 0, 'bundle (mat + bags)', ''),
 65: ('Blue Hydrangea', 0, 0, '', ''),
}
PCS_HOL = {1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 29}  # +3 Pink Bow Lattice, +29 Pink Bow Stripe: nutcrackers (v109 QA, Oct 31)
PCS_HIDE = {26: 'hands hold the mat on every edge in the only brand image; a crop without hands loses the floral border (v109 QA)', 6: 'covered: tiles cover most of the pattern in an angled room shot (only brand image)'}
