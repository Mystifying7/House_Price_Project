from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
from predict import load_and_clean_data, train_ml_model

app = Flask(__name__)
CORS(app) # Enable CORS so React can access this API

# Global dictionaries to hold models and metadata for multiple cities
models = {}
feature_columns_dict = {}
locations_dict = {}

def initialize_backend():
    global models, feature_columns_dict, locations_dict
    
    # Map cities to their respective CSV files
    datasets = {
        "bangalore": "bangalore_house_data.csv",
        "mumbai": "mumbai_house_data.csv"
    }
    
    for city, filename in datasets.items():
        csv_path = f"./dataset/{filename}"
        # Fallback for render root paths
        if not os.path.exists(csv_path) and os.path.exists(f"backend/dataset/{filename}"):
            csv_path = f"backend/dataset/{filename}"
            
        if os.path.exists(csv_path):
            print(f"⏳ Training ML model for {city.upper()}...")
            data = load_and_clean_data(csv_path)
            
            feature_columns = [col for col in data.columns if col != 'price']
            locations = sorted([col for col in feature_columns if col not in ['total_sqft', 'bath', 'bhk']])
            
            models[city] = train_ml_model(data)
            feature_columns_dict[city] = feature_columns
            locations_dict[city] = locations
            
    print("🚀 All City ML Models and APIs Ready!")

# Initialize the pipeline immediately before starting the server
initialize_backend()

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    # Return available cities and their respective locations
    return jsonify({
        "cities": list(locations_dict.keys()),
        "locations_map": locations_dict
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        city = data.get('city', 'bangalore') # Default to bangalore if not provided
        total_sqft = float(data['total_sqft'])
        bath = int(data['bath'])
        bhk = int(data['bhk'])
        selected_location = data['location']
        
        if city not in models:
            return jsonify({"error": "City model not found or dataset missing"}), 400
            
        # Fetch the specific model and features for the requested city
        feature_columns = feature_columns_dict[city]
        model = models[city]
        
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)