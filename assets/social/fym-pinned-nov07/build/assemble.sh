#!/bin/bash
# Merged pinned reel: teaser (0-24.3, re-rendered, no dates) + launch redo spotlight segments.
set -e
P=/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/pin
R=/home/claude/mahjmatchmaker-data/assets/social/fym-launch/redo-nov03/launch-reel-redo.mp4
O=/home/claude/mahjmatchmaker-data/assets/social/fym-pinned-nov07
E="-c:v libx264 -pix_fmt yuv420p -crf 17 -r 30 -an"
# 'is HERE' 17.5-19.2 with the old '10.27 · mahjmatchmaker.com' line covered in navy
ffmpeg -v error -y -ss 17.5 -to 19.2 -i $R -vf "drawbox=x=0:y=1366:w=1080:h=58:color=0x052954:t=fill" $E $P/here.mp4
ffmpeg -v error -y -ss 20.68 -to 43.73 -i $R $E $P/flow.mp4
ffmpeg -v error -y -ss 47.0 -to 58.0 -i $R $E $P/shop_end.mp4
printf "file '%s'\n" $P/teaser.mp4 $P/here.mp4 $P/flow.mp4 $P/shop_end.mp4 > $P/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $P/list.txt $E -movflags +faststart $O/fym-pinned-reel.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $O/fym-pinned-reel.mp4
