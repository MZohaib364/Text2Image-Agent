import streamlit as st
import grpc
import text2image_pb2
import text2image_pb2_grpc
from PIL import Image
import base64
import io

st.set_page_config(page_title="Text2Image Generator", layout="centered")
st.title("🧙‍♂️ Text2Image Generator")
st.markdown("Enter your prompt and generate an AI-powered image.")

# Set up gRPC client
channel = grpc.insecure_channel('localhost:50051')
stub = text2image_pb2_grpc.Text2ImageServiceStub(channel)

# Input field
prompt = st.text_area("Prompt", "a wizard casting fire in the sky")

if st.button("Generate Image"):
    with st.spinner("Generating..."):
        context = "fantasy art"  # or let user select from dropdown
        request = text2image_pb2.ImageRequest(context=context, text=prompt)
        
        try:
            response = stub.GenerateImage(request)
            image_base64 = response.image_base64
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption="Generated Image", use_column_width=True)
        except grpc.RpcError as e:
            st.error(f"gRPC Error: {e.details()}")
