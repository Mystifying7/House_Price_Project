import subprocess
import sys

# Script run hote hi sabse pehle automatically background mein libraries install ho jayengi
try:
    import flask
    import flask_cors
    import pandas
    import numpy
    import sklearn
except ImportError:
    print("⏳ Auto-installing missing dependencies on Render...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# ==========================================
# AAPKA ORIGINAL CODE AB YAHA SE START HOGA:
# ==========================================
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from predict import load_and_clean_data, train_ml_model

app = Flask(__name__)
CORS(app) # Enable CORS so React can access this API

# Global variables to hold our model metadata
model = None
feature_columns = []
locations = []

def initialize_backend():
    global model, feature_columns, locations
    csv_path = "./dataset/bangalore_house_data.csv"
    data = load_and_clean_data(csv_path)
    
    # Extract feature column names expected by the ML model
    feature_columns = [col for col in data.columns if col != 'price']
    
    # Extract only the location text columns for the dropdown selection array
    locations = sorted([col for col in feature_columns if col not in ['total_sqft', 'bath', 'bhk']])
    
    model = train_ml_model(data)
    print("🚀 ML Model and API Ready!")

# Initialize the pipeline immediately before starting the server
initialize_backend()

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    # Sends the list of locations to React so it can populate the dropdown menu dynamically
    return jsonify({"locations": locations})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        total_sqft = float(data['total_sqft'])
        bath = int(data['bath'])
        bhk = int(data['bhk'])
        selected_location = data['location']
        
        # Construct the feature vector
        input_vector = np.zeros(len(feature_columns))
        input_vector[feature_columns.index('total_sqft')] = total_sqft
        input_vector[feature_columns.index('bath')] = bath
        input_vector[feature_columns.index('bhk')] = bhk
        
        if selected_location in feature_columns:
            location_index = feature_columns.index(selected_location)
            input_vector[location_index] = 1
            
        predicted_price = model.predict([input_vector])[0]
        
        return jsonify({"predicted_price": round(max(0, predicted_price), 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    import os
    # Render assigns a dynamic port automatically, fallback to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)