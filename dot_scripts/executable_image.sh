#!/usr/bin/env sh
USER=$(op read op://Private/ffmpeg/username)
PASS=$(op read op://Private/ffmpeg/password)

ffmpeg  -i "https://$USER:$PASS@192.168.100.2/cgi-bin/snapshot.cgi?channel=1&" snapshot.jpg
