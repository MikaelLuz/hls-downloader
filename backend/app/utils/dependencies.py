import subprocess
import sys

def check_dependencies():

    errors = []



    try:

        import yt_dlp  # noqa

    except ImportError:

        errors.append("yt-dlp não encontrado  →  pip install yt-dlp")



    try:

        import playwright  # noqa

    except ImportError:

        errors.append(

            "playwright não encontrado  →  pip install playwright\n"

            "                               playwright install chromium"

        )



    try:

        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)

    except (FileNotFoundError, subprocess.CalledProcessError):

        errors.append(

            "ffmpeg não encontrado → instale:\n"

            "  Windows: winget install ffmpeg\n"

            "  Linux:   sudo apt install ffmpeg\n"

            "  Mac:     brew install ffmpeg"

        )



    if errors:

        print("\n❌ Dependências faltando:\n")

        for e in errors:

            print(f"  • {e}\n")

        sys.exit(1)


