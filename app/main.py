import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from PIL import Image
from src.predict import predict_food
from src.nutrition import get_nutrition


st.set_page_config(page_title='FoodSnap AI', layout='wide')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

* { font-family: 'Nunito', sans-serif !important; }

.stApp {
    background: #ffffff !important;
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* Card style — targets st.container(border=True) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border-radius: 18px !important;
    border: 1px solid rgba(220, 220, 220, 0.6) !important;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.10) !important;
    padding: 18px 16px !important;
    margin-bottom: 18px !important; 
}

/* Fix background of the content itself */
.block-container, .st-emotion-cache-1wmy9hl, .st-emotion-cache-1y4p8pa {
    background-color: #ffffff00 !important;
}

/* Fix background of elements inside columns */
[data-testid="column"] > div {
    background: transparent !important;
}

/* Progress bar */
[data-testid="stProgressBar"] > div {
    background: #e8f5e9 !important;
    border-radius: 10px !important;
    height: 10px !important;
}
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #4caf50, #81c784) !important;
    border-radius: 10px !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed #aacfaa !important;
    border-radius: 14px !important;
    padding: 6px !important;
    background: rgba(255,255,255,0.4) !important;
}

/* Bottom button */
.stButton > button {
    background: white !important;
    color: #333 !important;
    border: 1px solid #ccc !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.09) !important;
    padding: 10px 28px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    box-shadow: 0 4px 18px rgba(0,0,0,0.14) !important;
    transform: translateY(-1px) !important;
}

/* Nutrition rows */
.nutrition-row {
    display: flex;
    justify-content: space-between;
    padding: 7px 0;
    border-bottom: 1px solid #f0f0f0;
    font-size: 0.93rem;
    color: #333;
}
.nutrition-row:last-child { border-bottom: none; }
.nutrition-row .label { font-weight: 700; color: #2a4a2a; }
.nutrition-row .value { color: #666; font-weight: 500; }

.confidence-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f0faf0;
    border: 1px solid #c3e6c3;
    border-radius: 8px;
    padding: 5px 14px;
    font-size: 0.9rem;
    color: #2e7d32;
    font-weight: 700;
    margin-top: 6px;
}
/* Make images full width inside Streamlit */
[data-testid="stImage"] img {
    width: 100% !important;
    height: auto !important;
    border-radius: 14px;
}

/* Override card padding to allow image to expand */
[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 14px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#1e3a1e; font-size:2.2rem; font-weight:800; margin-bottom:0;'>
    🌿📷 FoodSnap AI
</h1>
<p style='text-align:center; color:#4a6a4a; font-size:1.05rem; font-weight:600; margin-top:4px; margin-bottom:2rem;'>
    Instant Nutrition Insights
</p>
""", unsafe_allow_html=True)

# ── Two Columns ───────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap='medium')

with col1:
    # Card 1: Upload
    with st.container(border=True):
        st.markdown("##### 📁 Upload your food image here")
        uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'], label_visibility='collapsed')

    # Card 2: Meal image (only after upload)
    if uploaded_file:
        img = Image.open(uploaded_file)
        with st.container(border = True):
            st.markdown("**Your Meal:**")
            st.image(img, use_container_width=True)
   
    
with col2:
    if uploaded_file:
        food, conf = predict_food(img)
        safe_val = float(conf) / 100.0 if float(conf) > 1.0 else float(conf)

        # Card 3: Prediction
        with st.container(border=True):
            st.markdown("**Prediction:**")
            st.markdown(f"Predicted Food: **{food}**")
            st.progress(safe_val)
            st.markdown(
                f'<div class="confidence-badge">✅ {safe_val*100:.0f}% Confidence</div>',
                unsafe_allow_html=True
            )

        # Card 4: Nutrition
        nutrition = get_nutrition(food)
        units = {
            "calories": "kcal", "protein": "g", "fat": "g",
            "carbs": "g"
        }

        with st.container(border=True):
            nutrition_items = list(nutrition.items())[1:6]
            st.markdown("**Nutritional Breakdown**")
            st.caption("(per serving):")
            st.markdown(f"**{food}**")
            st.divider()
            rows_html = "".join([
                f'<div class="nutrition-row">'
                f'<span class="label">{k.capitalize()}:</span>'
                f'<span class="value">{v} {units.get(k.lower(), "")}</span>'
                f'</div>'
                for k, v in nutrition_items
            ])
            st.markdown(rows_html, unsafe_allow_html=True)

    else:
        # Placeholder cards when no image uploaded
        with st.container(border=True):
            st.markdown("**Prediction:**")
            st.markdown("<span style='color:#bbb;'>Upload an image to see the prediction.</span>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("**Nutritional Breakdown**")
            st.caption("(per serving):")
            st.markdown("<span style='color:#bbb;'>Nutrition info will appear here.</span>", unsafe_allow_html=True)

# ── Bottom Button ─────────────────────────────────────────────────────────
# if uploaded_file:
#     st.markdown("<br>", unsafe_allow_html=True)
#     _, center, _ = st.columns([2, 1, 2])
#     with center:
#         if st.button("🔄 Analyze Another Image"):
#             st.rerun()

