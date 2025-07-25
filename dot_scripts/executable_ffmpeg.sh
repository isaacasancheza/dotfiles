#!/usr/bin/env sh
USER=$(op read op://Private/ffmpeg/username )
PASS=$(op read op://Private/ffmpeg/password)

URL="rtsps://$USER:$PASS@192.168.100.2:554/cam/realmonitor?channel=1&subtype=0"

ffplay -vf "scale=1280:720,setsar=1" "$URL"

