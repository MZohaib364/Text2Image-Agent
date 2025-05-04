# 🖼️ Text2Image Agent

A GPU-accelerated, Dockerized application that enables **text-to-image generation** using state-of-the-art **Stable Diffusion models** from Hugging Face. The system provides both a **Flask REST API** and a **Streamlit-based web interface** for seamless user interaction.

---

## 🚀 Features

- 🔡 Accepts text prompts and generates high-quality images  
- ⚙️ Backend built with **Flask** for API-based access  
- 🌐 Frontend built with **Streamlit** for live interaction  
- 🧠 Utilizes Hugging Face's `diffusers` + `transformers`  
- ⚡ GPU acceleration with CUDA support (via PyTorch)  
- 📦 Containerized with Docker for easy deployment  

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Text2Image-Agent.git
cd Text2Image-Agent/GPU
```

### 2. Build the Docker Image (GPU support)
Ensure Docker is running with Linux containers and NVIDIA GPU support:
```bash
docker build -t text2image-app .
```

🔧 If you get image not found errors, use a verified PyTorch CUDA image:
```dockerfile
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
```

### 3. Run the Container
```bash
docker run --gpus all -p 8000:8000 -p 8501:8501 -it text2image-app
```

### 4. Access the App
- Streamlit UI: http://localhost:8501
- Flask REST API: http://localhost:8000/generate

---

## 💡 Usage

### Option 1: Using the Streamlit Interface
1. Open http://localhost:8501 in your browser
2. Enter a text prompt (e.g., "A futuristic city at night")
3. Click Generate Image
4. View or download the result

### Option 2: Using the REST API
POST /generate
```bash
curl -X POST http://localhost:8000/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "a sunset over a mountain range"}'
```

Response:
- Returns base64-encoded image string or saves to disk (depending on implementation)

---

## 🧱 System Architecture

```
┌────────────┐        ┌────────────┐        ┌────────────────────────┐
│   Streamlit│◀──────▶│   Flask API│◀──────▶│ Hugging Face + PyTorch │
└────────────┘        └────────────┘        └────────────────────────┘
     ▲                    ▲
     │                    │
     ▼                    ▼
 Web Browser         Dockerized GPU
```

- Frontend: Streamlit
- Backend: Flask
- Model Source: diffusers.StableDiffusionPipeline
- Inference: PyTorch + CUDA

---

## 📦 Model Source

The app uses:
- StableDiffusionPipeline from 🤗 Diffusers
- transformers for CLIP tokenizer/model
- Optional scheduler: DPMSolverMultistepScheduler

Make sure your server.py includes:
```python
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
```

---

## ⚠️ Known Limitations

- ❗ Not suitable for production: Flask/Streamlit are dev servers
- 🧠 Memory intensive: Requires >= 6 GB VRAM for SD 1.5
- 🔒 No user authentication or rate limiting
- 🌐 No image caching (each prompt triggers inference)
- 📉 Cold start time when loading large models in container

---

## 🔧 Troubleshooting

**Problem**: module 'torch' has no attribute 'compiler'  
**Cause**: You're using a newer version of transformers with an older torch.  
**Fix**: Downgrade transformers or upgrade PyTorch to 2.1+.

```bash
pip install torch==2.1.0 transformers==4.36.2 diffusers==0.25.0
```