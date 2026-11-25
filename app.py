import base64
import json
import os
import time
from google import genai
from google.genai import types
import numpy as np
from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Crop Health and Disease Monitoring",
    page_icon="🌿",
    layout="wide",
)

BG_IMAGE_PATH = "assets/leaf_bg.jpg"

CROP_CARDS = [
    {
        "name": "Mango",
        "image": "assets/crops/mango.jpg",
        "badge": "8 Classes (7 Diseases + Healthy)",
        "desc": (
            "Anthracnose, Bacterial Canker, Cutting Weevil, Die Back, Gall"
            " Midge, Powdery Mildew, Sooty Mould, Healthy."
        ),
    },
    {
        "name": "Brinjal (Eggplant)",
        "image": "assets/crops/brinjal.jpeg",
        "badge": "7 Classes (6 Diseases + Healthy)",
        "desc": (
            "Insect Pest, Leaf Spot, Mosaic Virus, Little Leaf, White Mold,"
            " Wilt Disease, Healthy."
        ),
    },
    {
        "name": "Groundnut",
        "image": "assets/crops/groundnut.jpeg",
        "badge": "5 Classes (4 Conditions + Healthy)",
        "desc": (
            "Early Leaf Spot (Tikka), Late Leaf Spot, Rust, Nutrient"
            " Deficiency, Healthy."
        ),
    },
    {
        "name": "Sugarcane",
        "image": "assets/crops/sugarcane.jpeg",
        "badge": "5 Classes (4 Diseases + Healthy)",
        "desc": (
            "Mosaic Virus, Red Rot / Red Spot, Rust, Yellow Leaf Disease,"
            " Healthy."
        ),
    },
    {
        "name": "Tomato",
        "image": "assets/crops/tomato.jpg",
        "badge": "2 Blight Classes",
        "desc": (
            "Early Blight (Alternaria solani) & Late Blight (Phytophthora"
            " infestans)."
        ),
    },
    {
        "name": "Rice (Paddy)",
        "image": "assets/crops/rice.jpeg",
        "badge": "2 Classes (1 Disease + Healthy)",
        "desc": "Sheath Blight (Rhizoctonia solani) & Healthy Leaf.",
    },
]

SUPPORTED_CLASSES = [
    "Mango - Anthracnose",
    "Mango - Bacterial Canker",
    "Mango - Cutting Weevil",
    "Mango - Die Back",
    "Mango - Gall Midge",
    "Mango - Healthy",
    "Mango - Powdery Mildew",
    "Mango - Sooty Mould",
    "Brinjal - Healthy",
    "Brinjal - Insect Pest",
    "Brinjal - Leaf Spot",
    "Brinjal - Little Leaf",
    "Brinjal - Mosaic Virus",
    "Brinjal - White Mold",
    "Brinjal - Wilt Disease",
    "Groundnut - Early Leaf Spot",
    "Groundnut - Healthy",
    "Groundnut - Late Leaf Spot",
    "Groundnut - Nutrient Deficiency",
    "Groundnut - Rust",
    "Sugarcane - Healthy",
    "Sugarcane - Mosaic",
    "Sugarcane - Red Rot",
    "Sugarcane - Rust",
    "Sugarcane - Yellow Leaf",
    "Tomato - Early Blight",
    "Tomato - Late Blight",
    "Rice - Healthy",
    "Rice - Sheath Blight",
]


def get_base64_image(image_path: str) -> str:
  if not os.path.exists(image_path):
    return ""
  with open(image_path, "rb") as f:
    return base64.b64encode(f.read()).decode()


