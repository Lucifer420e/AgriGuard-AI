import sys
import subprocess

# Auto-install opencv if missing
try:
    import cv2
    import numpy as np
except ImportError:
    print("⚙️ OpenCV library install ho rahi hai, kripya wait karein...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"])
    import cv2
    import numpy as np

import os

input_file = "agri-bg.mp4"
output_file = "agri-bg-hd.mp4"

if not os.path.exists(input_file):
    print(f"❌ Error: '{input_file}' file nahi mili!")
    sys.exit()

cap = cv2.VideoCapture(input_file)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# Sharpness matrix
sharpen_kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])

print("⚡ Video clarity enhance ho rahi hai...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    # Sharpening & contrast adjustment
    sharp_frame = cv2.filter2D(frame, -1, sharpen_kernel)
    enhanced_frame = cv2.convertScaleAbs(sharp_frame, alpha=1.12, beta=2)
    
    out.write(enhanced_frame)

cap.release()
out.release()
print(f"✅ Success! HD Video ban gayi: {output_file}")