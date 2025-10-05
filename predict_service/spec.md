Model service contract
----------------------
- Health: GET /health -> { "status": "ok" }

- Predict (single): POST /predict
  Body: JSON object with keys exactly matching feature names (see model/expected_columns.txt)
  Example:
    { "N":90, "P":42, "K":43, "temperature":20.8797, "humidity":82.0027, "ph":6.5029, "rainfall":202.9355 }

  Response:
    { "predictions": [<label>], "probabilities": [[...]] }

- Predict (batch): POST /predict_batch
  Body: JSON array of objects (each same format as above)

Notes:
- Feature names are case-sensitive. See model/expected_columns.txt.
- The service expects a scikit-learn pipeline saved at MODEL_PATH that includes preprocessing and model.
