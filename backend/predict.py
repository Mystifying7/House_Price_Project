import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Helper function to convert total_sqft into proper float numbers
def convert_sqft_to_num(x):
    if isinstance(x, str):
        tokens = x.split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(x)
    except:
        return None

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    
    # 1. Kachra columns safely remove karo (agar honge toh remove honge, warna ignore)
    df2 = df.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns', errors='ignore')
    
    # 2. Missing values hatao
    df3 = df2.dropna()
    
    # 3. BHK logic ko safely handle karo aur purana text wala 'size' delete karo
    if 'size' in df3.columns:
        df3['bhk'] = df3['size'].apply(lambda x: int(str(x).split(' ')[0]))
        # 🚨 FIX: Purana text wala column delete karo taaki ML model crash na ho
        df3 = df3.drop('size', axis='columns')
        
    # 4. Handle range strings in 'total_sqft'
    df4 = df3.copy()
    df4['total_sqft'] = df4['total_sqft'].apply(convert_sqft_to_num)
    
    # 5. Drop any nulls created during sqft conversion
    df5 = df4.dropna()
    
    # 6. Remove outliers (Any property offering less than 300 sqft per bedroom is likely noise)
    df6 = df5[~(df5.total_sqft / df5.bhk < 300)]
    
    # 7. Handle high-cardinality text column 'location'
    location_stats = df6['location'].value_counts(ascending=False)
    location_stats_less_than_10 = location_stats[location_stats <= 10]
    df6['location'] = df6['location'].apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
    
    # 8. One-Hot Encoding (Safely drop 'other' if it exists)
    dummies = pd.get_dummies(df6.location).astype(int)
    df7 = pd.concat([df6, dummies.drop('other', axis='columns', errors='ignore')], axis='columns')
    df8 = df7.drop('location', axis='columns')
    
    print("✅ Data cleaning and preprocessing complete!")
    return df8

def train_ml_model(data):
    print("⚙️ Splitting data and training model...")
    # Separate independent variables (X) from target price (y)
    X = data.drop(['price'], axis='columns')
    y = data.price
    
    # 80% Training set to learn, 20% Testing set to validate evaluation accuracy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    
    # Train the standard Linear Regression model architecture
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Calculate model precision coefficient matrix accuracy
    accuracy = model.score(X_test, y_test)
    print(f"🎯 Model Accuracy (R² Score): {accuracy * 100:.2f}%")
    return model