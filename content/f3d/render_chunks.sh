#!/usr/bin/env bash
# Uso: VIDEO=urda LOOK=a ./render_chunks.sh <nombre>  → output/f3d/<nombre>.mp4 (render por trozos de 10 s, relanzable)
cd "$(dirname "$0")"
NAME=$1; OUT=../../output/f3d/$NAME; mkdir -p $OUT
N=$(python3 -c "import sys; sys.argv=['x']; import render3d as R; T=R.timing(); print(int(T['total']*R.FPS))")
STEP=300; SEGS=()
for ((f=0; f<N; f+=STEP)); do
  s=$OUT/seg_$(printf %04d $f).mp4; SEGS+=($s)
  [ -s $s ] || python3 render3d.py seg $s $f $((f+STEP)) 2>&1 | grep -a -v GET
done
[ -s ../../output/f3d/$NAME.mp4 ] || python3 render3d.py join ../../output/f3d/$NAME.mp4 "${SEGS[@]}"
