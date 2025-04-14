import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import uuid
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.preprocessing import image
from PIL import Image
from models.predict import SkinCancerPredictor


# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Initialize Flask app
app = Flask(__name__)

CORS(app)   # Enable CORS for all routes
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load the pre-trained model for skin cancer detection 
predictor = SkinCancerPredictor(model_path="./models/skin_cancer_model.keras")

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Route for the home page
@app.route("/")
def home():
    return jsonify({"message": "Skin Cancer Detection API is running!"})

# Route for image prediction
@app.route("/predict", methods=["POST"])
def predict():
    # Check if the post request contains an image file
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        file.save(filepath)


        try:
            result = predictor.predict(filepath) # Predict the image using the loaded model
            os.remove(filepath) # Remove the file after prediction to save space
            return jsonify(result)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    else:
        return jsonify({"error": "File type not allowed"}), 400


# if __name__ == "__main__":
#     app.run(debug=True)
