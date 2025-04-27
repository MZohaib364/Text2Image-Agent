from diffusers import StableDiffusionPipeline
import torch

# Load Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1-base",
    use_safetensors=False,
)

# Force CPU usage
pipe = pipe.to("cpu")

# Enable attention slicing for lower RAM usage and faster inference on CPU
pipe.enable_attention_slicing()

# Generate image
prompt = "A handsome young man on a mountain."
image = pipe(prompt).images[0]

# Save image
image.save("locally_generated.png")

print("Image generated and saved as fantasy_landscape.png")
