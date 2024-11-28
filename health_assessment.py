# diet_planner/health_assessment.py
from typing import Dict, List, Tuple
import numpy as np

class HealthAssessment:
    HEALTH_RISK_MATRIX = {
        'cardiovascular': {
            'risk_factors': ['age', 'waist_circumference', 'bmi'],
            'base_risk': 0.3
        },
        'diabetes': {
            'risk_factors': ['bmi', 'age', 'activity_level'],
            'base_risk': 0.2
        },
        'metabolic_syndrome': {
            'risk_factors': ['waist_circumference', 'bmi', 'activity_level'],
            'base_risk': 0.25
        }
    }

    @classmethod
    def assess_health_risks(cls, user_profile: Dict) -> Dict[str, float]:
        """
        Assess health risks based on user profile
        Returns risk percentages for different health conditions
        """
        # Ensure all necessary keys exist with default values
        safe_profile = {
            'age': user_profile.get('age', 30),
            'sex': user_profile.get('sex', 'unknown'),
            'waist_circumference': user_profile.get('waist_circumference', 0),
            'bmi': user_profile.get('bmi', 22),
            'activity_level': user_profile.get('activity_level', 'sedentary')
        }
        
        risks = {}
        
        for condition, config in cls.HEALTH_RISK_MATRIX.items():
            risk_score = config['base_risk']
            
            # Adjust risk based on individual factors
            if condition == 'cardiovascular':
                risk_score += cls._cardiovascular_risk_adjustment(safe_profile)
            
            elif condition == 'diabetes':
                risk_score += cls._diabetes_risk_adjustment(safe_profile)
            
            elif condition == 'metabolic_syndrome':
                risk_score += cls._metabolic_syndrome_risk(safe_profile)
            
            # Normalize and cap risk at 70%
            risks[condition] = min(0.7, max(0, risk_score)) * 100
        
        return risks

    @staticmethod
    def _cardiovascular_risk_adjustment(profile: Dict) -> float:
        """Adjust cardiovascular risk"""
        risk_adjustment = 0
        
        # Age factor
        if profile['age'] > 45:
            risk_adjustment += 0.1
        
        # Waist circumference risk
        if profile['sex'] == 'male' and profile['waist_circumference'] > 102:
            risk_adjustment += 0.15
        elif profile['sex'] == 'female' and profile['waist_circumference'] > 88:
            risk_adjustment += 0.15
        
        # BMI risk
        if profile['bmi'] > 30:
            risk_adjustment += 0.2
        
        return risk_adjustment

    @staticmethod
    def _diabetes_risk_adjustment(profile: Dict) -> float:
        """Adjust diabetes risk"""
        risk_adjustment = 0
        
        if profile['age'] > 45:
            risk_adjustment += 0.1
        
        if profile['bmi'] > 25:
            risk_adjustment += 0.15
        
        if profile['activity_level'] in ['sedentary', 'lightly_active']:
            risk_adjustment += 0.1
        
        return risk_adjustment

    @staticmethod
    def _metabolic_syndrome_risk(profile: Dict) -> float:
        """Assess metabolic syndrome risk"""
        risk_adjustment = 0
        
        if profile['waist_circumference'] > 88 and profile['sex'] == 'female':
            risk_adjustment += 0.2
        
        if profile['waist_circumference'] > 102 and profile['sex'] == 'male':
            risk_adjustment += 0.2
        
        if profile['activity_level'] in ['sedentary', 'lightly_active']:
            risk_adjustment += 0.1
        
        return risk_adjustment