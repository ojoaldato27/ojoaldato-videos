#!/bin/bash
# Segunda tanda de repeticiones, en paralelo a la cola principal: Kola y palomitas (pegatina encima de la pregunta)
cd /home/claude/shorts-ingenieria/content/cine
while pgrep -f "fast.py v05_apolo" >/dev/null; do sleep 15; done
for m in v07_kola t10_palomitas; do timeout 1500 python3 fast.py $m >> logs/redo2_$m.log 2>&1; echo "DONE $m $(date +%T)" >> logs/redo2.log; done