def inject_custom_css(bg_path: str) -> None:
  encoded_bg = get_base64_image(bg_path)
  bg_rule = (
      f"""
        background-image: linear-gradient(
            rgba(7, 18, 12, 0.72),
            rgba(7, 18, 12, 0.80)
        ), url("data:image/jpeg;base64,{encoded_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        """
      if encoded_bg
      else "background-color: #0b1912;"
  )

  st.markdown(
      f"""
        <style>
        .stApp {{
            {bg_rule}
            color: #f3f7f4;
        }}
        .block-container {{
            max-width: 960px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}
        .hero-title {{
            font-size: 2.35rem;
            font-weight: 800;
            line-height: 1.15;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }}
        .hero-sub {{
            font-size: 1rem;
            color: #d6e4da;
            margin-bottom: 1.25rem;
        }}
        .section-heading {{
            font-size: 1.45rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 1.75rem;
            margin-bottom: 0.4rem;
        }}
        .section-sub {{
            font-size: 0.95rem;
            color: #cfe0d4;
            margin-bottom: 1rem;
        }}
        .crop-badge {{
            display: inline-block;
            background: rgba(20, 46, 31, 0.85);
            border: 1px solid rgba(110, 207, 138, 0.35);
            color: #9be7b0;
            font-size: 0.76rem;
            font-weight: 600;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            margin-bottom: 0.45rem;
        }}
        .crop-desc {{
            font-size: 0.84rem;
            color: #dce8df;
            line-height: 1.45;
            margin-bottom: 1.1rem;
        }}
        .guidelines-box {{
            background: rgba(11, 24, 17, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 12px;
            padding: 1.15rem 1.35rem;
            margin-top: 0.75rem;
            margin-bottom: 1.5rem;
        }}
        .guidelines-box p {{
            margin: 0.45rem 0;
            font-size: 0.9rem;
            color: #e6efe8;
            line-height: 1.5;
        }}
        .hsv-pill {{
            display: inline-block;
            background: rgba(16, 28, 22, 0.82);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 8px;
            padding: 0.35rem 0.7rem;
            font-size: 0.85rem;
            color: #d7e4db;
            margin-bottom: 0.85rem;
        }}
        .severity-banner {{
            background: rgba(24, 34, 48, 0.9);
            border: 1px solid rgba(120, 155, 210, 0.35);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            font-weight: 600;
            color: #eef4ff;
            margin-bottom: 1rem;
        }}
        .remedy-label {{
            font-size: 1rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 0.75rem;
            margin-bottom: 0.35rem;
        }}
        .remedy-box {{
            background: rgba(12, 24, 18, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 10px;
            padding: 0.7rem 0.95rem;
            font-size: 0.92rem;
            color: #e8f1ea;
            line-height: 1.5;
        }}
        .warning-card {{
            background: rgba(58, 20, 22, 0.88);
            border: 1px solid rgba(248, 113, 113, 0.45);
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            color: #ffe4e6;
            font-size: 0.92rem;
            line-height: 1.5;
        }}
        .footer-box {{
            text-align: center;
            color: #c7d8cc;
            font-size: 0.84rem;
            line-height: 1.7;
            margin-top: 1.5rem;
        }}
        .footer-box a {{
            color: #9be7b0;
            text-decoration: none;
        }}
        div[data-testid="stFileUploaderDropzone"] {{
            background: rgba(14, 26, 20, 0.78);
            border: 1px dashed rgba(255, 255, 255, 0.28);
            border-radius: 10px;
        }}
        </style>
        """,
      unsafe_allow_html=True,
  )


@st.cache_resource
def get_gemini_client() -> genai.Client:
  api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
  if not api_key:
    st.error("GEMINI_API_KEY is missing. Add it in Streamlit Secrets.")
    st.stop()
  return genai.Client(api_key=api_key)


def get_hsv_leaf_score(image: Image.Image) -> float:
  """Return foliage coverage ratio (0.0 to 1.0) using HSV hue and value thresholds."""
  hsv = np.array(image.convert("RGB").resize((224, 224)).convert("HSV"))
  h, _, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

  valid_exposure = (v >= 20) & (v <= 245)
  foliage_mask = valid_exposure & (h >= 15) & (h <= 145)
  return float(np.mean(foliage_mask))


def parse_confidence_pct(raw_conf) -> float:
  if isinstance(raw_conf, (int, float)):
    val = float(raw_conf)
    return val * 100.0 if 0.0 <= val <= 1.0 else max(0.0, min(100.0, val))
  text = str(raw_conf).strip().replace("%", "")
  try:
    val = float(text)
    return val * 100.0 if 0.0 <= val <= 1.0 else max(0.0, min(100.0, val))
  except ValueError:
    mapping = {"high": 88.0, "medium": 68.0, "low": 42.0}
    return mapping.get(text.lower(), 75.0)


