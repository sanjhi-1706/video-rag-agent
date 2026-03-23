import cv2
import os

def extract_frames(video_path, interval=30):
    os.makedirs("data/frames", exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frames = []

    count = 0
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            path = f"data/frames/frame_{frame_id}.jpg"
            cv2.imwrite(path, frame)
            frames.append(path)
            frame_id += 1

        count += 1

    cap.release()
    return frames