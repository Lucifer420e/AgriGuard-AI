import os
import sys

# Safe import for tf_keras / keras
try:
    import tf_keras as keras
except ImportError:
    try:
        import tensorflow.keras as keras
    except ImportError:
        print("❌ Error: Keras module not found. Please run 'pip install tf_keras'")
        sys.exit(1)

import tf2onnx
import onnx

h5_file = "keras_model.h5"
onnx_file = "model.onnx"

if not os.path.exists(h5_file):
    print(f"❌ Error: '{h5_file}' file is missing in directory.")
    sys.exit(1)

print("⏳ Loading Keras H5 Model...")
model = keras.models.load_model(h5_file, compile=False)

print("⏳ Converting to ONNX format...")
# Converting keras model to onnx
onnx_model, _ = tf2onnx.convert.from_keras(model)
onnx.save(onnx_model, onnx_file)

print(f"✅ SUCCESS: Saved '{onnx_file}' successfully!")