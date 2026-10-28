#!/usr/bin/env bash
# Trabajo de la noche del 28 al 29/10: F1 en HQ + 3 versiones de Urda (looks a, b, c), cada una con copia <10 MB.
cd "$(dirname "$0")"; F=../../output/f3d; S=/home/claude/subidas; mkdir -p $S
while [ ! -s $F/3D_Rebufo_F1_HQ.mp4 ]; do pgrep -f render_hq.sh >/dev/null || ./render_hq.sh; sleep 30; done
[ -s $S/3D_Rebufo_F1.mp4 ] && [ $S/3D_Rebufo_F1.mp4 -nt $F/3D_Rebufo_F1_HQ.mp4 ] || ../../tools/hevc10.sh $F/3D_Rebufo_F1_HQ.mp4 $S/3D_Rebufo_F1.mp4
echo "F1 listo $(date)"
for L in a b c; do
  VIDEO=urda LOOK=$L ./render_chunks.sh Urda_$L
  [ -s $S/Urda_$L.mp4 ] || ../../tools/hevc10.sh $F/Urda_$L.mp4 $S/Urda_$L.mp4
  echo "Urda $L listo $(date)"
done
echo "TODO LISTO $(date)"
