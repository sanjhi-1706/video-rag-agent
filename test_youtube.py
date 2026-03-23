from app.services.youtube_service import download_audio

url = input("Enter YouTube URL: ")

path = download_audio(url)

print("Saved at:", path)