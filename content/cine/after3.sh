#!/bin/bash
# Tras el Titanic, vuelve a renderizar los que salieron antes de la colocación automática de palabras clave
cd /home/claude/shorts-ingenieria/content/cine
while [ ! -f logs/batch2.log ]; do sleep 20; done
sleep 30
while ! grep -q ALLDONE logs/batch.log 2>/dev/null; do sleep 20; done
mv logs/batch.log logs/batch3.log
./batch_fast.sh t02_microondas t03_tactil t04_qr t05_airbag t06_nevera t07_induccion t08_gps t09_bateria
