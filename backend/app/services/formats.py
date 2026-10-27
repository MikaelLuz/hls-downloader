import yt_dlp

def ytdlp_get_formats(url: str):

    import yt_dlp



    ydl_opts = {"quiet": True, "no_warnings": True}



    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)



    formats = info.get("formats", [])

    video_formats = [f for f in formats if f.get("vcodec") != "none" and f.get("height")]



    seen = {}

    for f in sorted(video_formats, key=lambda x: (x.get("height", 0), x.get("tbr", 0) or 0)):

        seen[f.get("height")] = f



    return list(seen.values()), info.get("title", "video")


