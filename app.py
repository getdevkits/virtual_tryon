import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Virtual Try-On Diffusion", page_icon="🪞", layout="centered")

st.title("👗 Virtual Try-On Diffusion (VTON-D)")
st.caption("AI-powered virtual clothing try-on using Hugging Face (via RapidAPI)")

# Sidebar info
st.sidebar.header("About")
st.sidebar.write("Upload a person image and a clothing image. Then generate a virtual try-on preview.")
st.sidebar.write("Free plan: 100 API requests/month via RapidAPI.")

# Upload columns
col1, col2 = st.columns(2)
with col1:
    person_img = st.file_uploader("Upload Person Image", type=["jpg", "jpeg", "png"])
    if person_img is not None:
        try:
            person_preview = Image.open(io.BytesIO(person_img.getvalue())).convert("RGB")
            st.image(person_preview, caption="Person", use_container_width=True)
        except Exception:
            st.warning("Couldn't preview this image, please upload a valid JPG/PNG.")

with col2:
    cloth_img = st.file_uploader("Upload Clothing Image", type=["jpg", "jpeg", "png"])
    if cloth_img is not None:
        try:
            cloth_preview = Image.open(io.BytesIO(cloth_img.getvalue())).convert("RGB")
            st.image(cloth_preview, caption="Clothing", use_container_width=True)
        except Exception:
            st.warning("Couldn't preview this image, please upload a valid JPG/PNG.")

st.markdown("---")

api_key = "2010bd9dd3mshe6feef1665eab1dp175d30jsn16f04b5bb10b"

if st.button("🚀 Generate Try-On"):
    if not person_img or not cloth_img:
        st.error("Please upload both person and clothing images.")
    else:
        with st.spinner("Generating your virtual try-on... please wait ⏳"):
            try:
                url = "https://virtual-try-on-diffusion-vton-d.p.rapidapi.com/tryon"
                headers = {
                    "X-RapidAPI-Key": api_key,
                    "X-RapidAPI-Host": "virtual-try-on-diffusion-vton-d.p.rapidapi.com"
                }
                files = {
                    "person": ("person.jpg", person_img.getvalue(), "image/jpeg"),
                    "cloth": ("cloth.jpg", cloth_img.getvalue(), "image/jpeg")
                }
                resp = requests.post(url, headers=headers, files=files)
                if resp.status_code == 200:
                    tryon_img = Image.open(io.BytesIO(resp.content))
                    st.success("✅ Virtual Try-On Generated Successfully!")
                    st.image(tryon_img, caption="AI Try-On Result", use_container_width=True)
                else:
                    st.error(f"❌ API returned {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by Virtual Try-On Diffusion • Hugging Face x RapidAPI")