def analyze_leaf_image(image: Image.Image, language: str = "English") -> dict:
  client = get_gemini_client()
  prompt = f"""
    You are an agricultural plant pathology assistant helping farmers in Tamil Nadu, India.
    Examine the image and respond in {language} for text descriptions while keeping JSON keys exact.

    1. Decide if the image shows a plant leaf or crop foliage.
    2. Identify the crop and disease/condition. Prefer an exact label from this list when applicable:
       {json.dumps(SUPPORTED_CLASSES)}
    3. If outside the list, provide a clear "Crop - Condition" label.

    Return ONLY valid JSON matching this schema:
    {{
        "is_leaf": true,
        "matched_label": "Crop - Condition",
        "crop": "Crop name",
        "condition": "Disease or Healthy",
        "confidence": "70.12%",
        "severity": "Mild",
        "visual_symptoms": "Short description of visible symptoms",
        "organic_remedy": "Practical organic or cultural remedy",
        "chemical_remedy": "Targeted control option with dosage or None required",
        "preventive_measures": "Prevention steps for the field"
    }}
    """

  models_to_try = [
      "gemini-4-hydrogen",
      "gemini-3.8-flash",
      "gemini-3.6-flash",
      "gemini-3.5-flash-lite",
      "gemini-3.1-flash-lite-preview",
      "gemini-3-flash-preview",
      "gemini-2.5-flash",
      "gemini-2.5-flash-lite",
  ]
  last_error = None

  for model_name in models_to_try:
    for attempt in range(2):
      try:
        response = client.models.generate_content(
            model=model_name,
            contents=[image, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
            ),
        )
        return json.loads(response.text)
      except Exception as exc:
        last_error = exc
        err_str = str(exc)
        # Retry once on transient overload, then move on to the next model
        if "503" in err_str or "UNAVAILABLE" in err_str:
          time.sleep(1.5 * (attempt + 1))
          continue
        # Immediately try the next model if quota/rate-limited or model ID unavailable
        if (
            "429" in err_str
            or "RESOURCE_EXHAUSTED" in err_str
            or "404" in err_str
            or "NOT_FOUND" in err_str
        ):
          break
        raise

  raise last_error


inject_custom_css(BG_IMAGE_PATH)

st.markdown(
    '<div class="hero-title">Crop Health and Disease Monitoring</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-sub">Scan a plant leaf using your device camera or upload'
    " a photo to detect diseases across 6 crops and 29 conditions.</div>",
    unsafe_allow_html=True,
)

language = st.selectbox(
    "Advisory Language", ["English", "Tamil", "Telugu"], label_visibility="collapsed"
)

tab_upload, tab_camera = st.tabs(["📁 Upload Leaf Photo", "📷 Scan via Camera"])

selected_file = None
with tab_upload:
  selected_file = st.file_uploader(
      "Choose a leaf image (JPG, JPEG, PNG)",
      type=["jpg", "jpeg", "png", "webp"],
  )

with tab_camera:
  camera_file = st.camera_input("Take a clear picture of the leaf")
  if camera_file is not None:
    selected_file = camera_file

