import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(
    page_title="Virtual Try-On Diffusion (VTON-D)",
    page_icon="👗",
    layout="centered"
)

st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        color: #2E4053;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #5D6D7E;
        margin-bottom: 2rem;
    }
    .upload-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .stButton button {
        background: linear-gradient(to right, #7b2ff7, #f107a3);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1.1rem;
        padding: 0.6rem 1.2rem;
        transition: 0.3s;
    }
    .stButton button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #f107a3, #7b2ff7);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>👗 Virtual Try-On Diffusion (VTON-D)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>AI-powered clothing try-on using diffusion models (via RapidAPI)</div>", unsafe_allow_html=True)

st.sidebar.title("About the App")
st.sidebar.info(
    """
    This app uses the **Virtual Try-On Diffusion (VTON-D)** model from Hugging Face,
    accessed via **RapidAPI**.  
    Upload a **person image** and a **clothing image**, then click **Generate Try-On**.
    """
)
st.sidebar.markdown("**API Plan:** Free (100 requests/month) via RapidAPI")

st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
st.subheader("1️⃣ Upload Input Images")

col1, col2 = st.columns(2)
with col1:
    person_img = st.file_uploader("Person Image", type=["jpg", "jpeg", "png"])
    if person_img:
        st.image(person_img, caption="Person Image", use_container_width=True)
with col2:
    cloth_img = st.file_uploader("Clothing Image", type=["jpg", "jpeg", "png"])
    if cloth_img:
        st.image(cloth_img, caption="Clothing Image", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
st.subheader("2️⃣ API Configuration")
st.write("Using API key placeholder `xxxxx` — replace with your own from RapidAPI.")
api_key = "xxxxx"
st.markdown("</div>", unsafe_allow_html=True)

if st.button("🚀 Generate Try-On"):
    if not (person_img and cloth_img):
        st.error("⚠️ Please upload both images before generating.")
    else:
        with st.spinner("Generating your virtual try-on... please wait ⏳"):
            url = "https://virtual-try-on-diffusion-vton-d.p.rapidapi.com/tryon"
            files = {
                "person": person_img.getvalue(),
                "cloth": cloth_img.getvalue(),
            }
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "virtual-try-on-diffusion-vton-d.p.rapidapi.com",
            }
            try:
                response = requests.post(url, headers=headers, files=files)
                if response.status_code == 200:
                    result_img = Image.open(io.BytesIO(response.content))
                    st.success("✅ Virtual Try-On generated successfully!")
                    st.image(result_img, caption="AI Try-On Result", use_container_width=True)
                else:
                    st.error(f"❌ API request failed ({response.status_code}) — {response.text}")
            except Exception as e:
                st.error(f"Error contacting API: {e}")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.9rem;'>"
    "Powered by <b>Virtual Try-On Diffusion (VTON-D)</b> • Hugging Face x RapidAPI"
    "</div>",
    unsafe_allow_html=True
)
