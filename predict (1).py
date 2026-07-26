import os
import numpy as np
from PIL import Image, ImageOps
import onnxruntime as ort

# File Paths
LABELS_PATH = "labels.txt"
ONNX_PATH = "model.onnx"
TEST_IMAGE_PATH = "your_test_leaf.jpg" # Yahan apni ek image ka path dalein

# 1. Load Labels
with open(LABELS_PATH, "r") as f:
    labels = [line.strip().split(" ", 1)[-1].replace("_", " ") for line in f if line.strip()]

# 2. Load Model
session = ort.InferenceSession(ONNX_PATH)
input_name = session.get_inputs()[0].name

# 3. Preprocess Image
img = Image.open(TEST_IMAGE_PATH).convert("RGB")
img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)
img_array = np.asarray(img, dtype=np.float32)

# Correct Normalization: (-1 to 1)
normalized_img = (img_array / 127.5) - 1.0
data = np.expand_dims(normalized_img, axis=0)

# 4. Run Prediction
preds = session.run(None, {input_name: data})[0][0]

# 5. Print All Classes Confidence
print("\n--- MODEL PREDICTION RESULTS ---")
for idx, prob in enumerate(preds):
    percent = prob * 100
    print(f"[{idx}] {labels[idx]}: {percent:.2f}%")

best_idx = np.argmax(preds)
print(f"\n✅ FINAL PREDICTION: {labels[best_idx]} ({preds[best_idx]*100:.2f}%)")