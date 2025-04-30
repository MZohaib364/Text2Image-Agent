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
    context = data.get("context", "")
    text = data.get("text", "")

    if not context or not text:
        return jsonify({"error": "Both 'context' and 'text' are required"}), 400

    grpc_request = text2image_pb2.ImageRequest(context=context, text=text)
    grpc_response = stub.GenerateImage(grpc_request)

    return jsonify({
        "image_base64": grpc_response.image_base64,
        "message": grpc_response.message,
        "status_code": grpc_response.status_code
    }), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)
