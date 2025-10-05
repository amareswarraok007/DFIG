# DFIG - Crop Prediction System

A machine learning-based crop prediction system with both Python FastAPI and Node.js backends.

## Project Structure

```
DFIG/
├── Agri.xlsx                 # Dataset
├── scripts/
│   ├── s.py                  # Data exploration script
│   └── train_and_save.py     # Model training script
├── predict_service/          # Python FastAPI service
│   ├── app.py               # FastAPI application
│   ├── test_predict.py      # Test script
│   └── requirements.txt     # Python dependencies
├── backend/                 # Node.js service
│   ├── index.js
│   ├── package.json
│   ├── Dockerfile
│   ├── routes/
│   └── validators/
└── model/                   # Trained model files
    ├── pipeline.pkl
    └── expected_columns.txt
```

## Features

- **N, P, K**: Nitrogen, Phosphorus, Potassium levels
- **Temperature**: Temperature in Celsius
- **Humidity**: Relative humidity percentage
- **pH**: Soil pH level
- **Rainfall**: Rainfall in mm

## Setup

### Python Service (FastAPI)

1. Navigate to predict_service directory:
   ```bash
   cd predict_service
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Train the model:
   ```bash
   cd ..
   python scripts/train_and_save.py
   ```

5. Start the service:
   ```bash
   cd predict_service
   export MODEL_PATH=$(pwd)/../model/pipeline.pkl
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

### Node.js Service

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the service:
   ```bash
   npm start
   ```

## API Usage

### Python Service (Port 8000)

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "N": 90,
       "P": 42,
       "K": 43,
       "temperature": 20.88,
       "humidity": 82.0,
       "ph": 6.5,
       "rainfall": 202.9
     }'
```

### Node.js Service (Port 3000)

```bash
curl -X POST "http://localhost:3000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "N": 90,
       "P": 42,
       "K": 43,
       "temperature": 20.88,
       "humidity": 82.0,
       "ph": 6.5,
       "rainfall": 202.9
     }'
```

## Testing

Test the Python service:
```bash
cd predict_service
python test_predict.py
```

## Model Training

The model uses a Random Forest classifier with the following pipeline:
1. StandardScaler for feature normalization
2. RandomForestClassifier for crop prediction

To retrain the model:
```bash
python scripts/train_and_save.py
```
