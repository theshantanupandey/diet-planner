from user_profile import UserProfile
from health_assessment import HealthAssessment
from diet_plan_generator import DietPlanGenerator
from scoring_system import HealthScoreCalculator
from ml_models import HealthRiskPredictor

class DietPlannerAI:
    def __init__(self):
        self.ml_predictor = HealthRiskPredictor()
        self.tracking_history = []

    def create_user_profile(self, user_data: dict) -> UserProfile:
        """
        Create and validate user profile
        """
        profile = UserProfile(
            age=user_data.get('age', 30),
            sex=user_data.get('sex', 'female'),
            height=user_data.get('height', 165),
            weight=user_data.get('weight', 70),
            activity_level=user_data.get('activity_level', 'sedentary'),
            allergies=user_data.get('allergies', []),
            caffeine_intake=user_data.get('caffeine_intake', 0),
            alcohol_intake=user_data.get('alcohol_intake', 0),
            medications=user_data.get('medications', []),
            health_issues=user_data.get('health_issues', []),
            waist_circumference=user_data.get('waist_circumference', 80)
        )
        return profile

    def assess_health_risks(self, user_profile: UserProfile) -> dict:
        """
        Comprehensive health risk assessment
        """
        # Convert user profile to dictionary for assessment
        profile_dict = user_profile.to_dict()
        
        # Calculate and add BMI to the profile dictionary
        bmi = user_profile.calculate_bmi()
        profile_dict['bmi'] = bmi
        
        # Ensure all necessary keys are present
        profile_dict.update({
            'age': user_profile.age,
            'sex': user_profile.sex,
            'waist_circumference': user_profile.waist_circumference,
            'activity_level': user_profile.activity_level
        })
        
        # Assess health risks
        health_risks = HealthAssessment.assess_health_risks(profile_dict)
        
        # Machine learning enhanced risk prediction
        try:
            ml_risk_score = self.ml_predictor.predict_health_risk(profile_dict)
            
            # Blend traditional and ML-based risk assessment
            for condition, risk in health_risks.items():
                health_risks[condition] = (risk + ml_risk_score) / 2
        except Exception as e:
            print(f"ML Risk Prediction Error: {e}")
            # Fallback to traditional risk assessment
        
        return health_risks

    def generate_diet_plan(self, user_profile: UserProfile, health_risks: dict) -> dict:
        """
        Generate personalized diet plan
        """
        profile_dict = user_profile.to_dict()
        diet_plan = DietPlanGenerator.generate_diet_plan(profile_dict, health_risks)
        
        return diet_plan

    def calculate_health_score(self, user_profile: UserProfile, health_risks: dict) -> float:
        """
        Calculate overall health score
        """
        profile_dict = user_profile.to_dict()
        health_score = HealthScoreCalculator.calculate_health_score(
            profile_dict, 
            health_risks, 
            self.tracking_history
        )
        
        return health_score

    def update_tracking_history(self, tracking_data: dict):
        """
        Update user tracking history
        """
        self.tracking_history.append(tracking_data)
        
        # Keep only last 10 entries to manage memory
        self.tracking_history = self.tracking_history[-10:]

    def generate_comprehensive_report(self, user_profile: UserProfile) -> dict:
        """
        Generate comprehensive health report
        """
        # Assess health risks
        health_risks = self.assess_health_risks(user_profile)
        
        # Generate diet plan
        diet_plan = self.generate_diet_plan(user_profile, health_risks)
        
        # Calculate health score
        health_score = self.calculate_health_score(user_profile, health_risks)
        
        # Compile report
        report = {
            'user_id': user_profile.user_id,
            'health_risks': health_risks,
            'diet_plan': diet_plan,
            'health_score': health_score,
            'recommendations': self._generate_recommendations(health_risks)
        }
        
        return report

    def _generate_recommendations(self, health_risks: dict) -> list:
        """
        Generate personalized health recommendations
        """
        recommendations = []
        
        if health_risks.get('cardiovascular', 0) > 50:
            recommendations.extend([
                "Increase intake of heart-healthy foods like leafy greens and nuts",
                "Consider stress reduction techniques",
                "Aim for regular cardiovascular exercise"
            ])
        
        if health_risks.get('diabetes', 0) > 50:
            recommendations.extend([
                "Focus on low glycemic index vegetarian foods",
                "Incorporate more fiber-rich foods",
                "Monitor portion sizes carefully"
            ])
        
        if health_risks.get('metabolic_syndrome', 0) > 50:
            recommendations.extend([
                "Prioritize whole grains and plant-based proteins",
                "Reduce processed food intake",
                "Increase physical activity"
            ])
        
        return recommendations

# Example usage
def main():
    # Sample user data with comprehensive information
    user_data = {
        'age': 35,
        'sex': 'female',
        'height': 165,
        'weight': 70,
        'activity_level': 'moderately_active',
        'waist_circumference': 85,
        'health_issues': ['occasional stress']
    }

    # Initialize AI
    diet_planner = DietPlannerAI()
    
    # Create user profile
    user_profile = diet_planner.create_user_profile(user_data)
    
    # Generate comprehensive report
    report = diet_planner.generate_comprehensive_report(user_profile)
    
    print("Comprehensive Health Report:")
    print(f"Health Risks: {report['health_risks']}")
    print(f"Health Score: {report['health_score']}")
    print("Recommendations:")
    for rec in report['recommendations']:
        print(f"- {rec}")

if __name__ == "__main__":
    main()
