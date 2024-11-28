# diet_planner/diet_plan_generator.py
from typing import Dict, List, Tuple
import numpy as np

class DietPlanGenerator:
    # Vegetarian RDA (Recommended Daily Allowance) per macro and micronutrients
    RDA = {
        'protein': 0.8,  # g per kg body weight
        'iron': 8.0,     # mg/day
        'calcium': 1000, # mg/day
        'vitamin_b12': 2.4,  # mcg/day
        'vitamin_d': 600,    # IU/day
        'zinc': 8,       # mg/day
    }

    @classmethod
    def generate_diet_plan(cls, user_profile: Dict, health_risks: Dict) -> Dict:
        """
        Generate personalized vegetarian diet plan
        """
        # Calculate base nutritional requirements
        body_weight = user_profile['weight']
        protein_requirement = body_weight * cls.RDA['protein']
        
        # Adjust meals based on health risks and activity
        meals = cls._create_meal_sequence(user_profile, health_risks)
        
        # Micronutrient focus meals
        nutrient_focus = cls._determine_nutrient_focus(health_risks)
        
        diet_plan = {
            'protein_target': protein_requirement,
            'micronutrient_focus': nutrient_focus,
            'meals': meals
        }
        
        return diet_plan

    @classmethod
    def _create_meal_sequence(cls, profile, health_risks) -> List[Dict]:
        """
        Create dynamic meal sequence
        """
        meals = [
            {
                'type': 'breakfast',
                'recommended_timing': '7-8 AM',
                'nutrition_goals': ['energy_boost', 'metabolism_kickstart']
            },
            {
                'type': 'lunch',
                'recommended_timing': '12-1 PM',
                'nutrition_goals': ['sustained_energy', 'muscle_maintenance']
            },
            {
                'type': 'dinner',
                'recommended_timing': '6-7 PM',
                'nutrition_goals': ['recovery', 'minimal_digestion_load']
            }
        ]
        
        # Conditionally skip meals based on health assessment
        if health_risks.get('metabolic_syndrome', 0) > 50:
            meals = [meal for meal in meals if meal['type'] != 'dinner']
        
        return meals

    @classmethod
    def _determine_nutrient_focus(cls, health_risks) -> List[str]:
        """
        Determine micronutrient focus based on health risks
        """
        nutrient_recommendations = {
            'cardiovascular': ['omega_3', 'fiber', 'potassium'],
            'diabetes': ['chromium', 'magnesium', 'fiber'],
            'metabolic_syndrome': ['vitamin_d', 'calcium', 'zinc']
        }
        
        focus_nutrients = []
        for condition, risk in health_risks.items():
            if risk > 50:
                focus_nutrients.extend(nutrient_recommendations.get(condition, []))
        
        return list(set(focus_nutrients))