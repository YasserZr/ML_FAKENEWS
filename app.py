from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS library
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes by default

# Load the vectorizer and model
model_file = "linearsvc.pkl"
if os.path.exists(model_file):
    vectorizer, model = joblib.load(model_file)
else:
    raise FileNotFoundError(f"Model file {model_file} not found.")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the text input from the request
        data = request.json
        text = data.get("text", "")
        
        if not text:
            return jsonify({"error": "No text provided for prediction."}), 400
        
        # Transform the text and predict
        vectorized_text = vectorizer.transform([text])
        prediction = model.predict(vectorized_text)[0]
        label = "FAKE" if prediction == 1 else "REAL"
        
        return jsonify({"prediction": label})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
