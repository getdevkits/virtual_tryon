import streamlit as st
import http.client
import io
from PIL import Image

st.set_page_config(page_title="Try-On Diffusion", page_icon="🪞", layout="centered")
st.title("👗 AI Virtual Try-On Diffusion")
st.caption("Powered by RapidAPI — try-on-diffusion.p.rapidapi.com")

# Upload Section
col1, col2 = st.columns(2)

with col1:
    person_img = st.file_uploader("Upload Person Image", type=["jpg", "jpeg", "png"])
    if person_img:
        st.image(person_img, caption="Person Image", use_container_width=True)

with col2:
    cloth_img = st.file_uploader("Upload Clothing Image", type=["jpg", "jpeg", "png"])
    if cloth_img:
        st.image(cloth_img, caption="Clothing Image", use_container_width=True)

api_key = "2010bd9dd3mshe6feef1665eab1dp175d30jsn16f04b5bb10b"  # dummy key placeholder

if st.button("🚀 Generate Try-On"):
    if not person_img or not cloth_img:
        st.error("Please upload both images.")
    else:
        st.info("Sending request to Try-On Diffusion API...")
        try:
            # Prepare images as binary data
            person_bytes = person_img.getvalue()
            cloth_bytes = cloth_img.getvalue()

            # Initialize connection
            conn = http.client.HTTPSConnection("try-on-diffusion.p.rapidapi.com")

            # ⚠️ NOTE: This specific endpoint might require multipart/form-data payload.
            # So we’ll manually build it.
            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            payload = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="person"; filename="person.jpg"\r\n'
                f"Content-Type: image/jpeg\r\n\r\n"
            ).encode() + person_bytes + (
                f"\r\n--{boundary}\r\n"
                f'Content-Disposition: form-data; name="cloth"; filename="cloth.jpg"\r\n'
                f"Content-Type: image/jpeg\r\n\r\n"
            ).encode() + cloth_bytes + f"\r\n--{boundary}--".encode()

            headers = {
                "x-rapidapi-key": api_key,
                "x-rapidapi-host": "try-on-diffusion.p.rapidapi.com",
                "content-type": f"multipart/form-data; boundary={boundary}",
            }

            conn.request("POST", "/try-on-file", body=payload, headers=headers)
            res = conn.getresponse()
            data = res.read()

            if res.status == 200:
                try:
                    result_img = Image.open(io.BytesIO(data))
                    st.success("✅ Virtual Try-On generated successfully!")
                    st.image(result_img, caption="AI Try-On Result", use_container_width=True)
                except Exception:
                    st.write("Response:", data.decode("utf-8"))
            else:
                st.error(f"API Error: {res.status}")
                st.text(data.decode("utf-8"))

            conn.close()

        except Exception as e:
            st.error(f"Error contacting API: {e}")
