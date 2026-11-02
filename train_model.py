import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1. Load student placement dataset
data = pd.read_csv("placement_data.csv")

# 2. Select input features and target
X = data.drop("Placement Status", axis=1)
X["Internship Experience"] = X["Internship Experience"].map(
    {"No": 0, "Yes": 1}
)

y = data["Placement Status"]

# 3. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# 4. Train the machine learning model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# 5. Evaluate the model
predictions = model.predict(X_test)

print("Model Training Completed!")
print("Test Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

# 6. Save the trained model and feature names
with open("placement_model.pkl", "wb") as file:
    pickle.dump(
        {"model": model, "features": list(X.columns)},
        file
    )

print("\nModel saved as placement_model.pkl")