import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def load_and_clean_data(filepath):
    print("⏳ Loading dataset...")
    df = pd.read_csv(filepath)
    
    # 1. Drop non-critical columns that aren't useful for linear regression pricing
    df2 = df.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')
    df3 = df2.dropna()
    
    # 2. Clean 'size' column to a clean numeric 'bhk' column
    df3['bhk'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))
    df4 = df3.drop(['size'], axis='columns')
    
    # 3. Handle range strings in 'total_sqft' (e.g., '1100 - 1300' becomes 1200)
    def convert_sqft_to_num(x):
        tokens = x.split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        try:
            return float(x)
        except:
            return None

    df5 = df4.copy()
    df5['total_sqft'] = df5['total_sqft'].apply(convert_sqft_to_num)
    df5 = df5.dropna()
    
    # 4. Remove outliers (Any property offering less than 300 sqft per bedroom is likely abnormal/noise)
    df6 = df5[~(df5.total_sqft / df5.bhk < 300)]
    
    # 5. Handle high-cardinality text column 'location'
    # If a location appears 10 or fewer times, group it under 'other' to prevent overfitting
    location_stats = df6['location'].value_counts(ascending=False)
    location_stats_less_than_10 = location_stats[location_stats <= 10]
    df6['location'] = df6['location'].apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
    
    # 6. One-Hot Encoding: Convert text location names into binary (0 or 1) numeric feature vectors
    dummies = pd.get_dummies(df6.location).astype(int)
    df7 = pd.concat([df6, dummies.drop('other', axis='columns')], axis='columns')
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