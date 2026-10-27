#!/bin/bash
cd /home/claude/shorts-ingenieria/content/cine
while [ ! -f logs/batch1.log ]; do sleep 20; done
sleep 30
while ! grep -q ALLDONE logs/batch.log 2>/dev/null; do sleep 20; done
mv logs/batch.log logs/batch2.log
./batch_fast.sh v00_titanic
