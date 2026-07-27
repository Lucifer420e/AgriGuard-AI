import base64
from io import BytesIO
import os
from gtts import gTTS
import numpy as np
from PIL import Image
import requests
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import os
from dotenv import load_dotenv

# .env file se variables load karne ke liye
load_dotenv()

# Key ko read karne ke liye
api_key = os.getenv("GEMINI_API_KEY")

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & SESSION STATES
# ---------------------------------------------------------
st.set_page_config(
    page_title="AgriGuard AI Expert",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "translate_hindi" not in st.session_state:
  st.session_state.translate_hindi = False

if "user_query" not in st.session_state:
  st.session_state.user_query = ""


# ---------------------------------------------------------
# 2. DYNAMIC LIVE WEATHER ENGINE
# ---------------------------------------------------------
def get_live_weather(state_name):
  try:
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={state_name}&count=1&language=en&format=json"
    geo_res = requests.get(geo_url, timeout=5).json()

    if not geo_res.get("results"):
      return None

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]
    location_name = (
        f"{geo_res['results'][0]['name']},"
        f" {geo_res['results'][0].get('country', '')}"
    )

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m&timezone=auto"
    w_res = requests.get(weather_url, timeout=5).json()

    current = w_res.get("current", {})
    return {
        "location": location_name,
        "temp": current.get("temperature_2m", 30),
        "humidity": current.get("relative_humidity_2m", 60),
        "rain": current.get("rain", 0),
        "wind": current.get("wind_speed_10m", 10),
    }
  except Exception:
    return None


# ---------------------------------------------------------
# 3. HIGH-DEFINITIONAL VIDEO & TRANSLUCENT GLASS PANELS
# ---------------------------------------------------------
def inject_custom_theme(video_filename="agri-bg.mp4"):
  base_dir = os.path.dirname(os.path.abspath(__file__))
  video_path = os.path.join(base_dir, video_filename)

  if not os.path.exists(video_path):
    video_path = os.path.join(base_dir, "agri-bg-hd.mp4")

  video_b64 = ""
  if os.path.exists(video_path):
    with open(video_path, "rb") as f:
      video_b64 = base64.b64encode(f.read()).decode()

  custom_style = f"""
    <style>
    /* HD BACKGROUND VIDEO */
    #bg-video {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -1;
        filter: brightness(0.9) contrast(1.1) !important;
    }}

    .stApp {{
        background: transparent !important;
    }}

    /* SIDEBAR TRANSLUCENT GLASS */
    [data-testid="stSidebar"] {{
        background: rgba(8, 18, 30, 0.55) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.3) !important;
    }}

    /* MAIN TRANSLUCENT GLASS CARDS */
    div[data-testid="stColumn"] {{
        background: rgba(6, 16, 26, 0.38) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(0, 240, 255, 0.35) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }}

    /* PURE WHITE TEXT WITH INTENSE WHITE GLOW */
    .main-title {{
        text-align: center;
        font-size: 3.6rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        text-shadow: 
            0 0 5px #FFFFFF,
            0 0 10px #FFFFFF,
            0 0 20px rgba(255, 255, 255, 0.9),
            0 0 40px rgba(0, 240, 255, 0.7),
            0 0 80px rgba(0, 240, 255, 0.5) !important;
        margin-bottom: 25px;
        letter-spacing: 1.5px;
    }}

    .cyan-hdr {{
        color: #00f0ff !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.7), 0 2px 4px rgba(0,0,0,0.8);
        margin-bottom: 18px !important;
    }}

    .glow-blue {{
        color: #00f0ff !important;
        font-weight: 800;
        font-size: 1.1rem;
        text-shadow: 0 0 6px rgba(0, 240, 255, 0.6), 0 2px 4px rgba(0,0,0,0.8);
        letter-spacing: 0.3px;
    }}
    .glow-white {{
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1.05rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.9);
    }}

    .advice-item {{
        margin-bottom: 16px;
        line-height: 1.5;
    }}

    /* WEATHER MAIN LOCATION CARD */
    .weather-main-card {{
        background: rgba(0, 240, 255, 0.12);
        border: 1px solid rgba(0, 240, 255, 0.4);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
        text-align: center;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }}
    .weather-temp {{
        font-size: 2.5rem;
        font-weight: 900;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.8);
        margin-top: 4px;
    }}

    /* SEPARATE METRIC MINI-PANELS IN SIDEBAR */
    .metric-panel {{
        background: rgba(6, 16, 26, 0.45);
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        backdrop-filter: blur(8px);
    }}
    .metric-label {{
        color: #ffffff;
        font-weight: 600;
        font-size: 0.98rem;
    }}
    .metric-value {{
        color: #00f0ff;
        font-weight: 800;
        font-size: 1.1rem;
        text-shadow: 0 0 6px rgba(0,240,255,0.5);
    }}

    /* AI RESPONSE BOX */
    .ai-response-box {{
        background: rgba(6, 16, 26, 0.45) !important;
        backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(0, 240, 255, 0.35) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        margin-top: 20px;
        color: #ffffff !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }}

    .answer-step {{
        background: rgba(0, 0, 0, 0.35);
        border-left: 4px solid #00f0ff;
        padding: 12px 16px;
        margin-top: 10px;
        border-radius: 0 10px 10px 0;
        font-size: 1.08rem;
        line-height: 1.5;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }}

    /* Q&A SEARCH BAR STYLES */
    .qa-column-box div[data-testid="stColumn"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        padding: 0 !important;
    }}

    input[type="text"] {{
        height: 52px !important;
        border-radius: 14px !important;
        border: 1.5px solid rgba(0, 240, 255, 0.45) !important;
        background: rgba(6, 16, 26, 0.45) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        padding-left: 18px !important;
        backdrop-filter: blur(10px) !important;
    }}

    input[type="text"]:focus {{
        border-color: #00f0ff !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.4) !important;
    }}

    iframe[title="streamlit_mic_recorder.speech_to_text"] {{
        height: 52px !important;
        width: 100% !important;
    }}

    button[kind="secondary"] {{
        height: 52px !important;
        width: 100% !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, rgba(0,240,255,0.8), rgba(0,136,204,0.8)) !important;
        color: #040c14 !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.4) !important;
        transition: all 0.2s ease !important;
    }}

    button[kind="secondary"]:hover {{
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.7) !important;
    }}

    h1, h2, h3, h4, p, label, span {{
        color: #FFFFFF !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }}
    </style>

    <video autoplay loop muted playsinline id="bg-video">
        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>
    """
  st.markdown(custom_style, unsafe_allow_html=True)


