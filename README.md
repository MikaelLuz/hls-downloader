# HLS / M3U8 Downloader v2 — CLI refatorada

Este projeto reorganiza o script Python original em módulos, **sem exigir FastAPI ou extensão Chrome** nesta etapa. A interface de terminal permanece como antes. Use apenas com vídeos que você tem autorização para baixar; não contorna DRM.

## Requisitos

- Python 3.10+
- FFmpeg instalado e disponível no PATH
- Chromium do Playwright (instalado pelo comando abaixo)

## Instalação (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
ffmpeg -version
```

Se o PowerShell bloquear a ativação, use diretamente `.\.venv\Scripts\python.exe` nos comandos, sem ativar o ambiente. Para instalar FFmpeg no Windows, pode usar `winget install Gyan.FFmpeg` e abrir um novo terminal.

## Executar

No diretório `backend`:

```powershell
python cli.py
# ou
python cli.py "https://exemplo.com/pagina-com-video"
```

Se não ativou o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe cli.py
```

No Linux/macOS, ative com `source .venv/bin/activate` e use `python3 cli.py`. Instale FFmpeg pelo gerenciador de pacotes do sistema.

## Fluxo

1. Informa a URL (ou passa como argumento) e a pasta de destino.
2. Tenta extrair diretamente via yt-dlp. Se encontrar formatos, permite escolher resolução e baixa.
3. Se a extração direta falhar, abre Chromium via Playwright, com sessão persistida em `backend/.playwright_session/`.
4. Navegue até o vídeo e pressione PLAY. As URLs HLS detectadas aparecem no terminal.
5. Volte ao terminal e pressione ENTER. Escolha uma ou várias streams; no modo de captura, o script seleciona automaticamente a maior resolução identificada.
6. O arquivo é baixado usando yt-dlp e FFmpeg, com progresso no terminal.

## Módulos

| Arquivo | Responsabilidade |
| --- | --- |
| `backend/cli.py` | Fluxo principal, entradas e orquestração |
| `backend/app/utils/dependencies.py` | Verificação de dependências |
| `backend/app/services/formats.py` | Extração de formatos com yt-dlp |
| `backend/app/services/sniffer.py` | Captura HLS via Playwright e seleção de URLs |
| `backend/app/services/selection.py` | Escolha interativa de resolução |
| `backend/app/services/downloader.py` | Download e barra de progresso |

## Observações

- A sessão do Playwright não é automaticamente compartilhada com yt-dlp. Alguns vídeos autenticados podem falhar.
- URLs HLS assinadas podem expirar.
- A captura detecta URLs `.m3u8` ou padrões de manifest HLS, não conteúdo protegido por DRM.
- O parâmetro `timeout` de `sniff_m3u8_urls` permanece sem aplicação na versão original: o script aguarda ENTER.
- A pasta `.playwright_session` pode conter dados sensíveis de login: não envie ao Git.
- A API FastAPI e a extensão Chrome serão adicionadas em etapas posteriores.
