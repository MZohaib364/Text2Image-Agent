import grpc
from concurrent import futures
import time
import requests

import text2image_pb2
import text2image_pb2_grpc

import os
from dotenv import load_dotenv

load_dotenv()

# Access the token
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

class Text2ImageServicer(text2image_pb2_grpc.Text2ImageServiceServicer):
        def GenerateImage(self, request, context):
                prompt = request.prompt
                response = requests.post(API_URL, headers=headers, json={"inputs":prompt})
                if response.status_code != 200:
                    context.set_details('Failed tp generate image from model')
                    context.set_code(grpc.StatusCode.INTERNAL)
                    return text2image_pb2.Text2ImageResponse(status="error", file="")
                
                file_path = "generated.png"
                with open(file_path, 'wb') as f:
                       f.write(response.content)



                return text2image_pb2.Text2ImageResponse(status="success", file=file_path)
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text2image_pb2_grpc.add_Text2ImageServiceServicer_to_server(Text2ImageServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
