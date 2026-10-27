import os
import re
import sys

def progress_hook(d):

    if d["status"] == "downloading":

        # Extrai a porcentagem numérica pura (padrão float do yt-dlp)

        downloaded = d.get("downloaded_bytes", 0)

        total = d.get("total_bytes") or d.get("total_bytes_estimate")



        # Tenta calcular pelos bytes se disponível, senão limpa a string do yt-dlp

        if total:

            percentage = (downloaded / total) * 100

        else:

            percent_str = d.get("_percent_str", "0.0%").replace("%", "").strip()

            try:

                percentage = float(percent_str)

            except ValueError:

                percentage = 0.0



        # Montagem da barra de progresso visual (30 caracteres de largura)

        bar_length = 30

        filled_length = int(round(bar_length * percentage / 100))

        bar = "█" * filled_length + "░" * (bar_length - filled_length)



        # Informações complementares de velocidade e tempo restante

        speed = d.get("_speed_str", "   ?B/s").strip()

        eta = d.get("_eta_str", "?").strip()



        # Fragmentos HLS/M3U8 (caso se aplique)

        fi, ft = d.get("fragment_index"), d.get("fragment_count")

        frag = f" | Frag {fi}/{ft}" if fi and ft else ""



        # Print dinâmico na mesma linha limpando caracteres antigos do terminal (\033[K)

        sys.stdout.write(f"\r  📥 |{bar}| {percentage:6.1f}% | 🚀 {speed:<10} | ⏳ ETA {eta:<6}{frag}\033[K")

        sys.stdout.flush()



    elif d["status"] == "finished":

        sys.stdout.write("\033[K") # Limpa resquícios da linha da barra

        print(f"\n\n  ✅ Download concluído! Mesclando/Processando streams com o ffmpeg...\n")


def download(url: str, format_id: str, title: str, output_dir: str, index_suffix: int = None):

    import yt_dlp



    # Se houver um sufixo (múltiplos vídeos), adiciona no nome do arquivo

    suffix_str = f"_{index_suffix}" if index_suffix is not None else ""

    safe_title = re.sub(r'[\\/*?:"<>|]', "_", title) + suffix_str

    out_path   = os.path.join(output_dir, f"{safe_title}.%(ext)s")



    ydl_opts = {

        "format": f"{format_id}+bestaudio/best",

        "outtmpl": out_path,

        "merge_output_format": "mp4",

        "concurrent_fragment_downloads": 5,

        "retries": 10,

        "fragment_retries": 10,

        "progress_hooks": [progress_hook],

        "quiet": True,

        "no_warnings": True

    }



    print(f"  ⬇  Iniciando download de: {safe_title}...\n  📁 Destino: {output_dir}\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        ydl.download([url])


