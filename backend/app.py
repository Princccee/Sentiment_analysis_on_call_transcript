from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads' # to handle the uploaded files on streamlit app on the server side
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load pre-trained sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# --- Flask API Endpoints ---
# Define the upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

# --------------------------------------------------
# Define the analyze endpoint
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    # Expect a JSON payload with the file path
    data = request.json
    file_path = data.get('file_path')

    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'Invalid file path'}), 400

    # Read the file content
    with open(file_path, 'r') as f:
        text = f.read()
    
    # Perform sentiment analysis
    result = sentiment_analyzer(text)
    
    return jsonify({'sentiment': result}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)