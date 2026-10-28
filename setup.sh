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
# voz Kokoro (gratis e ilimitada, elegida por Iker el 28/10): paquete + modelo desde GitHub
python3 -c "import kokoro_onnx" 2>/dev/null || pip install --break-system-packages -q kokoro-onnx soundfile
mkdir -p /home/claude/tts
[ -s /home/claude/tts/kokoro-v1.0.onnx ] || curl -sL -o /home/claude/tts/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s /home/claude/tts/voices-v1.0.bin ] || curl -sL -o /home/claude/tts/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
mkdir -p output/cine /home/claude/subidas /home/claude/entregas
echo "listo"
