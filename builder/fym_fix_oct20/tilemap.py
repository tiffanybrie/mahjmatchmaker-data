"""FYM set name -> canonical album/swipe-book tile photo (repo-relative). Oct 20.
Sources: assets/tiles/album/index.json (album + swipe-book tile shots), scripts/albumcard/gen_hol3.py TILE (holiday album),
scripts/swipe/canon_tiles.py (Heritage / Heritage 2.0 / Sunday)."""
A='assets/tiles/album/'; H='assets/tiles/holiday/'
TILEMAP={
 'Amara':A+'amara.jpg','Heritage 1.0':A+'heritage.jpg','Gatsby':A+'gatsby.jpg','Heritage 2.0':A+'heritage-2-0.jpg','Drake':A+'drake.jpg',
 'Lagoon':A+'lagoon.jpg','Seabreeze':A+'seabreeze.jpg','Talulah':A+'talulah.jpg','Willow':A+'willow.jpg','Cypress':A+'cypress.jpg',
 'Solara':A+'solara.jpg','Coquette':A+'coquette.jpg','Emerald':A+'emerald.jpg','Gemma':A+'gemma.jpg','Glow Wild':A+'glow-wild.jpg',
 'Jasmine':A+'jasmine.jpg','La Fete':A+'la-fete.jpg','Luminaire':A+'luminaire.jpg','Moonlight':A+'moonlight.jpg','Nantucket':A+'nantucket.jpg',
 'Osler':A+'osler.jpg','Palm Royale':A+'palm-royale.jpg','Pearlescent':A+'pearlescent.jpg','Pippa':A+'pippa.jpg','Sierra':A+'sierra.jpg',
 'Smith':A+'smith.jpg','Classic Tortoise':A+'classic-tortoise-zoom.jpg','Miss Classic Jade':A+'jade.jpg','Miss Classic Malachite':A+'malachite.jpg',
 'Birdie':A+'birdie.jpg','Dandy':A+'dandy.jpg','Glitterville':A+'glitterville.jpg','Limoncello':A+'limoncello.jpg','Lola':A+'lola.jpg',
 'Sorbet':A+'sorbet.jpg','Sunset':A+'sunset.jpg','Taylor':A+'taylor.jpg',
 # holiday album (gen_hol3.py TILE)
 'Dear Santa':H+'dear-santa.jpg',"Rackin' Rudolph":H+'rackin-rudolph.jpg','Holly Jolly (Rudolph Red)':H+'holly-jolly-red-pile.jpg',
 'Holly Jolly (Grinch Green)':H+'holly-jolly-green.jpg','Holly Jolly (Sugarplum Pink)':H+'holly-jolly-pink-pile.jpg','Nivalee (Glacier Blue)':H+'nivalee-blue.jpg',
 'Tinselle (Emerald Green)':H+'tinselle-emerald-3x3.jpg','Tinselle (Ruby Red)':H+'tinselle-ruby-3x3.jpg','Nutcracker Ballet':H+'nutcracker-ballet.jpg',
 'Après Ski Club':H+'cmc-apres-ski.jpg',
 'December 1994':'assets/tiles/sunday_mahjong_december_1994_tilebox_CARD-ONLY-edited.jpg',
 # swipe books (tile shots kept in assets/tiles/album)
 'Sunday':A+'sunday-tile-set.png','Hummingbird':A+'hummingbird.png','Nature Walk':A+'nature-walk.png','Plum Panda':A+'plum-panda.png',
 'Sunday Blues':A+'sunday-blues.png','Papaya Spritz':A+'papaya-spritz.jpg','Petalée':A+'petalee-pile.jpg',
 'Brownstone Bloom':'assets/tiles/anders_ruff_brownstone_bloom_pile_colorfixed.jpg',
}
