# diet_planner/scoring_system.py
from typing import Dict, List

class HealthScoreCalculator:
    @classmethod
    def calculate_health_score(cls, user_profile: Dict, 
                                health_risks: Dict, 
                                tracking_history: List[Dict]) -> float:
        """
        Calculate dynamic health score out of 100
        """
        # Baseline assessment (30 points)
        baseline_score = cls._calculate_baseline_score(user_profile)
        
        # Lifestyle metrics (20 points)
        lifestyle_score = cls._calculate_lifestyle_score(user_profile)
        
        # Nutritional compliance (30 points)
        nutrition_score = cls._calculate_nutrition_score(tracking_history)
        
        # Progress tracking (20 points)
        progress_score = cls._calculate_progress_score(tracking_history)
        
        # Total weighted score
        total_score = (
            baseline_score * 0.3 + 
            lifestyle_score * 0.2 + 
            nutrition_score * 0.3 + 
            progress_score * 0.2
        )
        
        return round(total_score, 2)

    @staticmethod
    def _calculate_baseline_score(profile: Dict) -> float:
        """Calculate baseline health metrics score"""
        bmi_score = max(0, 30 - abs(profile['bmi'] - 22)) / 8 * 10
        age_score = max(0, 10 - (profile['age'] - 30) / 5)
        return min(bmi_score + age_score, 30)

    @staticmethod
    def _calculate_lifestyle_score(profile: Dict) -> float:
        """Calculate lifestyle related score"""
        activity_scores = {
            'sedentary': 5,
            'lightly_active': 10,
            'moderately_active': 15,
            'very_active': 20
        }
        return activity_scores.get(profile.get('activity_level', 'sedentary'), 5)

    @staticmethod
    def _calculate_nutrition_score(tracking_history: List[Dict]) -> float:
        """Calculate nutrition compliance score"""
        if not tracking_history:
            return 0
        
        recent_entries = tracking_history[-5:]  # Last 5 entries
        compliance_rate = sum(entry.get('meal_compliance', 0) for entry in recent_entries) / len(recent_entries)
        return compliance_rate * 30

    @staticmethod
    def _calculate_progress_score(tracking_history: List[Dict]) -> float:
        """Calculate progress tracking score"""
        if not tracking_history:
            return 0
        
        weight_changes = [entry.get('weight_change', 0) for entry in tracking_history]
        consistency = len([change for change in weight_changes if abs(change) < 1]) / len(weight_changes)
        
        return consistency * 20