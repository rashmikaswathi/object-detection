from flask import Flask, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
import cv2
import os
import base64
import numpy as np
save_dir = "all_detections"
os.makedirs(save_dir, exist_ok=True)
saved_classes = set()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/saved_images/<class_name>/<filename>')
def serve_saved_image(class_name, filename):
    return send_from_directory(os.path.join(save_dir, class_name), filename)

@socketio.on('video_frame')
def handle_video_frame(data_uri):
    try:
        # Decode the base64 image
        _, encoded = data_uri.split(",", 1)
        np_data = np.frombuffer(base64.b64decode(encoded), np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        # Detect using YOLOv8 (faster without stream=True)
        results = model(frame)[0]
        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Append detection
            detections.append({
                "label": label,
                "confidence": f"{conf*100:.0f}%",
                "box": [x1, y1, x2, y2]
            })

            # Save only once per class
            if label not in saved_classes:
                cropped = frame[y1:y2, x1:x2]
                if cropped.size > 0:
                    class_dir = os.path.join(save_dir, label)
                    os.makedirs(class_dir, exist_ok=True)
                    path = os.path.join(class_dir, f"{label}.jpg")
                    cv2.imwrite(path, cropped)
                    saved_classes.add(label)

        emit("detection_results", detections)
    except Exception as e:
        print("[ERROR] Detection failed:", e)

@socketio.on("get_gallery_images")
def send_gallery_images():
    gallery = []
    for class_dir in os.listdir(save_dir):
        class_path = os.path.join(save_dir, class_dir)
        if os.path.isdir(class_path):
            for file in os.listdir(class_path):
                if file.lower().endswith((".jpg", ".png")):
                    gallery.append({
                        "class": class_dir,
                        "url": f"/saved_images/{class_dir}/{file}"
                    })
    emit("gallery_content", gallery)

if __name__ == "__main__":
    print("[INFO] Server running at http://localhost:5050")
    socketio.run(app, host="0.0.0.0", port=5050)
