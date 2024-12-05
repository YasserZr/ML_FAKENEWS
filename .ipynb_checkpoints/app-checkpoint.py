from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input data from the request
        data = request.json
        features = np.array(data['features']).reshape(1, -1)

        # Make predictions
        prediction = model.predict(features)
        return jsonify({'prediction': prediction.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return "Model API is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
