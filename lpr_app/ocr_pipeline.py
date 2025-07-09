# -*- coding: utf-8 -*-
import cv2
import torch
import easyocr
import os
from tkinter import Tk, filedialog

# === CONFIG ===
Tk().withdraw()  # hide tkinter root window
image_path = filedialog.askopenfilename(title="Select License Plate Image")

if not image_path:
    raise ValueError("No image selected.")
model_path = "../models/best.pt"  # path to your trained model

# === Load image ===
img = cv2.imread(image_path)
if img is None:
    raise ValueError(f"Image not found: {image_path}")

H, W, _ = img.shape

# === Load trained YOLOv5 model ===
model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', force_reload=True)
model.conf = 0.4  # confidence threshold (optional)

# === Run YOLOv5 detection ===
results = model(img)
detections = results.xyxy[0]  # [x1, y1, x2, y2, conf, class]

if len(detections) == 0:
    print("No objects detected.")
    exit()

reader = easyocr.Reader(['en'])  # OCR reader

for *box, conf, cls in detections:
    x1, y1, x2, y2 = map(int, box)

    plate_region = img[y1:y2, x1:x2]
    result = reader.readtext(plate_region)

    # Combine all OCR text into one line
    all_text = " ".join([d[1] for d in result])
    print("➡️", all_text)

    # Position text
    text_y = y1 - 20 if y1 - 40 > 0 else y2 + 50

    # Draw OCR result
    cv2.putText(
        img,
        all_text,
        (x1, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        2.0,
        (0, 255, 255),
        10,
        cv2.LINE_AA
    )

    # Optional: Draw bounding box
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 4)

# === Resize and show ===
scale_factor = 1.5
resized = cv2.resize(img, (int(W * scale_factor), int(H * scale_factor)))

cv2.imshow("🔍 Detected Plate Text", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()