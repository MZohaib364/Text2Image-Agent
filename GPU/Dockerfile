# Use CUDA-enabled PyTorch base image for GPU inference
FROM pytorch/pytorch:latest


# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

# Copy all source files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose ports
EXPOSE 50051 8000 8501

# Start all components using a bash script
CMD ["bash", "-c", "\
    python3 server.py & \
    python3 rest_api.py & \
    streamlit run FrontEnd/streamlit_app.py --server.port 8501"]
