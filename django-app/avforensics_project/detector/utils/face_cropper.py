import cv2
import os

def extract_faces(video_path, output_dir, max_faces=5):
    os.makedirs(output_dir, exist_ok=True)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    cap = cv2.VideoCapture(video_path)

    count = 0
    while count < max_faces:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            face_path = os.path.join(output_dir, f'face_{count+1}.jpg')
            cv2.imwrite(face_path, face)
            count += 1
            if count >= max_faces:
                break
    cap.release()