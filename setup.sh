#!/usr/bin/env bash
# Prepara una sesión nueva para renderizar los vídeos de «Ojo al dato».
set -e
cd "$(dirname "$0")"
python3 -c "import PIL, numpy, scipy" 2>/dev/null || pip install --break-system-packages -q pillow numpy scipy
if [ ! -f /usr/share/fonts/opentype/inter/Inter-ExtraBold.otf ]; then
  mkdir -p /usr/share/fonts/opentype/inter && cp fonts/inter/*.otf /usr/share/fonts/opentype/inter/
fi
[ -f /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf ] || (apt-get install -y -q fonts-dejavu-core >/dev/null 2>&1 || true)
command -v ffmpeg >/dev/null || (apt-get install -y -q ffmpeg >/dev/null 2>&1 || true)
mkdir -p output/cine /home/claude/subidas /home/claude/entregas
echo "listo"
