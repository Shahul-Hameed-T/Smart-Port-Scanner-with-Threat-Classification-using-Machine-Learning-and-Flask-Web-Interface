import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("sample_dataset.csv")
X = df[["open_ports", "risky_ports", "os_code"]]
y = df["label"]

# Train classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model
joblib.dump(model, "threat_classifier_model.pkl")
print("✅ Model trained and saved as 'threat_classifier_model.pkl'")
