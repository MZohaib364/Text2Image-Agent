import streamlit as st
import requests
from PIL import Image
import io
import base64

st.set_page_config(page_title="Text2Image Generator", layout="centered")
st.title("🧙‍♂️ Text2Image Generator")
st.markdown("Enter your prompt and generate an AI-powered image.")

# Input field
prompt = st.text_area("Prompt", "a wizard casting fire in the sky")

if st.button("Generate Image"):
    with st.spinner("Generating..."):
        response = requests.post(
            "http://localhost:8000/generate",
            json={"prompt": prompt},
        )
        if response.status_code == 200:
            data = response.json()
            image_base64 = data["image_base64"]
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.error("Failed to generate image. Server error or invalid input.")
