import sys, subprocess, numpy as np
sys.path.insert(0, "/home/claude/shorts-ingenieria/pipeline"); sys.path.insert(0, "/home/claude/shorts-ingenieria/content/cine")
import cine, docu as DC, music3 as M
from scipy.io import wavfile
S = "/tmp"
VID = "/home/claude/shorts-ingenieria/output/cine/03_Llave_Titanic_estilo7.mp4"
OPC = [("pop", "1 · POP ENÉRGICA"), ("warm", "2 · LO-FI CÁLIDA"), ("epic", "3 · ÉPICA"), ("mystery", "4 · MISTERIO"),
       ("space", "5 · ESPACIAL"), ("viral", "6 · VIRAL CON RITMO")]
SEG = 10.0
sr = M.SR
# audio original del vídeo (voz + efectos + música suave actual) de los primeros 10 s
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VID, "-t", str(SEG), "-ac", "1", "-ar", str(sr), f"{S}/orig10.wav"], check=True)
_, base = wavfile.read(f"{S}/orig10.wav")
base = base.astype(np.float32) / 32768
voice, _ = DC.load_audio("/home/claude/shorts-ingenieria/content/cine/voz/c03_titanic.mp3", sr)
voice = voice[: int(SEG * sr)]
env = cine.smooth(np.abs(voice), int(0.05 * sr))
act = cine.smooth((env > 0.03).astype(float), int(0.35 * sr))
out = []
for k, (style, lab) in enumerate(OPC):
    rng = np.random.default_rng(5 + k)
    m = cine.music_bed(style, SEG + 1, rng)[: int(SEG * sr)]
    m = m / (np.max(np.abs(m)) + 1e-9)
    g = 1 - 0.45 * np.clip(act * 1.6, 0, 1)
    mix = base[: len(m)] * 0.9 + m * 0.32 * g
    fade = int(0.3 * sr)
    mix[:fade] *= np.linspace(0, 1, fade); mix[-fade:] *= np.linspace(1, 0, fade)
    out.append(mix)
audio = np.concatenate(out)
audio = audio / (np.max(np.abs(audio)) + 1e-9) * 0.9
wavfile.write(f"{S}/musica_opc.wav", sr, (audio * 32767).astype(np.int16))
# vídeo: los mismos 10 s repetidos 6 veces con la etiqueta de cada opción
FONT = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
parts = []
for k, (style, lab) in enumerate(OPC):
    p = f"{S}/mo_{k}.mp4"
    dt = (f"drawbox=x=0:y=1760:w=1080:h=160:color=0xE62828@1:t=fill,"
          f"drawtext=fontfile={FONT}:text='MÚSICA {lab}':fontcolor=white:fontsize=58:x=(w-text_w)/2:y=1812")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VID, "-t", str(SEG), "-an", "-vf", dt + ",scale=720:1280,fps=30",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", p], check=True)
    parts.append(p)
open(f"{S}/mo_list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{S}/mo_list.txt", "-i", f"{S}/musica_opc.wav",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "/home/claude/entrega18/Musica_de_fondo_6_opciones.mp4"], check=True)
print("ok")
