#!/bin/bash
# Renderiza en serie con fast.py los módulos dados; deja registro en logs/batch.log
cd /home/claude/shorts-ingenieria/content/cine
for m in "$@"; do
  echo "START $m $(date +%H:%M:%S)" >> logs/batch.log
  if timeout 1200 python3 fast.py "$m" >> logs/batch_$m.log 2>&1; then echo "DONE $m $(date +%H:%M:%S)" >> logs/batch.log; else echo "FAIL $m" >> logs/batch.log; fi
done
echo "ALLDONE $(date +%H:%M:%S)" >> logs/batch.log
