from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=dtype,
    use_safetensors=True
)

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to(device)

pipe.enable_attention_slicing()
pipe.enable_vae_slicing()
# pipe.enable_model_cpu_offload()  # Optional for low VRAM

prompt = "A highly realistic photo of a handsome young man standing on a mountain in golden hour lighting."
image = pipe(prompt, height=384, width=384, num_inference_steps=25).images[0]

image.save("realistic_man_mountain.png")
print("Image generated and saved.")
