#!/bin/bash
# Script to download audio from a YouTube Music playlist using yt-dlp
# Usage: ./download-playlist.sh "URL_PLAYLIST"
#
# Made with <3 by ChatGPT, 2025-07-24

if [ -z "$1" ]; then
  echo "Error: You must provide the playlist URL."
  echo "Usage: $0 \"URL_PLAYLIST\""
  exit 1
fi

PLAYLIST_URL="$1"

uvx yt-dlp --extract-audio --audio-format best -o "%(title)s.%(ext)s" "$PLAYLIST_URL"

