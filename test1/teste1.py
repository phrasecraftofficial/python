# ===============================
# 1. Verificação e instalação
# ===============================
import importlib
import subprocess
import sys
import os

def install_pip_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install(package, import_name=None):
    try:
        importlib.import_module(import_name or package)
        print(f"✅ {package} já instalado")
    except ImportError:
        print(f"📦 Instalando {package}...")
        install_pip_package(package)

# Bibliotecas necessárias
check_and_install("yt-dlp")
check_and_install("ffmpeg-python", "ffmpeg")
check_and_install("ipywidgets")

# FFmpeg binário
print("🔍 Verificando FFmpeg...")
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ FFmpeg já disponível")
except FileNotFoundError:
    print("📦 Instalando FFmpeg...")
    subprocess.run(["apt-get", "update"], check=True)
    subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True)

print("\n🚀 Ambiente pronto!\n")


# ===============================
# 2. Interface gráfica
# ===============================
import ipywidgets as widgets
from IPython.display import display, clear_output

url_input = widgets.Text(
    description="URL:",
    placeholder="Cole aqui o link do vídeo",
    layout=widgets.Layout(width="70%")
)

start_button = widgets.Button(
    description="Iniciar",
    button_style="success",
    icon="play"
)

output = widgets.Output()


# ===============================
# 3. Função de conversão
# ===============================
def iniciar_conversao(b):
    with output:
        clear_output()
        
        video_url = url_input.value.strip()
        if not video_url:
            print("❌ Por favor, insira um link válido.")
            return
        
        print("🎧 Iniciando download e conversão...")
        
        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "wav",
            "--audio-quality", "0",
            "-o", "audio.%(ext)s",
            video_url
        ]
        
        try:
            subprocess.run(command, check=True)
            print("\n✅ Conversão concluída com sucesso!")
            print("📁 Arquivo gerado: audio.wav")
        except subprocess.CalledProcessError as e:
            print("❌ Erro durante a conversão.")
            print(e)


start_button.on_click(iniciar_conversao)


# ===============================
# 4. Exibição da UI
# ===============================
display(
    widgets.VBox(
        [url_input, start_button],
        layout=widgets.Layout(gap="10px")
    )
)
display(output)
