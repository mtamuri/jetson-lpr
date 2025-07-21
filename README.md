# 🚗 License Plate Recognition System (YOLOv5 + OCR)

A 20-day internship project that detects Turkish license plates in images and videos using YOLOv5 and extracts the text using OCR (EasyOCR & Tesseract). The project includes dataset preparation, model training, real-time video processing, and Jetson Nano deployment.

---

## 📌 Overview

- 🔍 Custom-trained YOLOv5 model on Turkish license plates  
- 🖼️ Roboflow-labeled dataset with training/validation split  
- 🔤 OCR (EasyOCR & Tesseract) used to read plate text  
- 🎥 Video processed frame-by-frame with timestamp logging  
- 📊 CSV output of detected plate texts with frame metadata  
- 💻 Final deployment on Jetson Nano for edge inference  

---

## 🧰 Tools & Technologies

| Tool         | Role                            |
|--------------|---------------------------------|
| Python       | Core development language       |
| YOLOv5       | Object detection framework      |
| OpenCV       | Video/image processing          |
| EasyOCR      | OCR engine #1                   |
| Tesseract    | OCR engine #2                   |
| Roboflow     | Image labeling platform         |
| Jetson Nano  | Edge deployment platform        |
| VSCode       | Code editing environment        |
| GitHub       | Version control                 |

---

## 📁 Project Structure

```plaintext
License Reading App/
├── yolov5/
│   ├── video_ocr.py                  # OCR + Detection + Logging
│   ├── runs/train/.../best.pt        # Trained model weights
│   └── ...                           # YOLOv5 original codebase
├── archive/
│   └── turkish_plate_video.py       # Creates video from images
├── plates_log.csv                   # Output: OCR results with timestamps
└── README.md                        
```

---

## ⚙️ Installation

```bash
# Clone YOLOv5 repository
git clone https://github.com/ultralytics/yolov5
cd yolov5

# Install dependencies
pip install -r requirements.txt
pip install easyocr pytesseract opencv-python pdf2image
```

---

## 🧪 Training the Model

```bash
python train.py --img 640 --batch 4 --epochs 50 --data data.yaml --weights yolov5s.pt --name plate_detector
```

- Used 70% training and 30% validation split
- Output saved in `runs/train/plate_detector/`
- Final weights: `best.pt`
- Achieved mAP@50 ≈ **0.984**

---

## 🧠 OCR Pipeline

- Implemented `ocr_pipeline.py` to test OCR on cropped plates
- Compared EasyOCR and Tesseract OCR
- **EasyOCR performed ~42% better** on Turkish plates

---

## 🎥 Running Video Inference

```bash
python video_ocr.py
```

- Requires:  
  - `best.pt` model  
  - `turkish_plate_video.avi` in correct path  
- Outputs:  
  - `output_with_text.avi` → annotated video  
  - `plates_log.csv` → plate text + timestamp  

---

## 🧾 Sample Output (CSV)

```csv
timestamp,frame,plate_text
2025-07-19T13:15:24.012345,23,34 ABC 123
2025-07-19T13:15:25.045600,24,06 DEF 456
```

---

## 🚀 Jetson Nano Deployment

- Set up Jetson without formatting (kept existing OS)
- Installed Python packages (`opencv-python`, `torch`, `easyocr`, `pytesseract`)
- Cloned the LPR repo and organized files
- Ran real-time inference using `video_ocr.py`
- Adjusted paths, fixed Python compatibility errors
- Logged OCR results on-device with low FPS but successful detection

---

## 📽️ Project Demo

- Project output annotated on real traffic footage
- Turkish license plates detected + text extracted
- CSV logs auto-generated with accurate timestamps
- Video processed both on PC and Jetson Nano

---

## 📊 Model Performance

| Metric     | Result      |
|------------|-------------|
| mAP@50     | 0.984       |
| Epochs     | 50          |
| FPS (Jetson) | ~3-5 FPS  |
| OCR Accuracy | EasyOCR > Tesseract (~42%) |

---

## ✅ Milestones

- ✅ Dependency Setup  
- ✅ Data Collection + Labeling  
- ✅ YOLOv5 Training  
- ✅ OCR Integration  
- ✅ Video Inference + Logging  
- ✅ Jetson Deployment  
- ✅ Demo Presentation + Final Report  

---

## 📎 Acknowledgements

- [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)
- [Roboflow](https://roboflow.com/)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [OpenCV](https://opencv.org/)
- Supported by **CEM Internship Program**

---

## 📌 Final Note

This project was developed during a 20-day internship focused on real-world object detection and OCR. It can be further extended with real-time camera feeds, better OCR post-processing, and deployment to edge devices like Raspberry Pi or production-grade Jetson modules.

---
