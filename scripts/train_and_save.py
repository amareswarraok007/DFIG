# scripts/train_and_save.py
"""
Train a sklearn Pipeline (scaler + RandomForest) using Agri.xlsx
Saves:
  - model/pipeline.pkl
  - model/expected_columns.txt
Adjust TARGET if your target column differs.
"""

import os
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

DATA_PATH = '/workspaces/DFIG/Agri.xlsx'      # must be next to script or give full path
TARGET = "crops"               # as used in your notebook
SAVE_DIR = "model"

os.makedirs(SAVE_DIR, exist_ok=True)

print("Loading data from:", DATA_PATH)
df = pd.read_excel(DATA_PATH)
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

if TARGET not in df.columns:
    raise RuntimeError(f"TARGET '{TARGET}' not found. Columns: {df.columns.tolist()}")

# Use these exact features (from your notebook)
FEATURES = ['N','P','K','temperature','humidity','ph','rainfall']
for c in FEATURES:
    if c not in df.columns:
        raise RuntimeError(f"Feature '{c}' not in dataframe columns.")

X = df[FEATURES]
y = df[TARGET]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline: StandardScaler + RandomForest
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
])

print("Fitting pipeline...")
pipeline.fit(X_train, y_train)

# Evaluate
y_train_pred = pipeline.predict(X_train)
y_test_pred = pipeline.predict(X_test)
print("Train accuracy:", round(accuracy_score(y_train, y_train_pred), 4))
print("Test accuracy: ", round(accuracy_score(y_test, y_test_pred), 4))
print("\nClassification report (test):")
print(classification_report(y_test, y_test_pred, zero_division=0, digits=4))

# Save pipeline and expected columns
pipeline_path = os.path.join(SAVE_DIR, "pipeline.pkl")
joblib.dump(pipeline, pipeline_path)
print("Saved pipeline to:", pipeline_path)

expected_cols_path = os.path.join(SAVE_DIR, "expected_columns.txt")
with open(expected_cols_path, "w") as f:
    f.write(",".join(FEATURES))
print("Saved expected columns to:", expected_cols_path)
