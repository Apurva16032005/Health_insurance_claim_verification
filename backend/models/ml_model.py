import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml_model.pkl")

class FraudMLModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        """
        Loads the trained model from disk.
        If missing, it creates a dummy model so the server doesn't crash.
        """
        if os.path.exists(MODEL_PATH):
            print(f"[INFO] Loading ML Model from: {MODEL_PATH}")
            try:
                with open(MODEL_PATH, "rb") as f:
                    data = pickle.load(f)
                    self.model = data['model']
                    self.scaler = data['scaler']
                print("[INFO] ML Model Loaded Successfully")
            except Exception as e:
                print(f"[WARN] Error loading model: {e}")
                self._train_dummy_model()
        else:
            print("[WARN] Model file not found. Training temporary dummy model...")
            self._train_dummy_model()

    def _train_dummy_model(self):
        """Trains a simple fallback model if the real one isn't found."""
        X_dummy = np.random.rand(10, 4)
        y_dummy = np.random.randint(0, 2, 10)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_dummy)
        self.model = RandomForestClassifier()
        self.model.fit(X_scaled, y_dummy)
        print("[WARN] Dummy model active (Run train_model.py to train real model)")

    def predict(self, features):
        """
        Predicts fraud probability.
        Input features: [CNN_Score, Meta_Flag, Amount_Anomaly, NLP_Score]
        """
        if not self.model or not self.scaler:
            return 0.5
            
        try:
            # Reshape and scale
            features_array = np.array(features).reshape(1, -1)
            features_scaled = self.scaler.transform(features_array)
            
            # Get probability of Fraud / Risk
            probs = self.model.predict_proba(features_scaled)[0]
            if len(probs) == 3:
                # 3-Class Risk weighting: Class 0 (Low: 0.0), Class 1 (Medium: 0.5), Class 2 (High: 1.0)
                fraud_prob = probs[1] * 0.5 + probs[2] * 1.0
            else:
                fraud_prob = probs[1]
            return round(float(fraud_prob), 4)
        except Exception as e:
            print(f"Prediction Error: {e}")
            return 0.5
