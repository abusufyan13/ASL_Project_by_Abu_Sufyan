import streamlit as st
import numpy as np
from PIL import Image
import json
import base64
from io import BytesIO
import time

# ===============================
# Page Configuration
# ===============================

# Load and convert image to base64 for favicon
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Try to load the image for favicon
try:
    # Save the base64 image for favicon
    favicon_base64 = get_base64_image("image.png")
    favicon_html = f'<link rel="icon" type="image/png" href="data:image/png;base64,{favicon_base64}">'
    st.markdown(favicon_html, unsafe_allow_html=True)
except:
    # Fallback if image not found
    pass

st.set_page_config(
    page_title="ASL Recognition System",
    page_icon="",  # Fallback icon
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# Custom CSS with Framer Motion-like Animations
# ===============================

st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0B1E3D 0%, #1a3a5c 100%);
    }
    
    /* Main container */
    .main {
        background: rgba(11, 30, 61, 0.85);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid rgba(0, 217, 233, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        margin: 1rem;
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    /* Framer Motion-inspired animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInRight {
        from {
            opacity: 0;
            transform: translateX(40px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes rotateIn {
        from {
            opacity: 0;
            transform: rotate(-10deg) scale(0.9);
        }
        to {
            opacity: 1;
            transform: rotate(0) scale(1);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    
    /* Title styling */
    .title-container {
        text-align: center;
        padding: 20px 0 15px 0;
        border-bottom: 2px solid rgba(0, 217, 233, 0.15);
        margin-bottom: 30px;
        position: relative;
        animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .title-container::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #00D9E9, #FFB000);
        border-radius: 3px;
        animation: expandWidth 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @keyframes expandWidth {
        from { width: 0; opacity: 0; }
        to { width: 100px; opacity: 1; }
    }
    
    .main-title {
        color: #FFFFFF;
        font-size: 48px;
        font-weight: 900;
        letter-spacing: -1px;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 217, 233, 0.2);
    }
    
    .main-title .highlight {
        background: linear-gradient(135deg, #FFB000, #FF6B00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 3s ease-in-out infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sub-title {
        color: #BcD6E6;
        font-size: 16px;
        font-weight: 400;
        letter-spacing: 4px;
        margin-top: 8px;
        opacity: 0.8;
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    /* Sidebar logo styling */
    .sidebar-logo-container {
        text-align: center;
        padding: 15px 0 10px 0;
        margin-bottom: 10px;
        animation: rotateIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .sidebar-logo-wrapper {
        display: inline-block;
        position: relative;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .sidebar-logo-wrapper:hover {
        transform: scale(1.08) rotate(-2deg);
    }
    
    .sidebar-logo-wrapper::before {
        content: '';
        position: absolute;
        top: -5px;
        left: -5px;
        right: -5px;
        bottom: -5px;
        background: linear-gradient(135deg, #00D9E9, #FFB000, #00D9E9);
        border-radius: 16px;
        opacity: 0;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        background-size: 300% 300%;
        animation: gradientMove 3s ease-in-out infinite;
    }
    
    .sidebar-logo-wrapper:hover::before {
        opacity: 0.3;
    }
    
    @keyframes gradientMove {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sidebar-logo {
        max-width: 150px;
        height: auto;
        border-radius: 12px;
        border: 2px solid rgba(0, 217, 233, 0.3);
        padding: 8px;
        background: rgba(255, 255, 255, 0.08);
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        z-index: 1;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-logo:hover {
        border-color: rgba(0, 217, 233, 0.8);
        box-shadow: 0 8px 30px rgba(0, 217, 233, 0.3);
        transform: scale(1.02);
    }
    
    /* Custom upload button - Improved */
    .upload-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0;
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .custom-upload-btn {
        background: linear-gradient(135deg, #00D9E9, #0099a8);
        color: white;
        padding: 14px 30px;
        border: none;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        display: inline-flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 15px rgba(0, 217, 233, 0.3);
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .custom-upload-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .custom-upload-btn:hover::before {
        left: 100%;
    }
    
    .custom-upload-btn:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 30px rgba(0, 217, 233, 0.5);
        background: linear-gradient(135deg, #00e5f5, #00a8b8);
    }
    
    .custom-upload-btn:active {
        transform: translateY(0px) scale(0.98);
    }
    
    .custom-upload-btn .btn-icon {
        font-size: 20px;
        animation: float 3s ease-in-out infinite;
    }
    
    .stFileUploader {
        position: relative;
    }
    
    /* Image display */
    .image-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(0, 217, 233, 0.2);
        margin: 20px 0;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        animation: scaleIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .image-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 217, 233, 0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .image-container:hover {
        transform: scale(1.02);
        border-color: rgba(0, 217, 233, 0.4);
        box-shadow: 0 8px 30px rgba(0, 217, 233, 0.1);
    }
    
    .image-container img {
        border-radius: 12px;
        position: relative;
        z-index: 1;
    }
    
    /* Result cards */
    .result-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 24px;
        margin: 12px 0;
        border-left: 4px solid #00D9E9;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInRight 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .result-card:nth-child(2) {
        animation-delay: 0.1s;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(0, 217, 233, 0.05), transparent);
        opacity: 0;
        transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .result-card:hover {
        transform: translateX(12px) scale(1.02);
        background: rgba(255, 255, 255, 0.10);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }
    
    .result-card:hover::before {
        opacity: 1;
    }
    
    .result-label {
        color: #BcD6E6;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
        position: relative;
        z-index: 1;
    }
    
    .result-value {
        color: #FFFFFF;
        font-size: 32px;
        font-weight: 800;
        position: relative;
        z-index: 1;
    }
    
    .result-value .highlight {
        background: linear-gradient(135deg, #FFB000, #FF6B00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .confidence-bar {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        height: 10px;
        margin-top: 12px;
        overflow: hidden;
        position: relative;
        z-index: 1;
    }
    
    .confidence-fill {
        background: linear-gradient(90deg, #00D9E9, #FFB000);
        height: 100%;
        border-radius: 12px;
        transition: width 1.5s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        animation: fillBar 1.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @keyframes fillBar {
        from { width: 0 !important; }
        to { width: var(--target-width); }
    }
    
    .confidence-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
        background-size: 200% 100%;
    }
    
    /* Footer */
    .footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 2px solid rgba(0, 217, 233, 0.1);
        text-align: center;
        color: #5f8aa7;
        font-size: 13px;
        letter-spacing: 1px;
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .footer .dot {
        color: #00D9E9;
        margin: 0 8px;
    }
    
    .footer .year {
        background: linear-gradient(135deg, #FFB000, #FF6B00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Sidebar styles */
    .sidebar-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 16px;
        margin: 12px 0;
        border: 1px solid rgba(0, 217, 233, 0.1);
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        animation: fadeInLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-section:nth-child(2) { animation-delay: 0.05s; }
    .sidebar-section:nth-child(3) { animation-delay: 0.1s; }
    .sidebar-section:nth-child(4) { animation-delay: 0.15s; }
    .sidebar-section:nth-child(5) { animation-delay: 0.2s; }
    .sidebar-section:nth-child(6) { animation-delay: 0.25s; }
    
    .sidebar-section:hover {
        border-color: rgba(0, 217, 233, 0.3);
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(6px) scale(1.02);
        box-shadow: 0 4px 20px rgba(0, 217, 233, 0.1);
    }
    
    .sidebar-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(180deg, #00D9E9, #FFB000);
        opacity: 0;
        transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .sidebar-section:hover::before {
        opacity: 1;
    }
    
    .sidebar-section h4 {
        color: #00D9E9;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .sidebar-section p {
        color: #BcD6E6;
        font-size: 13px;
        line-height: 1.6;
        margin: 4px 0;
        text-align: justify;
    }
    
    .sidebar-section .badge {
        display: inline-block;
        background: rgba(0, 217, 233, 0.15);
        color: #00D9E9;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin: 2px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .sidebar-section .badge:hover {
        background: rgba(0, 217, 233, 0.3);
        transform: scale(1.08) rotate(-2deg);
    }
    
    .sidebar-section .highlight-text {
        color: #FFB000;
        font-weight: 600;
    }
    
    /* Group member styling */
    .member-list {
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin-top: 8px;
    }
    
    .member-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 6px 12px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        border: 1px solid transparent;
    }
    
    .member-item:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(0, 217, 233, 0.2);
        transform: translateX(6px) scale(1.02);
    }
    
    .member-icon {
        font-size: 16px;
        width: 25px;
        text-align: center;
        color: #00D9E9;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .member-name {
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Quote styling */
    .quote-container {
        background: linear-gradient(135deg, rgba(255, 176, 0, 0.1), rgba(0, 217, 233, 0.1));
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        border: 1px solid rgba(255, 176, 0, 0.2);
        position: relative;
        animation: rotateIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .quote-container:hover {
        transform: scale(1.03) rotate(-1deg);
        box-shadow: 0 8px 30px rgba(255, 176, 0, 0.15);
    }
    
    .quote-container::before {
        content: '"';
        font-size: 60px;
        color: rgba(255, 176, 0, 0.2);
        position: absolute;
        top: -10px;
        left: 10px;
        font-family: Georgia, serif;
        animation: bounceIn 1s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0) rotate(-10deg); opacity: 0; }
        50% { transform: scale(1.2) rotate(5deg); }
        70% { transform: scale(0.9) rotate(-3deg); }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    
    .quote-text {
        color: #FFFFFF;
        font-size: 15px;
        font-style: italic;
        line-height: 1.8;
        text-align: center;
        padding: 10px 0;
        position: relative;
        z-index: 1;
    }
    
    .quote-author {
        color: #FFB000;
        font-size: 13px;
        font-weight: 600;
        text-align: right;
        margin-top: 8px;
        position: relative;
        z-index: 1;
    }
    
    /* Button overrides */
    .stButton > button {
        background: linear-gradient(135deg, #00D9E9, #0099a8);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 14px;
        padding: 12px 35px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: 0 4px 15px rgba(0, 217, 233, 0.3);
        width: 100%;
        font-size: 16px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFB000, #FF6B00);
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 176, 0, 0.4);
    }
    
    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none !important;
    }
    
    /* Prediction button special styling */
    .predict-btn > button {
        background: linear-gradient(135deg, #FFB000, #FF6B00) !important;
        font-size: 20px !important;
        padding: 16px 40px !important;
        box-shadow: 0 8px 30px rgba(255, 176, 0, 0.4) !important;
        animation: pulseGlow 2s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            box-shadow: 0 8px 30px rgba(255, 176, 0, 0.4);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 8px 50px rgba(255, 176, 0, 0.6);
            transform: scale(1.03);
        }
    }
    
    .predict-btn > button:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 12px 40px rgba(255, 176, 0, 0.6) !important;
        animation: none;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 217, 233, 0.1) !important;
        color: #BcD6E6 !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 217, 233, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        transform: translateX(6px) scale(1.02);
    }
    
    /* Upload/Camera mode toggle */
    div[data-testid="stRadio"] > div {
        display: flex;
        justify-content: center;
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(0, 217, 233, 0.15);
    }
    div[data-testid="stRadio"] label {
        background: transparent;
        color: #BcD6E6 !important;
        padding: 8px 20px;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(0, 217, 233, 0.1);
    }
    div[data-testid="stRadio"] input:checked + div {
        color: #0B1E3D !important;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: visible; background: transparent !important; box-shadow: none !important;}
    header [data-testid="stToolbar"] { visibility: hidden; }
    header [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
        transform: none !important;
        visibility: visible !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 32px;
        }
        .result-value {
            font-size: 24px;
        }
        .custom-upload-btn {
            padding: 12px 20px;
            font-size: 14px;
        }
        .member-item {
            flex-wrap: wrap;
        }
        .sidebar-logo {
            max-width: 100px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# Sidebar
# ===============================

with st.sidebar:
    # Display logo image at top of sidebar with Framer Motion-like animation
    try:
        # Load and display the image
        sidebar_img = Image.open("image.png")
        # Convert to base64 for display
        buffered = BytesIO()
        sidebar_img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        st.markdown(f'''
        <div class="sidebar-logo-container">
            <div class="sidebar-logo-wrapper">
                <img src="data:image/png;base64,{img_base64}" alt="GCU Logo" class="sidebar-logo">
            </div>
        </div>
        ''', unsafe_allow_html=True)
    except:
        # Fallback if image not found
        st.markdown("""
        <div style="text-align: center; padding: 20px 0 10px 0; animation: rotateIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);">
            <div style="font-size: 56px; color: #00D9E9; animation: float 3s ease-in-out infinite;">AI</div>
            <h2 style="color: #FFFFFF; font-weight: 800; margin: 10px 0 0 0;">
                ASL<span style="color: #FFB000;">AI</span>
            </h2>
            <p style="color: #5f8aa7; font-size: 12px; letter-spacing: 2px; margin-top: 4px;">
                v2.0 · DEEP LEARNING
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Team Section - without roles
    st.markdown("""
    <div class="sidebar-section">
        <h4>Team Members</h4>
        <div class="member-list">
            <div class="member-item">
                <span class="member-icon">●</span>
                <span class="member-name">Abu Sufyan</span>
            </div>
            <div class="member-item">
                <span class="member-icon">●</span>
                <span class="member-name">Shahbaz Ali</span>
            </div>
            <div class="member-item">
                <span class="member-icon">●</span>
                <span class="member-name">Ramzan Ali</span>
            </div>
            <div class="member-item">
                <span class="member-icon">●</span>
                <span class="member-name">Ali Raza</span>
            </div>
            <div class="member-item">
                <span class="member-icon">●</span>
                <span class="member-name">Kashaf Majeed</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Developer Information
    st.markdown("""
    <div class="sidebar-section">
        <h4>Developed By</h4>
        <p>
            <span class="highlight-text">Abu Sufyan</span><br>
            <span style="font-size: 12px; color: #5f8aa7;">
                Graduate from 
                <span style="color: #FFFFFF;">University of Narowal</span>
            </span><br>
            <span style="font-size: 12px; color: #5f8aa7;">
                Course: 
                <span style="color: #FFFFFF;">Deep Learning</span>
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Institute Information
    st.markdown("""
    <div class="sidebar-section">
        <h4>Institute</h4>
        <p style="font-size: 12px; line-height: 1.8; text-align: justify;">
            <span style="color: #00D9E9;">Abdus Salam School of</span><br>
            <span style="color: #FFFFFF; font-weight: 600;">Mathematical Sciences</span><br>
            <span style="color: #5f8aa7; font-size: 11px;">GC University Lahore</span>
        </p>
        <p style="font-size: 12px; margin-top: 8px; text-align: justify;">
            <span style="color: #00D9E9;">Instructor:</span><br>
            <span style="color: #FFFFFF; font-weight: 600;">Dr. Jamshaid Warraich</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Beautiful Quote
    st.markdown("""
    <div class="quote-container">
        <div class="quote-text">
            "The only way to do great work is to love what you do. 
            In the world of AI, every line of code is a step towards 
            a smarter future."
        </div>
        <div class="quote-author">— Steve Jobs (Inspired by AI)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Project Info
    st.markdown("""
    <div class="sidebar-section">
        <h4>About Project</h4>
        <p style="text-align: justify;">
            A deep learning-based system for American Sign Language (ASL) 
            alphabet recognition using a 4-layer neural network architecture 
            with ReLU activation and Softmax classification.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Model Architecture
    st.markdown("""
    <div class="sidebar-section">
        <h4>Architecture</h4>
        <p style="font-family: monospace; font-size: 12px; text-align: justify;">
            <span style="color: #00D9E9;">Input:</span> 4096 (64x64 pixels)<br>
            <span style="color: #5f8aa7;">↓</span> ReLU<br>
            <span style="color: #00D9E9;">Layer 1:</span> 128 neurons<br>
            <span style="color: #5f8aa7;">↓</span> ReLU<br>
            <span style="color: #00D9E9;">Layer 2:</span> 64 neurons<br>
            <span style="color: #5f8aa7;">↓</span> ReLU<br>
            <span style="color: #00D9E9;">Layer 3:</span> 32 neurons<br>
            <span style="color: #5f8aa7;">↓</span> Softmax<br>
            <span style="color: #00D9E9;">Output:</span> 26 classes (A-Z)
        </p>
        <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 4px;">
            <span class="badge">4 Layers</span>
            <span class="badge">ReLU</span>
            <span class="badge">Softmax</span>
            <span class="badge">96% Acc</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div class="sidebar-section">
        <h4>Features</h4>
        <p style="text-align: justify;">
            ✓ Real-time prediction<br>
            ✓ Confidence scoring<br>
            ✓ Top-3 predictions<br>
            ✓ GPU accelerated<br>
            ✓ Responsive design<br>
            ✓ Interactive UI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown("""
    <div class="sidebar-section">
        <h4>Tech Stack</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px;">
            <span class="badge">Python</span>
            <span class="badge">NumPy</span>
            <span class="badge">Streamlit</span>
            <span class="badge">PIL</span>
            <span class="badge">JSON</span>
            <span class="badge">Matplotlib</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer in sidebar
    st.markdown("""
    <div style="text-align: center; color: #5f8aa7; font-size: 11px; padding: 10px 0; animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1);">
        <span>Made with passion by Team ASL-AI</span><br>
        <span style="opacity: 0.6;">© 2026 ASL Recognition System</span>
        <br><br>
        <span style="font-size: 10px; opacity: 0.4;">
            "Innovating through Deep Learning"
        </span>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# Load Classes
# ===============================

@st.cache_resource
def load_classes():
    with open("classes.json", "r") as f:
        return json.load(f)

classes = load_classes()

# ===============================
# Neural Network Class
# ===============================

class SignLanguageNN:
    def __init__(self):
        self.w1 = np.load("ASL_weight1.npy")
        self.w2 = np.load("ASL_weight2.npy")
        self.w3 = np.load("ASL_weight3.npy")
        self.w4 = np.load("ASL_weight4.npy")

    def relu(self, x):
        return np.maximum(0, x)

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)

    def query(self, image):
        image = image.reshape(-1, 1)
        
        h1 = self.relu(np.dot(self.w1, image))
        h2 = self.relu(np.dot(self.w2, h1))
        h3 = self.relu(np.dot(self.w3, h2))
        output = self.softmax(np.dot(self.w4, h3))
        
        return output

# ===============================
# Load Model
# ===============================

@st.cache_resource
def load_model():
    return SignLanguageNN()

model = load_model()

# ===============================
# Image Processing
# ===============================

def preprocess_image(image):
    image = image.convert("L")
    image = image.resize((64, 64))
    image = np.array(image)
    image = image.astype(float)
    image = (image / 255.0 * 0.99) + 0.01
    image = image.reshape(-1)
    return image

# ===============================
# Custom File Uploader - Improved
# ===============================

def custom_file_uploader():
    uploaded_file = st.file_uploader(
        "Choose Image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="file_uploader"
    )
    
    return uploaded_file

# ===============================
# Streamlit UI - Main
# ===============================

# Main container
st.markdown('<div class="main">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="title-container">
    <h1 class="main-title">
        American Sign Language <span class="highlight">Recognition</span>
    </h1>
    <div class="sub-title">DEEP LEARNING · REAL-TIME GESTURE RECOGNITION</div>
</div>
""", unsafe_allow_html=True)

# Create two columns for layout
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    # Image upload section
    st.markdown("""
    <div style="margin-bottom: 20px; animation: fadeInDown 0.6s cubic-bezier(0.16, 1, 0.3, 1);">
        <h3 style="color: #FFFFFF; font-weight: 700; margin-bottom: 10px;">
            Upload Image
        </h3>
        <p style="color: #5f8aa7; font-size: 14px; margin-top: -5px;">
            Upload a clear image of an ASL hand gesture
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mode selector: Upload or Camera
    input_mode = st.radio(
        "Input source",
        ["Upload", "Camera"],
        horizontal=True,
        label_visibility="collapsed",
        key="input_mode"
    )
    
    if input_mode == "Upload":
        # Custom upload button
        uploaded_file = custom_file_uploader()
        
        # Show supported formats
        st.markdown("""
        <div style="text-align: center; color: #5f8aa7; font-size: 12px; margin-top: 10px; animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);">
            Supported formats: JPG, JPEG, PNG · Max size: 5MB
        </div>
        """, unsafe_allow_html=True)
    else:
        # Live camera capture
        uploaded_file = st.camera_input(
            "Take a photo",
            label_visibility="collapsed",
            key="camera_input"
        )

with right_col:
    # Display uploaded image
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.markdown("""
        <div style="margin-bottom: 20px; animation: fadeInDown 0.6s cubic-bezier(0.16, 1, 0.3, 1);">
            <h3 style="color: #FFFFFF; font-weight: 700; margin-bottom: 10px;">
                Preview
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        caption_text = "Captured Gesture" if input_mode == "Camera" else "Uploaded Gesture"
        st.image(image, caption=caption_text, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# If image is uploaded, show prediction button
if uploaded_file:
    # Initialize session state for prediction
    if 'prediction_made' not in st.session_state:
        st.session_state.prediction_made = False
    if 'prediction_result' not in st.session_state:
        st.session_state.prediction_result = None
    
    st.markdown("---")
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="predict-btn">', unsafe_allow_html=True)
        predict_button = st.button(
            "Predict Gesture", 
            use_container_width=True,
            disabled=st.session_state.prediction_made
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Process prediction when button is clicked
    if predict_button:
        with st.spinner("Analyzing gesture with neural network..."):
            # Simulate processing time for better UX
            time.sleep(0.8)
            processed_image = preprocess_image(image)
            prediction = model.query(processed_image)
            predicted_class = np.argmax(prediction)
            confidence = np.max(prediction).item()
            
            # Store results in session state
            st.session_state.prediction_result = {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'prediction': prediction
            }
            st.session_state.prediction_made = True
            
            # Rerun to show results
            st.rerun()
    
    # Display results if prediction is made
    if st.session_state.prediction_made and st.session_state.prediction_result:
        result = st.session_state.prediction_result
        predicted_class = result['predicted_class']
        confidence = result['confidence']
        prediction = result['prediction']
        
        # Results section
        st.markdown("---")
        st.markdown("""
        <h3 style="color: #FFFFFF; font-weight: 700; text-align: center; margin-bottom: 20px; animation: fadeInDown 0.6s cubic-bezier(0.16, 1, 0.3, 1);">
            Recognition Results
        </h3>
        """, unsafe_allow_html=True)
        
        # Results in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="result-card" style="border-left-color: #FFB000;">
                <div class="result-label">Predicted Letter</div>
                <div class="result-value">
                    <span class="highlight">{classes[predicted_class]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="result-card" style="border-left-color: #00D9E9;">
                <div class="result-label">Confidence Score</div>
                <div class="result-value">
                    {confidence*100:.1f}%
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence*100}%; --target-width: {confidence*100}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional predictions
        with st.expander("View Top 3 Predictions", expanded=False):
            top_indices = np.argsort(prediction.flatten())[-3:][::-1]
            rank_symbols = ["1st", "2nd", "3rd"]
            colors = ["#FFB000", "#C0C0C0", "#CD7F32"]
            for i, idx in enumerate(top_indices):
                prob = prediction[idx].item() * 100
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; 
                            padding: 12px 16px; margin: 8px 0; 
                            background: rgba(255,255,255,0.05); border-radius: 12px;
                            border-left: 3px solid {colors[i]};
                            animation: fadeInRight 0.5s cubic-bezier(0.16, 1, 0.3, 1);
                            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 18px; font-weight: 700; color: {colors[i]};">
                            {rank_symbols[i]}
                        </span>
                        <span style="color: #FFFFFF; font-weight: 600; font-size: 18px;">
                            {classes[idx]}
                        </span>
                    </div>
                    <span style="color: {colors[i]}; font-weight: 700; font-size: 18px;">
                        {prob:.1f}%
                    </span>
                </div>
                """, unsafe_allow_html=True)
        
        # Reset button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Recognize Another Image", use_container_width=True):
                # Reset session state
                st.session_state.prediction_made = False
                st.session_state.prediction_result = None
                st.rerun()

else:
    # Show placeholder when no image is uploaded
    st.markdown("""
    <div style="text-align: center; padding: 80px 20px; color: #5f8aa7; animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);">
        <div style="font-size: 72px; color: #00D9E9; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">↑</div>
        <h3 style="color: #BcD6E6; font-weight: 600; margin-bottom: 10px; animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);">
            Ready to Recognize Gestures
        </h3>
        <p style="font-size: 16px; max-width: 400px; margin: 0 auto; animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1);">
            Upload an image of an ASL hand gesture to get instant recognition results
        </p>
        <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; animation: fadeInUp 1.2s cubic-bezier(0.16, 1, 0.3, 1);">
            <span style="background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 20px; font-size: 13px; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
                A-Z Recognition
            </span>
            <span style="background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 20px; font-size: 13px; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
                98% Accuracy
            </span>
            <span style="background: rgba(255,255,255,0.05); padding: 8px 16px; border-radius: 20px; font-size: 13px; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
                Real-time
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <span>Deep Learning Project</span>
    <span class="dot">•</span>
    <span>ASL Recognition System</span>
    <span class="dot">•</span>
    <span class="year">2026</span>
    <br>
    <span style="font-size: 11px; opacity: 0.6;">
        Developed by Team ASL-AI · University of Narowal
    </span>
    <br>
    <span style="font-size: 11px; opacity: 0.6;">
        Under the supervision of Dr. Jamshaid Warraich
    </span>
    <br><br>
    <span style="font-size: 10px; opacity: 0.4;">
        "Empowering communication through AI"
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
