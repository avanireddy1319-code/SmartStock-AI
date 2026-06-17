# smartstock_theme.py
import base64
from pathlib import Path
import streamlit as st

ASSETS = Path(__file__).parent / "assets"

def _b64(name: str) -> str:
    p = ASSETS / name
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode()

def inject_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(124,58,237,.25), transparent 35%),
            radial-gradient(circle at top right, rgba(34,211,238,.18), transparent 35%),
            linear-gradient(180deg, #05060f 0%, #0a0d1f 50%, #05060f 100%);
        color: #e6ecff;
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(10,14,32,.92);
        border-right: 1px solid rgba(124,58,237,.3);
        backdrop-filter: blur(18px);
    }

    section[data-testid="stSidebar"] * {
        color: #d6def0 !important;
    }

    div[data-testid="stMetric"],
    div[data-testid="stDataFrame"],
    div[data-testid="stAlert"],
    div[data-testid="stForm"] {
        background: rgba(255,255,255,.05);
        border: 1px solid rgba(165,243,252,.15);
        border-radius: 18px;
        backdrop-filter: blur(18px);
        padding: 18px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(
            135deg,
            #22d3ee,
            #3b82f6,
            #8b5cf6
        );
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: 600;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background: rgba(10,14,32,.6);
        color: white;
        border-radius: 12px;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    </style>
    """, unsafe_allow_html=True)

def hero(title: str, subtitle: str = "", image: str = "hero_dashboard.png"):
        img_b64 = _b64(image)

        img_tag = (
            f'<img src="data:image/png;base64,{img_b64}"/>'
            if img_b64 else ""
        )

        st.markdown(f"""
        <div class="ss-hero">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
        </div>
        {img_tag}
    </div>
    """, unsafe_allow_html=True)


def feature_card(image: str, title: str, desc: str):
    img_b64 = _b64(image)
    img_tag = f'<img src="data:image/png;base64,{img_b64}"/>' if img_b64 else ""
    st.markdown(f"""
    <div class="ss-feature">
      {img_tag}
      <h4>{title}</h4>
      <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)


def sticker(image: str, height: int = 180):
    img_b64 = _b64(image)
    if not img_b64: return
    st.markdown(
        f'<div style="text-align:center"><img src="data:image/png;base64,{img_b64}" style="height:{height}px"/></div>',
        unsafe_allow_html=True,
    )



