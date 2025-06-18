#!/usr/bin/env sh

ffmpeg -i video.mp4 -preset veryfast -g 60 -sc_threshold 0 -force_key_frames "expr:gte(t,n_forced*50)" -f segment -segment_time 50 -reset_timestamps 1 -c:v libx264 -c:a aac part_%02d.mp4

