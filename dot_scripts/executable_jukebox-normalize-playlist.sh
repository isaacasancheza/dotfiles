#!/bin/bash
# Script to normalize Opus audio files using ffmpeg-normalize 
# Usage: Run in a folder with .opus files to normalize their loudness to -14 LUFS
#
# Made with <3 by ChatGPT, 2025-07-24

OUTPUT_DIR="normalized"
mkdir -p "$OUTPUT_DIR"

# Capture Ctrl+C and exit
trap "echo 'Process cancelled by user'; exit 1" SIGINT

for file in *.opus; do
  if [[ -f "$file" ]]; then
    echo "Normalizing: $file"

    uvx ffmpeg-normalize "$file" \
      -o "$OUTPUT_DIR/$(basename "${file%.*}").opus" \
      -c:a libopus -b:a 192k \
      -t -14 \
      -ar 48000 \
      --keep-loudness-range-target \
      -f

  else
    echo "⚠️ No .opus files found."
    break
  fi
done