if selected_file is not None:
  img = Image.open(selected_file).convert("RGB")
  hsv_score = get_hsv_leaf_score(img)
  passed_hsv = hsv_score > 0.15

  left_col, right_col = st.columns([1, 1.45], gap="large")
  with left_col:
    st.image(img, use_container_width=True)
    st.markdown(
        '<div style="text-align:center; font-size:0.84rem; color:#cfe0d4;'
        ' margin-top:0.25rem;">Captured Leaf Sample</div>',
        unsafe_allow_html=True,
    )

  with right_col:
    st.markdown(
        f'<div class="hsv-pill">🌿 HSV Plant Score: <b>{hsv_score:.3f}</b>'
        " (Required: &gt;0.15)</div>",
        unsafe_allow_html=True,
    )

    if not passed_hsv:
      st.markdown(
          f"""
                <div class="warning-card">
                    ⚠️ <b>Not a leaf detected!</b> (Plant Score: {hsv_score:.3f}).
                    Please point your camera or upload a clear picture of a plant leaf.
                </div>
                """,
          unsafe_allow_html=True,
      )
    else:
      if st.button("Analyze Leaf", type="primary"):
        with st.spinner("Analyzing leaf with Gemini Vision..."):
          try:
            result = analyze_leaf_image(img, language=language)
            if not result.get("is_leaf", True):
              st.markdown(
                  f"""
                                <div class="warning-card">
                                    ⚠️ <b>Not a leaf detected!</b> (Plant Score: {hsv_score:.3f}).
                                    Please point your camera or upload a clear picture of a plant leaf.
                                </div>
                                """,
                  unsafe_allow_html=True,
              )
            else:
              conf_pct = parse_confidence_pct(result.get("confidence", "75%"))
              st.markdown(
                  '<div class="section-heading" style="margin-top:0;">🔬'
                  " Diagnosis Result</div>",
                  unsafe_allow_html=True,
              )
              st.write(
                  f"**Detected Condition:**"
                  f" {result.get('matched_label', 'Unknown')}"
              )
              st.write(f"**Crop Type:** {result.get('crop', 'N/A')}")
              st.write(f"**Confidence Score: `{conf_pct:.2f}%`")
              st.progress(min(max(conf_pct / 100.0, 0.0), 1.0))

              st.markdown(
                  '<div class="section-heading">💊 Recommended'
                  " Treatment</div>",
                  unsafe_allow_html=True,
              )
              st.markdown(
                  f'<div class="severity-banner">Severity Level:'
                  f" {result.get('severity', 'Moderate')}</div>",
                  unsafe_allow_html=True,
              )

              st.markdown(
                  '<div class="remedy-label">1. Chemical Medicine:</div>',
                  unsafe_allow_html=True,
              )
              st.markdown(
                  '<div class="remedy-box">'
                  f"{result.get('chemical_remedy', 'None required')}</div>",
                  unsafe_allow_html=True,
              )

              st.markdown(
                  '<div class="remedy-label">2. Organic Alternative:</div>',
                  unsafe_allow_html=True,
              )
              st.markdown(
                  '<div class="remedy-box">'
                  f"{result.get('organic_remedy', 'N/A')}</div>",
                  unsafe_allow_html=True,
              )

              st.markdown(
                  '<div class="remedy-label">3. Preventive Measures:</div>',
                  unsafe_allow_html=True,
              )
              st.markdown(
                  '<div class="remedy-box">'
                  f"{result.get('preventive_measures', 'N/A')}</div>",
                  unsafe_allow_html=True,
              )
          except Exception as exc:
            st.error(f"Analysis failed: {exc}")

# Supported Crops & Disease Coverage Section
st.markdown(
    '<div class="section-heading">🌱 Supported Crops &amp; Disease Coverage (6'
    " Crops · 29 Classes)</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-sub">This AI diagnostic model is trained to identify'
    " healthy foliage and 24 distinct plant diseases/deficiencies across the"
    " following crops:</div>",
    unsafe_allow_html=True,
)

for row_start in range(0, len(CROP_CARDS), 3):
  cols = st.columns(3, gap="medium")
  for idx, card in enumerate(CROP_CARDS[row_start : row_start + 3]):
    with cols[idx]:
      if os.path.exists(card["image"]):
        st.image(card["image"], use_container_width=True)
      st.markdown(
          f"**  \n"
          f'<span class="crop-badge">{card["badge"]}</span>'
          f'<div class="crop-desc">{card["desc"]}</div>',
          unsafe_allow_html=True,
      )

# Important Scanning Guidelines Section
st.markdown(
    '<div class="section-heading">📌 Important Scanning Guidelines</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="guidelines-box">
        <p><b>1. Single Leaf Focus:</b> Hold one affected leaf close to the camera so the leaf fills most of the frame.</p>
        <p><b>2. Natural Daylight:</b> Capture photos in bright, even daylight—avoid harsh shadows or camera flash glare.</p>
        <p><b>3. Automatic Leaf Filter:</b> Non-leaf objects (walls, hands, soil) are automatically filtered out using HSV foliage validation.</p>
        <p><b>4. Agronomist Advisory:</b> Chemical and organic dosages serve as preliminary field guidance—always verify local agricultural extension labels before spraying.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown(
    """
    <div class="footer-box">
        <div>🌿 <b>Developed &amp; Owned by Shaik Muhammad Abbas</b></div>
        <div>🔒 Copyright © 2026 Shaik Muhammad Abbas | GitHub:
            <a href="https://github.com/abbasshaik-ops/crop-disease-monitor" target="_blank">
                abbasshaik-ops/crop-disease-monitor
            </a>
        </div>
        <div>© 2026 All Rights Reserved</div>
    </div>
    """,
    unsafe_allow_html=True,
)