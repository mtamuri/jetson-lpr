import cv2
import torch
import easyocr
from datetime import datetime
import os
import csv
from tkinter import Tk, filedialog


# === CONFIG ===
video_path = filedialog.askopenfilename(title="Select License Plate Video")
if not video_path:
    raise ValueError("⚠️ No video selected.")
model_path = "models/best.pt"
output_video_path = "output_with_text.avi"

# === Init YOLO model ===
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
model.conf = 0.4  # Confidence threshold

reader = easyocr.Reader(['en', 'tr'])

# === Open video ===
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise ValueError(f"❌ Cannot open video: {video_path}")

fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# === Prepare output video writer ===
out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (W, H))

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    detections = results.xyxy[0]  # [x1, y1, x2, y2, conf, cls]

    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)

        # Skip tiny detections that are unlikely plates
        if (x2 - x1) < 50 or (y2 - y1) < 20:
            continue

        # Crop plate region
        plate_region = frame[y1:y2, x1:x2]

        # === Preprocess: grayscale, resize, denoise ===
        gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        blurred = cv2.GaussianBlur(resized, (5, 5), 0)

        # Threshold to binary for better OCR contrast
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        result = reader.readtext(thresh)
        filtered_texts = [d[1] for d in result if d[2] > 0.4]
        all_text = " ".join(filtered_texts).strip()

        if all_text.strip():
            print(f"Frame {frame_idx} ➡️ {all_text}")

            # Log plate text + timestamp to CSV
            with open("plates_log.csv", "a", newline="") as f:
                import csv
                from datetime import datetime
                writer = csv.writer(f)
                writer.writerow([datetime.now().isoformat(), frame_idx, all_text])

            # Position text above or below box
            text_y = y1 - 20 if y1 - 40 > 0 else y2 + 50

            # Draw bounding box + OCR text
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.putText(
                frame,
                all_text,
                (x1, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.6,
                (0, 0, 0),
                3,
                cv2.LINE_AA
            )

    # Show + save
    cv2.imshow("🔍 OCR Video", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_idx += 1

cap.release()
out.release()
cv2.destroyAllWindows()