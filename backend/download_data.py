import os
import random
import pandas as pd

def generate_mumbai_dataset():
    target_dir = "./dataset"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    target_path = os.path.join(target_dir, "mumbai_house_data.csv")
    print("⏳ Generating local MUMBAI raw dataset vectors...")
    
    # Standard Mumbai major neighborhood list
    locations = [
        "Andheri West", "Andheri East", "Bandra West", "Borivali West", 
        "Kandivali East", "Malad West", "Powai", "Thane West", 
        "Dadar West", "Juhu", "Goregaon East", "Chembur"
    ]
    
    data = []
    
    # Generate 1000 structured rows matching standard real estate limits
    for _ in range(1000):
        loc = random.choice(locations)
        bhk = random.choice([1, 2, 3, 4])
        
        # Approximate standard square footage per BHK range
        if bhk == 1:
            sqft = random.randint(400, 650)
            bath = 1
        elif bhk == 2:
            sqft = random.randint(700, 1050)
            bath = 2
        elif bhk == 3:
            sqft = random.randint(1100, 1550)
            bath = random.choice([2, 3])
        else:
            sqft = random.randint(1600, 2500)
            bath = random.choice([3, 4])
            
        # Base multiplier logic for Mumbai prices (in Lakhs)
        base_rate = 22000 if "Bandra" in loc or "Juhu" in loc else 15000 if "Powai" in loc else 11000
        price = round((sqft * base_rate / 100000) * random.uniform(0.9, 1.1), 2)
        
        data.append([loc, sqft, bath, bhk, price])
        
    df = pd.DataFrame(data, columns=['location', 'total_sqft', 'bath', 'bhk', 'price'])
    df.to_csv(target_path, index=False)
    print(f"🚀 Success! Clean Mumbai dataset saved locally at: {target_path}")

if __name__ == "__main__":
    generate_mumbai_dataset()