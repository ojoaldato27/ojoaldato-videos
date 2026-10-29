#!/usr/bin/env bash
# Renderiza en primer plano dos trozos de 150 fotogramas: VIDEO=urda LOOK=a ./seg2.sh <nombre> <inicio>
cd "$(dirname "$0")"; NAME=$1; A=$2; OUT=../../output/f3d/$NAME; mkdir -p $OUT
N=$(python3 -c "import sys; sys.argv=['x']; import render3d as R; T=R.timing(); print(int(T['total']*R.FPS))")
for f in $A $((A+150)); do
  [ $f -ge $N ] && break
  s=$OUT/seg_$(printf %04d $f).mp4
  [ -s $s ] || timeout 290 python3 render3d.py seg $s $f $((f+150)) 2>&1 | grep -a "seg ok"
done
