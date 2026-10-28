#!/usr/bin/env bash
# Copia para subir desde Chrome (<10 MB): HEVC 2 pasadas, etiqueta hvc1 (la aceptan YouTube, TikTok e Instagram).
IN=$1; OUT=$2; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
VB=$(python3 -c "print(int((9.3*8*1024*1024/$D - 128000)/1000))")k
cd "$(dirname "$OUT")"
ffmpeg -y -v error -i "$IN" -c:v libx265 -preset medium -b:v $VB -x265-params pass=1:log-level=error -an -f null /dev/null && \
ffmpeg -y -v error -i "$IN" -c:v libx265 -preset medium -b:v $VB -x265-params pass=2:log-level=error -tag:v hvc1 -pix_fmt yuv420p -c:a aac -b:a 128k -ar 48000 -movflags +faststart "$OUT"
rm -f x265_2pass.log*
