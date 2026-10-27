#!/bin/bash
cd /home/claude/shorts-ingenieria/content/cine
while ! grep -q ALLDONE logs/batch.log; do sleep 20; done
mv logs/batch.log logs/batch1.log
./batch_fast.sh t11_f1_ventilador v01_krakatoa v02_lustig v03_monalisa v04_hachiko v05_apolo v06_tunguska v07_kola v08_emus v09_cleopatra v10_voyager
