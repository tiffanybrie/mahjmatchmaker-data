#!/bin/bash
# Sadie Jane OMM reel: 10 fast table flashes (hook, 1.0s) + CTA 2.0s + 'your turn' 3.5s + animated end card (from v1 reel @12.2s).
set -e; R=assets/social/sadie-jane-launch/reel; T=$(mktemp -d)
i=0; for f in 00 01 02 03 04 05 06 07 08 09 10 11-yourturn; do d=1.0; [ $f = 10 ] && d=2.0; [ $f = 11-yourturn ] && d=3.5
ffmpeg -v error -y -loop 1 -t $d -i $R/frames/$f.png -vf "fps=30,format=yuv420p" -c:v libx264 -preset veryfast -crf 18 $T/$(printf %02d $i).mp4; i=$((i+1)); done
cp $R/endcard.mp4 $T/99.mp4
ls $T/*.mp4 | sed "s/^/file '/;s/$/'/" > $T/l.txt; ffmpeg -v error -y -f concat -safe 0 -i $T/l.txt -c copy $R/sadie-jane-fym-reel.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $R/sadie-jane-fym-reel.mp4
