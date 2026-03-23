import whisper
import os

model = whisper.load_model("small")  # upgraded

TRANSCRIPT_DIR = "data/transcripts"

def transcribe(audio_path: str):
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

    try:
        print("🎤 Transcribing audio...")

        result = model.transcribe(
            audio_path,
            language="en",
            fp16=False
        )

        text = result["text"]

        filename = os.path.basename(audio_path).split('.')[0] + ".txt"
        file_path = os.path.join(TRANSCRIPT_DIR, filename)

        with open(file_path, "w") as f:
            f.write(text)

        print("✅ Transcription complete")

        return text, file_path

    except Exception as e:
        print("❌ Transcription error:", e)
        return None, None