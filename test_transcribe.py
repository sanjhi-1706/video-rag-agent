from app.services.stt_service import transcribe

audio_path = input("Enter audio file path: ")

text, path = transcribe(audio_path)

print("\n📄 Transcript:\n")
print(text[:500])  # print first 500 chars

print("\nSaved at:", path)