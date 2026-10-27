

def pick_format(formats: list[dict]) -> str:

    print("\n  📺 Resoluções disponíveis:\n")

    print(f"  {'#':<4} {'Resolução':<12} {'FPS':<6} {'Bitrate':<12} {'Codec'}")

    print("  " + "─" * 50)



    sorted_fmts = sorted(formats, key=lambda x: x.get("height", 0), reverse=True)



    for i, f in enumerate(sorted_fmts, 1):

        height  = f.get("height", "?")

        fps     = f.get("fps", "?")

        tbr     = f.get("tbr")

        tbr_str = f"{tbr:.0f}k" if tbr else "?"

        vcodec  = f.get("vcodec", "?").split(".")[0]

        fmt_id  = f.get("format_id", "?")

        print(f"  {i:<4} {str(height)+'p':<12} {str(fps):<6} {tbr_str:<12} {vcodec}  [{fmt_id}]")



    print()

    while True:

        try:

            choice = input("  Resolução (número, ou ENTER para melhor): ").strip()

            if choice == "":

                return sorted_fmts[0]["format_id"]

            idx = int(choice) - 1

            if 0 <= idx < len(sorted_fmts):

                return sorted_fmts[idx]["format_id"]

            print("  ⚠ Número inválido.")

        except ValueError:

            print("  ⚠ Digite apenas o número.")


