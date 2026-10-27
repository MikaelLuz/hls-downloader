import asyncio
import os
import sys
from urllib.parse import urlparse

async def sniff_m3u8_urls(page_url: str, timeout: int = 300) -> list[str]:

    """

    Abre o navegador visível com cookies salvos.

    Permite que o usuário navegue e clique em qualquer vídeo.

    O script só avança quando o usuário pressionar ENTER no terminal.

    """

    from playwright.async_api import async_playwright



    found_urls = []

    seen = set()



    def capture(url: str):

        url_clean = url.split("?")[0]

        if url_clean not in seen and (

            ".m3u8" in url or

            "manifest" in url.lower() and ("hls" in url.lower() or "m3u8" in url.lower())

        ):

            seen.add(url_clean)

            found_urls.append(url)

            # Mostra visualmente qual stream ele acabou de pescar

            print(f"\n  📡 [Capturado] Stream #{len(found_urls)}: {url[:70]}...")



    async with async_playwright() as p:

        session_dir = os.path.join(os.getcwd(), ".playwright_session")



        print(f"\n  🌐 Abrindo navegador em modo de seleção livre...")

        print(f"  📁 Sessão/Cookies salvos em: {session_dir}")



        context = await p.chromium.launch_persistent_context(

            user_data_dir=session_dir,

            headless=False, 

            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],

            user_agent=(

                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "

                "AppleWebKit/537.36 (KHTML, like Gecko) "

                "Chrome/124.0.0.0 Safari/537.36"

            ),

            viewport={"width": 1280, "height": 720},

        )



        page = context.pages[0] if context.pages else await context.new_page()

        page.on("request", lambda req: capture(req.url))



        print(f"  🔗 Acessando página: {page_url}")

        try:

            await page.goto(page_url, timeout=60000, wait_until="domcontentloaded")

        except Exception as e:

            print(f"  ⚠  Aviso ao carregar página: {e}")



        print(f"\n  🕹️  MODO SELEÇÃO ATIVADO:")

        print("  1. Navegue pelo portal e clique no vídeo que você deseja baixar.")

        print("  2. Dê PLAY no vídeo para o script capturar o link.")

        print("  3. Quando o vídeo correto aparecer como '[Capturado]' na tela...")

        print("  👉 Volte aqui no terminal e aperte [ENTER] para iniciar o download.")

        print("  " + "─" * 60)



        # Função interna para rodar o input sem bloquear o loop do asyncio

        def wait_for_user():

            import sys

            # Limpa o buffer de entrada para evitar Enters acidentais antigos

            if sys.platform == "win32":

                import msvcrt

                while msvcrt.kbhit():

                    msvcrt.getch()

            input("\n  ⌨️  Pressione [ENTER] para fechar o navegador e baixar a stream capturada... ")



        # Roda o input em uma thread separada para o Playwright continuar capturando a rede

        await asyncio.to_thread(wait_for_user)



        await context.close()



    # Se capturou múltiplos (ex: o automático + o que você clicou), o script original

    # já tem a função \`pick_sniffed_url\` que vai te deixar escolher qual deles baixar por número.

    return found_urls


def pick_sniffed_urls(urls: list[str]) -> list[str]:

    """Permite ao usuário escolher múltiplas streams por número ou todas de uma vez."""

    if len(urls) == 1:

        return [urls[0]]



    print("\n  🎬 Múltiplas streams detectadas:\n")

    for i, url in enumerate(urls, 1):

        domain = urlparse(url).netloc

        tail   = url.split("/")[-1][:60]

        print(f"  [{i}] {domain}/.../{tail}")



    print()

    while True:

        choice = input("  Quais streams baixar? (Ex: '1,3', 'todos', ou o número único): ").strip().lower()



        if choice == "todos":

            return urls



        if "," in choice:

            try:

                indices = [int(x.strip()) - 1 for x in choice.split(",") if x.strip()]

                if all(0 <= idx < len(urls) for idx in indices):

                    return [urls[idx] for idx in indices]

                print("  ⚠ Um ou mais números digitados são inválidos.")

            except ValueError:

                print("  ⚠ Digite apenas números separados por vírgula ou 'todos'.")

            continue



        try:

            idx = int(choice) - 1

            if 0 <= idx < len(urls):

                return [urls[idx]]

            print("  ⚠ Número inválido.")

        except ValueError:

            print("  ⚠ Digite um número válido, separados por vírgula, ou 'todos'.")


