#!/usr/bin/env env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "mutagen",
# ]
# ///
"""
Playlist manager with ads insertion every X minutes via VLC HTTP interface.

Made with ❤️ by ChatGPT
"""

import argparse
import subprocess
import time
from pathlib import Path
from typing import List
import random
import requests
from requests.auth import HTTPBasicAuth
from mutagen import File as MutagenFile

AUDIO_EXTS = {".mp3", ".ogg", ".flac", ".wav", ".aac", ".m4a", ".opus"}

def is_audio_file(path: Path) -> bool:
    return path.suffix.lower() in AUDIO_EXTS

def get_audio_files(directory: Path) -> List[Path]:
    return sorted([p for p in directory.iterdir() if p.is_file() and is_audio_file(p)])

def get_average_duration(paths: List[Path]) -> float:
    durations = []
    for p in paths:
        try:
            audio = MutagenFile(p)
            if audio and audio.info:
                durations.append(audio.info.length)
        except Exception:
            continue
    return sum(durations) / len(durations) if durations else 0

def seconds_to_hms(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def create_playlist(tracks: List[Path], ad_file: Path, songs_between_ads: int) -> List[Path]:
    random.shuffle(tracks)
    playlist = []
    i = 0
    while i < len(tracks):
        chunk = tracks[i:i+songs_between_ads]
        playlist.extend(chunk)
        if ad_file and len(chunk) == songs_between_ads:
            playlist.append(ad_file)
        i += songs_between_ads
    return playlist

def check_vlc_http_available(password: str) -> bool:
    try:
        res = requests.get("http://localhost:8080/requests/status.json", auth=HTTPBasicAuth("", password))
        return res.status_code == 200
    except:
        return False

def launch_vlc():
    subprocess.Popen([
        "vlc", "--intf", "http", "--extraintf", "http",
        "--http-password=secret", "--no-video-title-show"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def wait_for_vlc(password: str, timeout: int = 10) -> bool:
    for _ in range(timeout):
        if check_vlc_http_available(password):
            return True
        time.sleep(1)
    return False

def send_playlist_to_vlc(playlist: List[Path], password: str):
    base_url = "http://localhost:8080/requests"
    auth = HTTPBasicAuth("", password)

    # Clear current playlist
    requests.get(f"{base_url}/playlist.xml?command=pl_empty", auth=auth)

    # Enqueue tracks
    for track in playlist:
        requests.get(f"{base_url}/status.xml?command=in_enqueue&input={track.resolve().as_uri()}", auth=auth)

    # Set volume to 100% (value 256)
    requests.get(f"{base_url}/status.xml?command=volume&val=256", auth=auth)

    # Enable loop (always on)
    requests.get(f"{base_url}/status.xml?command=pl_loop", auth=auth)

    # Start playback
    requests.get(f"{base_url}/status.xml?command=pl_play", auth=auth)

    print("🎵 Playlist sent and playback started on VLC at 100% volume.")

def main():
    parser = argparse.ArgumentParser(description="Playlist with ads inserted every X minutes.")
    parser.add_argument("-d", "--directory", required=True, type=Path, help="Directory containing audio files.")
    parser.add_argument("-a", "--ad-file", type=Path, help="Ad audio file to insert.")
    parser.add_argument("-p", "--password", required=True, help="Password for VLC HTTP interface.")
    parser.add_argument("--ad-every", type=int, default=15, help="Minutes between ads (integer).")
    args = parser.parse_args()

    if not args.directory.exists():
        print("❌ Directory does not exist.")
        return

    tracks = get_audio_files(args.directory)
    if not tracks:
        print("❌ No audio files found.")
        return

    ad_file = args.ad_file if args.ad_file and args.ad_file.exists() else None

    avg_duration = get_average_duration(tracks)
    total_duration = 0
    playlist = create_playlist(tracks, ad_file, max(1, round((args.ad_every * 60) / avg_duration))) if ad_file and avg_duration > 0 else tracks
    for p in playlist:
        try:
            audio = MutagenFile(p)
            if audio and audio.info:
                total_duration += audio.info.length
        except Exception:
            continue

    if avg_duration == 0:
        print("⚠️ Could not calculate average song duration. No ads will be inserted.")
        songs_between_ads = 0
    else:
        songs_between_ads = max(1, round((args.ad_every * 60) / avg_duration))
        print(f"⏱ Estimated total playlist duration: {seconds_to_hms(total_duration)} (HH:MM:SS).")
        print(f"ℹ️ Ads will be inserted approximately every {songs_between_ads} songs (avg song length {avg_duration/60:.2f} minutes).")

    if not check_vlc_http_available(args.password):
        print("⚠️ VLC is not running or HTTP interface is not available. Attempting to launch VLC...")
        launch_vlc()
        if not wait_for_vlc(args.password):
            print("❌ Could not connect to VLC. Check HTTP interface is enabled and password is correct.")
            return

    send_playlist_to_vlc(playlist, args.password)

if __name__ == "__main__":
    main()

