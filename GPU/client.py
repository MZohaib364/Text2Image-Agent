import grpc
import text2image_pb2
import text2image_pb2_grpc

def run():
    # Connect to server (default port 50051)
    channel = grpc.insecure_channel('localhost:50051')
    stub = text2image_pb2_grpc.Text2ImageServiceStub(channel)

    # Define your image generation prompt
    prompt = "A realistic futuristic city skyline at sunset"

    # Make request
    request = text2image_pb2.ImageRequest(prompt=prompt)
    response = stub.GenerateImage(request)

    # Handle response
    print("Image generated at path:", response.image_path)

if __name__ == '__main__':
    run()
