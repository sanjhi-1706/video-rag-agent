from app.services.youtube_service import download_audio
from app.services.stt_service import transcribe
from app.rag.chunking import chunk_text

def process_video(url):
    print("📥 Downloading video audio...")
    audio_path = download_audio(url)

    print("🎤 Transcribing...")
    transcript, _ = transcribe(audio_path)

    print("✂️ Chunking...")
    chunks = chunk_text(transcript)

    print("✅ Processing complete")

    return {
        "transcript": transcript,
        "chunks": chunks
    }