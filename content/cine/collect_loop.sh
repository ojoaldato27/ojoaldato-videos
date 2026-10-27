#!/bin/bash
# Cada 2 minutos revisa y copia a la entrega los vídeos que vayan terminando, hasta que estén los 22
cd /home/claude/shorts-ingenieria/content/cine
while true; do
  python3 collect.py >> logs/collect.log 2>&1
  if grep -q ALLDONE logs/batch.log 2>/dev/null && [ -f logs/batch3.log ]; then python3 collect.py >> logs/collect.log 2>&1; echo FIN >> logs/collect.log; break; fi
  sleep 120
done
