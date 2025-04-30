from flask import Flask, request, jsonify
import grpc
import text2image_pb2
import text2image_pb2_grpc

app = Flask(__name__)

# Connect to the gRPC server
channel = grpc.insecure_channel('localhost:50051')
stub = text2image_pb2_grpc.Text2ImageServiceStub(channel)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    grpc_request = text2image_pb2.ImageRequest(prompt=prompt)
    grpc_response = stub.GenerateImage(grpc_request)

    # Return both image_path and base64 image in the response
    return jsonify({
        "image_base64": grpc_response.image_base64,
        "image_path": grpc_response.image_path,  # Include the image path here
        "status": "success"
    }), 200


if __name__ == '__main__':
    app.run(port=8000, debug=True)
