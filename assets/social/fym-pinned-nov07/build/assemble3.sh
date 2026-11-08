#!/bin/bash
# v3: teaser 0-19.6 cut from the v2 reel (unchanged, Tiffany: "start is good") + new app half (reel3.py A|B frames).
set -e
O=/home/claude/mahjmatchmaker-data/assets/social/fym-pinned-nov07; W=/dev/shm/pin3
E="-c:v libx264 -pix_fmt yuv420p -crf 17 -r 30 -an"
[ -f $W/teaser.mp4 ] || ffmpeg -v error -y -i $O/fym-pinned-reel.mp4 -t 19.6 $E $W/teaser.mp4
for V in ${@:-A B}; do
  ffmpeg -v error -y -framerate 30 -i $W/frames$V/%04d.jpg $E $W/app$V.mp4
  printf "file '%s'\n" $W/teaser.mp4 $W/app$V.mp4 > $W/list$V.txt
  ffmpeg -v error -y -f concat -safe 0 -i $W/list$V.txt $E -movflags +faststart $O/fym-pinned-reel-v3$V.mp4
  echo $V $(ffprobe -v error -show_entries format=duration -of csv=p=0 $O/fym-pinned-reel-v3$V.mp4)
done
