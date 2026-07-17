# PROP_ENGINE.ai 🏠 

An end-to-end Full-Stack Machine Learning application designed to predict real estate housing prices in Bengaluru. The system utilizes a trained Linear Regression model to provide instant valuation estimates based on historical house data vectors.

---

## 🚀 Key Features
- **Predictive ML Engine:** Trained on Bengaluru real estate data vectors to estimate market prices accurately.
- **Premium User Dashboard:** A modern, high-end SaaS dark-mode interface built with React and Tailwind CSS v4.
- **Dynamic Neighborhood Mapping:** Fetches active locations dynamically from the Flask server backend API.
- **Responsive Geometry Layout:** Fully reactive grids to update BHK layouts, square footage sizing, and bathroom dimensions instantly.

---

## 🛠️ Tech Stack & Architecture

### Frontend Layer
- **React.js & Vite:** Fast build toolchain for modern single-page applications.
- **Tailwind CSS v4:** Zero-config native compilation architecture for sleek, glassmorphic dark UIs.

### Backend & Core ML Pipeline
- **Python Flask:** Lightweight backend microservice routing predictions and structural metadata.
- **Flask-CORS:** Configured cross-origin mechanics for secure internal communication blocks.
- **Pandas & NumPy:** In-memory dataset cleanup, transformation pipelines, and matrix calculations.
- **Scikit-Learn:** Core framework implementing the Linear Regression mathematical models.

---

## 📁 Project Directory Structure

```text
House_Price_Project/
│
├── backend/                   # Python Flask & Machine Learning Pipeline
│   ├── dataset/               # Contains historical Bangalore property CSV data
│   ├── main.py                # Server execution scripts and API gateway routes
│   ├── predict.py             # Data cleaning logic and ML model training sequences
│   └── requirements.txt       # Global Python packages and dependency map
│
└── frontend/                  # React + Vite Production Build
    ├── src/
    │   ├── App.jsx            # Main premium dashboard page layout and styling
    │   ├── index.css          # Tailwind CSS v4 directive entry line
    │   └── main.jsx           # Core DOM renderer configuration
    ├── vite.config.js         # Tailwind Vite plugin hooks configuration
    └── package.json           # Frontend dependency setup
```
#Local Installation & Execution
cd backend
pip install -r requirements.txt
python main.py

#Boot Up the React App Frontend
cd frontend
npm install
npm run dev