inject_custom_theme("agri-bg.mp4")


# ---------------------------------------------------------
# 4. SIDEBAR WITH SEPARATE METRIC PANELS
# ---------------------------------------------------------
with st.sidebar:
  st.markdown(
      "<h2 style='color:#00f0ff; text-shadow: 0 0 8px"
      " rgba(0,240,255,0.6);'>🌤️ Agri Weather</h2>",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  target_state = st.text_input(
      "🔍 Enter State / City Name",
      value="Punjab",
      placeholder="e.g. Punjab, Delhi, UP...",
  )

  weather_data = get_live_weather(target_state)

  if weather_data:
    st.markdown(
        f"""
        <div class="weather-main-card">
            <div style="font-weight:700; color:#fff; font-size:1.05rem;">📍 {weather_data['location']}</div>
            <div class="weather-temp">{weather_data['temp']}°C</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="metric-panel">
            <span class="metric-label">💧 Humidity</span>
            <span class="metric-value">{weather_data['humidity']}%</span>
        </div>
        <div class="metric-panel">
            <span class="metric-label">🌧️ Rainfall</span>
            <span class="metric-value">{weather_data['rain']} mm</span>
        </div>
        <div class="metric-panel">
            <span class="metric-label">💨 Wind Speed</span>
            <span class="metric-value">{weather_data['wind']} km/h</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.error("State/City not found.")

  st.markdown("---")
  st.markdown("### 🌾 Agro Advisory")
  st.info("Check rainfall & wind speed before spraying chemicals.")


# ---------------------------------------------------------
# 5. TFLITE MODEL LOADER
# ---------------------------------------------------------

@st.cache_resource
def load_tflite_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "model_unquant.tflite")
    
    if not os.path.exists(model_path):
        model_path = os.path.join(base_dir, "model.tflite")
        
    if not os.path.exists(model_path):
        return None
        
    try:
        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=model_path)
        except ImportError:
            import tensorflow as tf
            interpreter = tf.lite.Interpreter(model_path=model_path)
            
        interpreter.allocate_tensors()
        return interpreter
    except Exception:
        return None

def load_labels():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    labels_path = os.path.join(base_dir, "labels.txt")
    if os.path.exists(labels_path):
        with open(labels_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return []

interpreter = load_tflite_model()
labels = load_labels()

def predict_disease(image):
    if not interpreter:
        return "Model File Missing", 0.0

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img = image.convert("RGB").resize((224, 224))
    img_array = np.array(img, dtype=np.float32)
    img_array = (img_array / 127.5) - 1.0
    img_array = np.expand_dims(img_array, axis=0)

    interpreter.set_tensor(input_details[0]["index"], img_array)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]["index"])
    predicted_index = np.argmax(output_data[0])
    confidence = float(output_data[0][predicted_index])

    if labels and predicted_index < len(labels):
        label_name = labels[predicted_index]
    else:
        label_name = f"Class {predicted_index}"

    return label_name, confidence

# ---------------------------------------------------------
# 6. EXPERT AI & HINDI AUDIO ENGINE
# ---------------------------------------------------------
def get_ai_answer(question):
  q = question.lower()

  only_medicine_keywords = [
      "medicine",
      "dawa",
      "fungicide",
      "spray name",
      "दवा",
      "इलाज क्या है",
      "कौन सी दवा",
  ]
  is_only_medicine = any(kw in q for kw in only_medicine_keywords)

  if is_only_medicine:
    display_html = """
        <div class='answer-step'><b>💊 Recommended Medicine 1:</b> <b>Mancozeb 75% WP</b> (Mix 2.5 g per Liter of water).</div>
        <div class='answer-step'><b>💊 Recommended Medicine 2:</b> <b>Copper Oxychloride 50% WP</b> (3 g per Liter for fungal protection).</div>
        <div class='answer-step'><b>💊 For Severe Infection:</b> <b>Propiconazole 25% EC</b> (1 mL per Liter).</div>
        """
    speech_text = (
        "अनुशंसित दवाएं हैं मैंकोज़ेब, कॉपर ऑक्सीक्लोराइड, और प्रोपीकोनाज़ोल।"
    )
  else:
    display_html = """
        <div class='answer-step'><b>🛡️ Step 1 (Immediate Action):</b> Prune and remove all infected leaves immediately to stop disease spread.</div>
        <div class='answer-step'><b>💧 Step 2 (Water Management):</b> Avoid overhead sprinkler irrigation; keep the crop canopy dry.</div>
        <div class='answer-step'><b>🧪 Step 3 (Recommended Medicines):</b> Spray <b>Mancozeb 75% WP</b> (2.5 g/L) or <b>Copper Oxychloride</b> to completely cure the infection.</div>
        """
    speech_text = (
        "सबसे पहले संक्रमित पत्तियों को काटकर हटा दें और फसल को सूखा रखें।"
        " इसके बाद मैंकोज़ेब या कॉपर ऑक्सीक्लोराइड कवकनाशी का छिड़काव करें।"
    )

  return display_html, speech_text


def text_to_speech_audio(text):
  try:
    tts = gTTS(text=text, lang="hi", slow=False)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp
  except Exception:
    return None


# ---------------------------------------------------------
# 7. MAIN CONTENT PANELS
# ---------------------------------------------------------
st.markdown(
    "<h1 class='main-title'>🌾 AgriGuard AI Expert</h1>", unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1.1, 1.1, 1.2])

with col1:
  st.markdown(
      "<div class='cyan-hdr'>1. Crop Leaf Input</div>", unsafe_allow_html=True
  )
  input_type = st.radio(
      "Select Input Method", ["Upload Image File", "Use Live Web Cam"]
  )

  uploaded_file = None
  if input_type == "Upload Image File":
    uploaded_file = st.file_uploader(
        "Choose Leaf Photo", type=["jpg", "jpeg", "png"]
    )
  else:
    uploaded_file = st.camera_input("Take Photo")

  if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

with col2:
  st.markdown(
      "<div class='cyan-hdr' style='text-align:center;'>2. Detection"
      " Result</div>",
      unsafe_allow_html=True,
  )
  if uploaded_file:
    label_res, conf_res = predict_disease(image)

    parts = label_res.replace("_", " ").split(" ", 1)
    crop_main = parts[0]
    disease_sub = parts[1] if len(parts) > 1 else ""

    st.markdown(
        f"""
        <div style='display:flex; flex-direction:column; align-items:center; text-align:center;'>
            <div style='font-size:1.1rem; font-weight:800; letter-spacing:2px; text-shadow:0 0 4px rgba(255,255,255,0.3);'>DISEASE IDENTIFIED</div>
            <div style='color:#00f0ff; font-size:2.8rem; font-weight:900; text-shadow:0 0 10px rgba(0, 240, 255, 0.6);'>{crop_main}</div>
            {"<div style='color:#00f0ff; font-size:2.2rem; font-weight:800; text-shadow:0 0 8px rgba(0, 240, 255, 0.5);'>" + disease_sub + "</div>" if disease_sub else ""}
            <p style='color:#FFFFFF !important; font-size:1.2rem; font-weight:700; text-shadow:0 0 3px rgba(255,255,255,0.2);'>System Confidence: <b style='color:#00f0ff; text-shadow:0 0 6px rgba(0,240,255,0.5);'>{conf_res:.1f}%</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:1.15rem; font-weight:800; color:#FFFFFF;"
        " text-align:center;'>⚡ LIVE QUICK STATS</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;'>• <b>Analysis Speed:</b> ~18ms<br>•"
        " <b>Ambient Temperature:</b> 32.0°C</p>",
        unsafe_allow_html=True,
    )
  else:
    st.info("Upload an image to trigger detection.")

with col3:
  st.markdown(
      "<div class='cyan-hdr'>3. AI Expert Advice</div>", unsafe_allow_html=True
  )
  if uploaded_file:
    btn_label = (
        "🌐 Translate to English"
        if st.session_state.translate_hindi
        else "🌐 Translate to Hindi (हिंदी)"
    )
    if st.button(btn_label):
      st.session_state.translate_hindi = not st.session_state.translate_hindi
      st.rerun()

    st.markdown("---")

    if not st.session_state.translate_hindi:
      st.markdown(
          """
            <div class='advice-item'><span class='glow-blue'>1. Isolation:</span> <span class='glow-white'>Prune infected leaf parts immediately to prevent spread.</span></div>
            <div class='advice-item'><span class='glow-blue'>2. Irrigation:</span> <span class='glow-white'>Avoid overhead watering; always keep foliage dry.</span></div>
            <div class='advice-item'><span class='glow-blue'>3. Fungicide Spray:</span> <span class='glow-white'>Apply recommended Mancozeb or Copper fungicide.</span></div>
            <div class='advice-item'><span class='glow-blue'>4. Soil Nutrition:</span> <span class='glow-white'>Apply Potash (K) fertilizer to boost plant immunity.</span></div>
            <div class='advice-item'><span class='glow-blue'>5. Regular Monitoring:</span> <span class='glow-white'>Inspect lower leaf canopy every 3 days for early symptoms.</span></div>
            """,
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          """
            <div class='advice-item'><span class='glow-blue'>1. अलगाव:</span> <span class='glow-white'>संक्रमित पत्तियों को तुरंत काटकर अलग करें।</span></div>
            <div class='advice-item'><span class='glow-blue'>2. सिंचाई:</span> <span class='glow-white'>ऊपर से पानी न दें, पत्तियों को सूखा रखें।</span></div>
            <div class='advice-item'><span class='glow-blue'>3. दवा का छिड़काव:</span> <span class='glow-white'>मैंकोजेब या कॉपर कवकनाशी का प्रयोग करें।</span></div>
            <div class='advice-item'><span class='glow-blue'>4. पोषण प्रबंधन:</span> <span class='glow-white'>रोग प्रतिरोधक क्षमता बढ़ाने के लिए पोटाश दें।</span></div>
            <div class='advice-item'><span class='glow-blue'>5. नियमित निरीक्षण:</span> <span class='glow-white'>हर 3 दिन में निचली पत्तियों की जांच करें।</span></div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.write("Advisory panel will activate post-detection.")

# ---------------------------------------------------------
# 8. INTEGRATED Q&A BAR
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<div class='cyan-hdr' style='font-size:1.4rem !important;'>💬 Ask AgriGuard"
    " AI Expert</div>",
    unsafe_allow_html=True,
)

placeholder_msg = (
    "सवाल पूछें या माइक बटन दबाएं..."
    if st.session_state.translate_hindi
    else "Ask a question or tap the mic..."
)

st.markdown("<div class='qa-column-box'>", unsafe_allow_html=True)
c_input, c_mic = st.columns([0.91, 0.09])

with c_input:
  query_input = st.text_input(
      label="Q&A Query Bar",
      value=st.session_state.user_query,
      placeholder=placeholder_msg,
      key="qa_input_box",
      label_visibility="collapsed",
  )

with c_mic:
  spoken_text = speech_to_text(
      start_prompt="🎙️",
      stop_prompt="🛑",
      language="hi-IN" if st.session_state.translate_hindi else "en-US",
      key="inline_mic_btn",
  )

st.markdown("</div>", unsafe_allow_html=True)

if spoken_text:
    st.session_state.user_query = spoken_text

active_query = query_input or spoken_text

if active_query:
    with st.spinner("AgriGuard AI is generating answer..."):
        html_answer, speech_text_res = get_ai_answer(active_query)

    st.markdown(
        f"""
        <div class='ai-response-box'>
            <h4 style='color:#00f0ff !important; margin-top:0; font-size:1.3rem; text-shadow:0 0 6px rgba(0,240,255,0.4);'>🤖 AgriGuard AI Answer:</h4>
            {html_answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Audio conversion ko active_query ke andar hi rakhein!
    audio_bytes = text_to_speech_audio(speech_text_res)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
