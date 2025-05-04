import grpc
from concurrent import futures
import time
import os
import base64
from io import BytesIO

import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

import text2image_pb2
import text2image_pb2_grpc

# Load model on GPU
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

pipe = pipe.to("cuda")
pipe.enable_attention_slicing()

class Text2ImageServicer(text2image_pb2_grpc.Text2ImageServiceServicer):
    def GenerateImage(self, request, context):
        prompt = f"{request.context.strip()}: {request.text.strip()}"
        
        try:
            # Generate the image
            image = pipe(prompt).images[0]

            # Create the folder to save images if it doesn't exist
            output_folder = "generated_images"
            os.makedirs(output_folder, exist_ok=True)

            # Define the filename and save the image
            image_filename = f"{int(time.time())}.png"  # Unique filename based on timestamp
            image_path = os.path.join(output_folder, image_filename)

            image.save(image_path)  # Save the image

            # Convert image to base64 string
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()

            # Return the image path and base64 string in the response
            return text2image_pb2.ImageResponse(
                status_code=200,
                message="Image generated and saved successfully.",
                image_base64=img_str,
                image_path=image_path  # Include the image path in the response
            )

        except Exception as e:
            return text2image_pb2.ImageResponse(
                status_code=500,
                message=f"Failed to generate image: {str(e)}",
                image_base64="",
                image_path=""  # Return empty path if generation fails
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    text2image_pb2_grpc.add_Text2ImageServiceServicer_to_server(Text2ImageServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
    