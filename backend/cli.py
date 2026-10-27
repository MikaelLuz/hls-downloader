"""CLI original do HLS Downloader v2, reorganizado em módulos."""
import asyncio
import os
import sys
from pathlib import Path

from app.utils.dependencies import check_dependencies
from app.services.formats import ytdlp_get_formats
from app.services.sniffer import sniff_m3u8_urls, pick_sniffed_urls
from app.services.selection import pick_format
from app.services.downloader import download

def main():

    print("""

╔══════════════════════════════════════════════╗

║         HLS / M3U8 Downloader v2             ║

╚══════════════════════════════════════════════╝

""")



    check_dependencies()



    # URL

    url = (sys.argv[1] if len(sys.argv) > 1 else

           input("  🔗 URL da página ou do .m3u8 direto: ").strip())



    if not url:

        print("❌ URL vazia.")

        sys.exit(1)



    # Pasta de saída

    default_dir = str(Path.home() / "Downloads" / "videos")

    output_dir  = input(f"\n  📁 Pasta de destino [{default_dir}]: ").strip() or default_dir

    os.makedirs(output_dir, exist_ok=True)



    # ── Tenta yt-dlp direto primeiro ──

    print("\n  🔍 Tentando detectar vídeo diretamente (yt-dlp)...")

    try:

        formats, title = ytdlp_get_formats(url)

        if formats:

            print(f"  ✅ Vídeo encontrado: {title}")

            format_id = pick_format(formats)

            download(url, format_id, title, output_dir)

            print(f"  📂 Salvo em: {output_dir}\n")

            return

        else:

            print("  ⚠  yt-dlp não encontrou formatos de vídeo.")

    except Exception as e:

        print(f"  ⚠  yt-dlp não conseguiu extrair: {e}")



# ── Fallback: Playwright sniff ──

    print("\n  🕵️  Ativando modo Playwright (browser headless + interceptação de rede)...")



    m3u8_urls = asyncio.run(sniff_m3u8_urls(url, timeout=300))



    if not m3u8_urls:

        print("\n❌ Nenhuma URL .m3u8 detectada.")

        sys.exit(1)



    # Nova função que retorna uma LISTA de alvos

    target_urls = pick_sniffed_urls(m3u8_urls)



    title_input = input("\n  ✏️  Nome base do arquivo (sem extensão): ").strip() or "video"



    # Loop para baixar cada um dos selecionados

    for idx, target_url in enumerate(target_urls, 1):

        print(f"\n  ========================================================")

        print(f"  📦 Processando item {idx} de {len(target_urls)}")

        print(f"  ========================================================")



        print("  🔍 Buscando resoluções na stream...")

        try:

            formats, _ = ytdlp_get_formats(target_url)

        except Exception:

            formats = []



        if formats:

            # Como são muitos vídeos, para não travar perguntando a resolução de cada um,

            # ele pega a melhor de forma inteligente. Se quiser escolher um por um, 

            # pode trocar a linha abaixo por: format_id = pick_format(formats)

            format_id = sorted(formats, key=lambda x: x.get("height", 0), reverse=True)[0]["format_id"]

            print(f"  ⚡ Melhor resolução selecionada automaticamente.")

        else:

            print("  ℹ  Baixando na melhor qualidade disponível.")

            format_id = "bestvideo+bestaudio/best"



        try:

            # Passa o idx como sufixo para os arquivos ficarem organizados (Ex: aula_1.mp4, aula_2.mp4)

            suffix = idx if len(target_urls) > 1 else None

            download(target_url, format_id, title_input, output_dir, index_suffix=suffix)

            print(f"  📂 Salvo com sucesso em: {output_dir}")

        except KeyboardInterrupt:

            print("\n  ⛔ Download atual cancelado pelo usuário.")

            break

        except Exception as e:

            print(f"\n❌ Erro ao baixar esta stream: {e}")



    print("\n  🎉 Todos os downloads solicitados foram processados!\n")



if __name__ == "__main__":
    main()
