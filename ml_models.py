# diet_planner/ml_models.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from typing import Dict, List

class HealthRiskPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100)
        self.scaler = StandardScaler()

    def train_model(self, training_data: List[Dict]):
        """
        Train machine learning model for health risk prediction
        """
        # Extract features and targets
        features = []
        targets = []
        
        for data in training_data:
            feature_vector = [
                data.get('age', 30),
                data.get('bmi', 22),
                data.get('waist_circumference', 80),
                data.get('activity_level_numeric', 1)
            ]
            features.append(feature_vector)
            targets.append(data.get('health_risk_score', 0))
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features_scaled, targets, test_size=0.2
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        return self.model.score(X_test, y_test)

    def predict_health_risk(self, user_profile: Dict) -> float:
        """
        Predict health risk for a new user profile
        """
        # Default mapping for activity levels
        activity_level_map = {
            'sedentary': 1, 
            'lightly_active': 2, 
            'moderately_active': 3, 
            'very_active': 4
        }
        
        # Create feature vector with default values
        feature_vector = [
            user_profile.get('age', 30),
            user_profile.get('bmi', 22),
            user_profile.get('waist_circumference', 80),
            activity_level_map.get(
                user_profile.get('activity_level', 'sedentary'), 
                1
            )
        ]
        
        # Ensure we have a 2D array for prediction
        scaled_features = self.scaler.transform([feature_vector])
        
        # Predict and return risk score
        prediction = self.model.predict(scaled_features)[0]
        
        # Normalize prediction to a reasonable risk score
        return max(0, min(80, prediction))  # Limit to 0-80 range