## Custom CSS is LESS (Oct 20)
- Site Custom CSS is compiled as LESS: `grid-area: 16/15/18/26` gets DIVIDED and silently dropped. Use grid-row-start/-end and grid-column-start/-end there.
- Oct 20 fix: homepage desktop had ~2,800px of blank space at the bottom (How It Works step 3 section, a text block parked at fluid-grid row 121). Custom CSS now caps that section at 18 rows and moves the "Love sharing your setups?" text under the FB button (desktop only). Homepage 18,435px -> 14,433px.
