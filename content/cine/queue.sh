#!/bin/bash
# Renderiza en orden los módulos de queue.txt que no estén en done.txt
cd /home/claude/shorts-ingenieria/content/cine
touch queue.txt done.txt failed.txt
while true; do
  m=""
  while read -r x; do
    [ -z "$x" ] && continue
    if ! grep -qx "$x" done.txt && ! grep -qx "$x" failed.txt && ! grep -qx "$x" running.txt 2>/dev/null; then m="$x"; break; fi
  done < queue.txt
  if [ -z "$m" ]; then sleep 15; continue; fi
  echo "$m" >> running.txt
  if nice -n 5 python3 run.py "$m" render > "logs/$m.log" 2>&1; then echo "$m" >> done.txt; else echo "$m" >> failed.txt; fi
  grep -vx "$m" running.txt > running.tmp; mv running.tmp running.txt
done
