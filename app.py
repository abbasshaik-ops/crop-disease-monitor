# app.py
import os
import json
import base64
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from utils.remedies import get_remedy

# Page Configuration
st.set_page_config(
    page_title="Crop Health & Disease Monitoring",
    page_icon="🌿",
    layout="centered"
)

def get_base64_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def resolve_asset_image(base_path_no_ext: str):
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        candidate = base_path_no_ext + ext
        if os.path.exists(candidate):
            return candidate
    return None

# Custom Leaf Image Background + Transparent Text with Translucent Border Lines
def apply_leaf_theme(bg_base_path: str = "assets/leaf_bg"):
    bg_image_path = resolve_asset_image(bg_base_path)
    if bg_image_path and os.path.exists(bg_image_path):
        ext = os.path.splitext(bg_image_path)[1].lower().replace(".", "")
        if ext == "jpg":
            ext = "jpeg"
        b64_str = get_base64_image(bg_image_path)
        bg_css = f"""
            background-image: 
                linear-gradient(180deg, rgba(6, 20, 12, 0.60) 0%, rgba(8, 26, 15, 0.54) 50%, rgba(6, 20, 12, 0.68) 100%),
                url("data:image/{ext};base64,{b64_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        """
    else:
        bg_css = """
            background: linear-gradient(145deg, #0d2818 0%, #164229 48%, #1e5635 100%);
        """

    st.markdown(
        f"""
        <style>
        /* Main App Background */
        .stApp {{
            {bg_css}
            color: #f0fdf4;
        }}

        /* Fully Transparent Header Bar */
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* Transparent Main Container (No Solid Box, Only Subtle Translucent Hairline Border) */
        .block-container {{
            background: transparent !important;
            border: 1px solid rgba(134, 239, 172, 0.28);
            border-radius: 18px;
            padding: 2rem 2rem 2.5rem 2rem !important;
            margin-top: 1.5rem;
            margin-bottom: 2rem;
        }}

        /* Crisp Text Directly Over Leaf Background */
        h1 {{
            color: #ffffff !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 14px rgba(0, 0, 0, 0.78);
            padding-bottom: 0.6rem;
            border-bottom: 1px solid rgba(134, 239, 172, 0.32);
        }}
        h2, h3 {{
            color: #bbf7d0 !important;
            font-weight: 700 !important;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.75);
            padding-bottom: 0.35rem;
            border-bottom: 1px solid rgba(134, 239, 172, 0.25);
        }}
        p, label, li, .stMarkdown, .stCaption {{
            color: #f0fdf4 !important;
            text-shadow: 0 1px 8px rgba(0, 0, 0, 0.85);
        }}

        /* Horizontal Divider Line */
        hr {{
            border-color: rgba(134, 239, 172, 0.3) !important;
        }}

        /* Transparent Tabs with Translucent Line Borders */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            background: transparent !important;
            padding: 6px;
            border-radius: 12px;
            border: 1px solid rgba(134, 239, 172, 0.3);
        }}
        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border-radius: 8px;
            color: #dcfce7 !important;
            font-weight: 600;
            padding: 8px 18px;
            text-shadow: 0 1px 6px rgba(0, 0, 0, 0.75);
        }}
        .stTabs [aria-selected="true"] {{
            background: rgba(34, 197, 94, 0.22) !important;
            border: 1px solid rgba(134, 239, 172, 0.55) !important;
            color: #ffffff !important;
        }}

        /* Transparent File Uploader & Camera Zone with Translucent Dashed Line */
        [data-testid="stFileUploaderDropzone"], [data-testid="stCameraInput"] {{
            background: transparent !important;
            border: 1px dashed rgba(134, 239, 172, 0.45) !important;
            border-radius: 14px !important;
            padding: 1rem !important;
        }}

        /* Transparent Buttons with Translucent Line Border */
        .stButton > button {{
            background: rgba(22, 163, 74, 0.25) !important;
            color: #ffffff !important;
            border: 1px solid rgba(134, 239, 172, 0.55) !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            text-shadow: 0 1px 6px rgba(0, 0, 0, 0.7);
            transition: all 0.15s ease;
        }}
        .stButton > button:hover {{
            background: rgba(34, 197, 94, 0.4) !important;
            border-color: #86efac !important;
        }}

        /* Progress Bar */
        .stProgress > div > div {{
            background-color: rgba(255, 255, 255, 0.15) !important;
        }}
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, #86efac, #22c55e) !important;
        }}

        /* Transparent Remedy Blockquotes with Translucent Line Border */
        blockquote {{
            background: transparent !important;
            border: 1px solid rgba(134, 239, 172, 0.3) !important;
            border-left: 3px solid rgba(134, 239, 172, 0.75) !important;
            border-radius: 10px !important;
            padding: 0.75rem 1rem !important;
            color: #f0fdf4 !important;
            text-shadow: 0 1px 8px rgba(0, 0, 0, 0.85);
        }}

        /* Transparent Inline Code Badges with Translucent Line Border */
        code {{
            background: transparent !important;
            color: #86efac !important;
            border: 1px solid rgba(134, 239, 172, 0.45) !important;
            border-radius: 6px;
            padding: 2px 7px;
            text-shadow: 0 1px 6px rgba(0, 0, 0, 0.8);
        }}

        /* Transparent Alert / Severity Boxes with Translucent Line Border */
        [data-testid="stAlert"] {{
            background: transparent !important;
            border: 1px solid rgba(134, 239, 172, 0.4) !important;
            border-radius: 12px !important;
            color: #f0fdf4 !important;
        }}

        /* Captured Leaf & Crop Thumbnail Frames */
        [data-testid="stImage"] img {{
            border-radius: 12px;
            border: 1px solid rgba(134, 239, 172, 0.42);
        }}

        /* Translucent Hairline Frame for Crop Info Tiles (No Solid Box Fill) */
        .crop-tile {{
            background: transparent;
            border: 1px solid rgba(134, 239, 172, 0.32);
            border-radius: 14px;
            padding: 0.75rem;
            margin-bottom: 0.85rem;
            text-shadow: 0 1px 8px rgba(0, 0, 0, 0.9);
        }}
        .crop-tile-title {{
            color: #bbf7d0;
            font-size: 1.02rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }}
        .crop-tile-count {{
            display: inline-block;
            border: 1px solid rgba(134, 239, 172, 0.45);
            color: #86efac;
            font-size: 0.76rem;
            font-weight: 600;
            padding: 1px 8px;
            border-radius: 999px;
            margin-bottom: 0.45rem;
        }}
        .crop-tile-desc {{
            color: #ecfdf5;
            font-size: 0.84rem;
            line-height: 1.4;
        }}
        .info-strip {{
            background: transparent;
            border: 1px solid rgba(134, 239, 172, 0.32);
            border-left: 3px solid rgba(134, 239, 172, 0.75);
            border-radius: 12px;
            padding: 0.85rem 1.1rem;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            line-height: 1.55;
            text-shadow: 0 1px 8px rgba(0, 0, 0, 0.9);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_leaf_theme("assets/leaf_bg")

MODEL_PATH = "models/crop_disease_model.keras"
LABELS_PATH = "models/class_labels.json"
IMG_SIZE = (224, 224)

CROP_CATALOG = [
    {
        "name": "Mango",
        "image": "assets/crops/mango.jpg",
        "count": "8 Classes (7 Diseases + Healthy)",
        "details": "Anthracnose, Bacterial Canker, Cutting Weevil, Die Back, Gall Midge, Powdery Mildew, Sooty Mould, Healthy."
    },
    {
        "name": "Brinjal (Eggplant)",
        "image": "assets/crops/brinjal.jpg",
        "count": "7 Classes (6 Diseases + Healthy)",
        "details": "Insect Pest, Leaf Spot, Mosaic Virus, Little Leaf, White Mold, Wilt Disease, Healthy."
    },
    {
        "name": "Groundnut",
        "image": "assets/crops/groundnut.jpg",
        "count": "5 Classes (4 Conditions + Healthy)",
        "details": "Early Leaf Spot (Tikka), Late Leaf Spot, Rust, Nutrient Deficiency, Healthy."
    },
    {
        "name": "Sugarcane",
        "image": "assets/crops/sugarcane.jpg",
        "count": "5 Classes (4 Diseases + Healthy)",
        "details": "Mosaic Virus, Red Rot / Red Spot, Rust, Yellow Leaf Disease, Healthy."
    },
    {
        "name": "Tomato",
        "image": "assets/crops/tomato.jpg",
        "count": "2 Blight Classes",
        "details": "Early Blight (Alternaria solani) & Late Blight (Phytophthora infestans)."
    },
    {
        "name": "Rice (Paddy)",
        "image": "assets/crops/rice.jpg",
        "count": "2 Classes (1 Disease + Healthy)",
        "details": "Sheath Blight (Rhizoctonia solani) & Healthy Leaf."
    }
]

@st.cache_resource
def load_model_and_labels():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
        return None, None
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)
    return model, labels

def is_likely_a_leaf(image: Image.Image) -> tuple[bool, str, float]:
    """
    Validates if an image is a plant leaf using HSV color space analysis.
    Accurately detects green leaves and yellow/brown diseased spots while 
    strictly rejecting skin, walls, and non-plant objects.
    """
    img_rgb = image.convert("RGB").resize((150, 150))
    img_hsv = img_rgb.convert("HSV")
    hsv_arr = np.array(img_hsv)
    
    h = hsv_arr[:, :, 0].astype(float)
    s = hsv_arr[:, :, 1].astype(float)
    v = hsv_arr[:, :, 2].astype(float)
    
    mean_brightness = np.mean(v)
    if mean_brightness < 20:
        return False, "The image is too dark. Please use better lighting.", 0.0
    if mean_brightness > 245:
        return False, "The image is overexposed (too bright/glaring).", 0.0
    
    green_mask = (h >= 30) & (h <= 100) & (s > 35) & (v > 30)
    green_ratio = np.sum(green_mask) / green_mask.size
    
    disease_spot_mask = (h >= 10) & (h < 30) & (s > 30) & (v > 30)
    spot_ratio = np.sum(disease_spot_mask) / disease_spot_mask.size
    
    plant_score = green_ratio + spot_ratio
    
    if plant_score < 0.15:
        return False, f"⚠️ **Not a leaf detected!** (Plant Score: {plant_score:.3f}). Please point your camera or upload a clear picture of a plant leaf.", plant_score
        
    return True, "Valid leaf detected.", plant_score

def predict_leaf(image: Image.Image, model, labels):
    image_resized = image.convert("RGB").resize(IMG_SIZE)
    img_array = tf.keras.utils.img_to_array(image_resized)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)[0]
    top_idx = int(np.argmax(predictions))
    confidence = float(predictions[top_idx]) * 100
    predicted_class = labels[top_idx]

    return predicted_class, confidence

# --- UI Layout ---
st.title("𝘊𝘳𝘰𝘱 𝘏𝘦𝘢𝘭𝘵𝘩 𝘢𝘯𝘥 𝘋𝘪𝘴𝘦𝘢𝘴𝘦 𝘔𝘰𝘯𝘪𝘵𝘰𝘳𝘪𝘯𝘨")
st.write("Scan a plant leaf using your device camera or upload a photo to detect diseases across **6 crops** and **29 conditions**.")


model, class_labels = load_model_and_labels()

if model is None:
    st.error("⚠️ Trained model not found! Run `python train_model.py` first.")
    st.stop()

tab1, tab2 = st.tabs(["📁 Upload Leaf Photo", "📷 Scan via Camera"])
selected_image = None

with tab1:
    uploaded_file = st.file_uploader("Choose a leaf image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        selected_image = Image.open(uploaded_file)

with tab2:
    camera_photo = st.camera_input("Take a clear picture of the leaf")
    if camera_photo is not None:
        selected_image = Image.open(camera_photo)

if selected_image is not None:
    st.divider()
    col1, col2 = st.columns([1, 1.3])

    with col1:
        st.image(selected_image, caption="Captured Leaf Sample", use_container_width=True)

    with col2:
        with st.spinner("Validating leaf foliage..."):
            is_valid, message, score = is_likely_a_leaf(selected_image)

        st.caption(f"🔍 HSV Plant Score: `{score:.3f}` (Required: >0.15)")

        if not is_valid:
            st.error(message)
        else:
            with st.spinner("Analyzing leaf disease..."):
                pred_class, confidence = predict_leaf(selected_image, model, class_labels)
                remedy_info = get_remedy(pred_class)

            st.subheader("🔬 Diagnosis Result")
            st.markdown(f"**Detected Condition:** `{remedy_info['disease_name']}`")
            st.markdown(f"**Crop Type:** {remedy_info['crop']}")
            st.markdown(f"**Confidence Score:** `{confidence:.2f}%`")
            st.progress(int(confidence))

            st.subheader("💊 Recommended Treatment")
            st.info(f"**Severity Level:** {remedy_info['severity']}")
            st.markdown(f"**1. Chemical Medicine:**\n> {remedy_info['chemical_medicine']}")
            st.markdown(f"**2. Organic Alternative:**\n> {remedy_info['organic_remedy']}")
            st.markdown(f"**3. Preventive Measures:**\n> {remedy_info['prevention']}")

# --- Supported Crops & Important User Info (Below Upload Area, Transparent with Translucent Borders) ---
st.divider()
st.subheader("🌱 Supported Crops & Disease Coverage (6 Crops · 29 Classes)")
st.write("This AI diagnostic model is trained to identify healthy foliage and **24 distinct plant diseases/deficiencies** across the following crops:")

for row_start in range(0, len(CROP_CATALOG), 3):
    cols = st.columns(3)
    for col, crop in zip(cols, CROP_CATALOG[row_start:row_start + 3]):
        with col:
            img_path = resolve_asset_image(os.path.splitext(crop["image"])[0])
            if img_path:
                st.image(img_path, use_container_width=True)
            st.markdown(
                f"""
                <div class="crop-tile">
                    <div class="crop-tile-title">{crop['name']}</div>
                    <div class="crop-tile-count">{crop['count']}</div>
                    <div class="crop-tile-desc">{crop['details']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

st.subheader("📌 Important Scanning Guidelines")
st.markdown(
    """
    <div class="info-strip">
        <strong>1. Single Leaf Focus:</strong> Hold one affected leaf close to the camera so the leaf fills most of the frame.<br>
        <strong>2. Natural Daylight:</strong> Capture photos in bright, even daylight—avoid harsh shadows or camera flash glare.<br>
        <strong>3. Automatic Leaf Filter:</strong> Non-leaf objects (walls, hands, soil) are automatically filtered out using HSV foliage validation.<br>
        <strong>4. Agronomist Advisory:</strong> Chemical and organic dosages serve as preliminary field guidance—always verify local agricultural extension labels before spraying.
    </div>
    """,
    unsafe_allow_html=True
)

# --- Bottom Ownership & Copyright Footer ---
st.divider()
st.markdown(
    """
    <div style="border: 1px solid rgba(134, 239, 172, 0.32); border-radius: 14px; padding: 1rem 1.2rem; margin-top: 0.5rem; text-align: center; text-shadow: 0 1px 8px rgba(0, 0, 0, 0.9);">
        <div style="color: #bbf7d0; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.35rem;">
            🛡️ Developed &amp; Owned by Shaik Muhammad Abbas
        </div>
        <div style="color: #f0fdf4; font-size: 0.88rem; margin-bottom: 0.3rem;">
            🔒 Copyright © 2026 Shaik Muhammad Abbas &nbsp;|&nbsp;
            <a href="https://github.com/abbasshaik-ops/crop-disease-monitor" target="_blank" style="color: #86efac; text-decoration: underline; font-weight: 600;">
                GitHub: abbasshaik-ops/crop-disease-monitor
            </a>
        </div>
        <div style="color: #dcfce7; font-size: 0.82rem;">
            © 2026 All Rights Reserved.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
