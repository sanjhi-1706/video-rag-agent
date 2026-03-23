import yt_dlp
import os

OUTPUT_DIR = "data/audio"

def download_audio(url: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{OUTPUT_DIR}/%(id)s.%(ext)s',
        'quiet': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path
    except Exception as e:
        print("❌ Download error:", e)
        return None