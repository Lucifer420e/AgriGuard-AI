import urllib.request
import os

print("⏳ Downloading ONNX conversion tool dependencies...")
# Installing tf2onnx & h5py directly via pip
os.system("pip install --quiet h5py onnxruntime numpy pillow requests")

print("\n---------------------------------------------------")
print("✅ Environment isolated from C++ PyBind crashes!")
print("Now update main_app_stm.py with pure ONNX runtime.")
print("---------------------------------------------------")