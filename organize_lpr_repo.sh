
#!/bin/bash

# === Paths ===
ROOT_DIR="$(pwd)"
Y5_DIR="$ROOT_DIR/yolov5"
APP_DIR="$ROOT_DIR/lpr_app"
DATA_DIR="$ROOT_DIR/data"

# === Create folders ===
mkdir -p "$APP_DIR"
mkdir -p "$DATA_DIR"

# === Move custom scripts ===
mv "$Y5_DIR/video_ocr.py" "$APP_DIR/" 2>/dev/null
mv "$Y5_DIR/ocr_pipeline.py" "$APP_DIR/" 2>/dev/null
mv "$Y5_DIR/split_dataset.py" "$APP_DIR/" 2>/dev/null
mv "$Y5_DIR/test.py" "$APP_DIR/" 2>/dev/null
mv "$Y5_DIR/data.yaml" "$APP_DIR/" 2>/dev/null

# === Move large data ===
mv "$ROOT_DIR/turkish_plate_video.avi" "$DATA_DIR/" 2>/dev/null
mv "$ROOT_DIR/test_plate.jpg" "$DATA_DIR/" 2>/dev/null

# === Update .gitignore ===
IGNORE_PATH="$ROOT_DIR/.gitignore"

touch "$IGNORE_PATH"

grep -qxF '*.pt' "$IGNORE_PATH" || echo '*.pt' >> "$IGNORE_PATH"
grep -qxF '*.avi' "$IGNORE_PATH" || echo '*.avi' >> "$IGNORE_PATH"
grep -qxF '*.mp4' "$IGNORE_PATH" || echo '*.mp4' >> "$IGNORE_PATH"
grep -qxF '*.jpg' "$IGNORE_PATH" || echo '*.jpg' >> "$IGNORE_PATH"
grep -qxF '*.png' "$IGNORE_PATH" || echo '*.png' >> "$IGNORE_PATH"
grep -qxF 'runs/' "$IGNORE_PATH" || echo 'runs/' >> "$IGNORE_PATH"
grep -qxF 'data/' "$IGNORE_PATH" || echo 'data/' >> "$IGNORE_PATH"

echo "✅ Files moved and .gitignore updated."
