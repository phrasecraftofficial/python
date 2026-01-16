# Gera SRT
import importlib
import subprocess
import sys
import os
import time
import ipywidgets as widgets
from IPython.display import display, clear_output

# ===============================
# 1. Verificação e instalação
# ===============================
def install_pip_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install(package, import_name=None):
    try:
        importlib.import_module(import_name or package)
    except ImportError:
        install_pip_package(package)

def verificar_dependencias():
    check_and_install("numpy")
    check_and_install("torch")
    check_and_install("openai-whisper", "whisper")
    check_and_install("yt-dlp")
    check_and_install("ipywidgets")
    
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True)

# ===============================
# 2. Funções Auxiliares (Formatação SRT)
# ===============================
def format_timestamp(seconds: float):
    """Converte segundos para o formato SRT: HH:MM:SS,mmm"""
    tdesc = time.gmtime(seconds)
    ms = int((seconds % 1) * 1000)
    return f"{time.strftime('%H:%M:%S', tdesc)},{ms:03d}"

# ===============================
# 3. Pipeline com SRT
# ===============================
def iniciar_pipeline(b):
    with output:
        clear_output()
        video_url = url_input.value.strip()
        if not video_url:
            print("❌ Por favor, insira um link válido.")
            return

        try:
            verificar_dependencias()
            import whisper

            # Download
            print("🎧 Baixando áudio...")
            audio_file = "audio.wav"
            if os.path.exists(audio_file): os.remove(audio_file)

            command = ["yt-dlp", "-f", "bestaudio", "--extract-audio", "--audio-format", "wav", "-o", "audio.%(ext)s", video_url]
            subprocess.run(command, check=True)

            # Transcrição
            print("🧠 Carregando modelo Whisper e transcrevendo...")
            model = whisper.load_model("base")
            result = model.transcribe(audio_file)

            # Geração do SRT
            print("\n🎬 Gerando formato SRT...\n")
            srt_content = ""
            for i, segment in enumerate(result['segments'], start=1):
                start = format_timestamp(segment['start'])
                end = format_timestamp(segment['end'])
                text = segment['text'].strip()
                
                srt_block = f"{i}\n{start} --> {end}\n{text}\n\n"
                srt_content += srt_block
            
            # Exibição e Salvamento
            print("-" * 30)
            print(srt_content)
            print("-" * 30)
            
            with open("legenda.srt", "w", encoding="utf-8") as f:
                f.write(srt_content)
            
            print("✅ Arquivo 'legenda.srt' salvo com sucesso!")

        except Exception as e:
            print(f"\n❌ Erro: {e}")

# ===============================
# 4. Interface
# ===============================
url_input = widgets.Text(description="URL:", placeholder="Link do vídeo", layout=widgets.Layout(width="70%"))
start_button = widgets.Button(description="Gerar SRT", button_style="success", icon="closed-captioning")
output = widgets.Output()

start_button.on_click(iniciar_pipeline)

display(widgets.VBox([url_input, start_button], layout=widgets.Layout(gap="10px")))
display(output)
