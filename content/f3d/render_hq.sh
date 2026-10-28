#!/usr/bin/env bash
# Render por trozos de 10 s (se puede relanzar: salta los trozos ya hechos) y unión final con audio.
cd "$(dirname "$0")"
OUT=../../output/f3d/hq; mkdir -p $OUT
N=1849; STEP=300; SEGS=()
for ((f=0; f<N; f+=STEP)); do
  s=$OUT/seg_$(printf %04d $f).mp4; SEGS+=($s)
  [ -s $s ] || python3 render3d.py seg $s $f $((f+STEP)) 2>&1 | grep -a -v GET
done
python3 render3d.py join ../../output/f3d/3D_Rebufo_F1_HQ.mp4 "${SEGS[@]}"
