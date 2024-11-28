# diet_planner/user_profile.py
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class UserProfile:
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    age: int = 0
    sex: str = ""
    height: float = 0.0  # in cm
    weight: float = 0.0  # in kg
    activity_level: str = ""
    allergies: List[str] = field(default_factory=list)
    caffeine_intake: float = 0.0  # mg per day
    alcohol_intake: float = 0.0  # standard drinks per week
    medications: List[str] = field(default_factory=list)
    health_issues: List[str] = field(default_factory=list)
    waist_circumference: float = 0.0  # in cm

    def calculate_bmi(self) -> float:
        """Calculate Body Mass Index"""
        return self.weight / ((self.height / 100) ** 2)

    def calculate_bmr(self) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if self.sex.lower() == 'male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        
        return bmr

    def calculate_tdee(self) -> float:
        """Calculate Total Daily Energy Expenditure"""
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        bmr = self.calculate_bmr()
        return bmr * activity_multipliers.get(self.activity_level, 1.2)

    def to_dict(self) -> Dict:
        """Convert profile to dictionary for storage/transmission"""
        return {
            'user_id': self.user_id,
            'age': self.age,
            'sex': self.sex,
            'height': self.height,
            'weight': self.weight,
            'bmi': self.calculate_bmi(),
            'bmr': self.calculate_bmr(),
            'tdee': self.calculate_tdee()
        }