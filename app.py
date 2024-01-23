# Flask-Backend (app.py)
from flask import Flask, render_template, Request, Response
import cv2
import requests

app = Flask(__name__)

backend_url = "https://example.com/analyse"

def send_image_to_backend(image):
    files = {'image': ('image.jpg', image, 'image/jpeg')}
    response = requests.post(backend_url, files=files)
    return response

def generate_frames():
    # Hier Kamera-Initialisierung hinzufügen
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Hier können Sie die Bildverarbeitung anpassen, falls nötig
        # Beispiel: frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Bild an Backend senden
        response = send_image_to_backend(frame_bytes)

        if response.status_code == 200:  # Erfolgreiche Analyse
            print("Analyse erfolgreich!")
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index_streaming.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
