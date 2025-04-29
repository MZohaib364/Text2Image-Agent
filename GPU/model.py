from diffusers import StableDiffusionPipeline
import torch

# Check if CUDA is available and set the device
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

# Load the Stable Diffusion v1.5 model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=dtype,
    use_safetensors=True,  # safer and faster format if available
)

# Move the pipeline to the selected device
pipe = pipe.to(device)

# Enable memory optimizations
pipe.enable_attention_slicing()           # Reduce memory usage
pipe.enable_vae_slicing()                 # Reduce VAE memory footprint (especially useful for low VRAM GPUs)

# Optional: if your VRAM is still close to full, enable CPU offload
# pipe.enable_model_cpu_offload()

# Generate image
prompt = "A highly realistic photo of a handsome young man standing on a mountain in golden hour lighting."
image = pipe(prompt).images[0]

# Save the image
image.save("realistic_man_mountain.png")
print("Image generated and saved as realistic_man_mountain.png")
