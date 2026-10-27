#!/bin/bash
# Uso: ./fixlufs.sh <mp4> <lufs_actual>  -> sube/baja la ganancia hasta ~-14 LUFS con limitador, sin tocar el vídeo
f="$1"; cur="$2"
g=$(python3 -c "print(round(-14.0-($cur),2))")
ffmpeg -hide_banner -loglevel error -y -i "$f" -c:v copy -af "volume=${g}dB,alimiter=limit=0.89:level=false" -c:a aac -b:a 192k "${f%.mp4}_ln.mp4" && mv "${f%.mp4}_ln.mp4" "$f"
