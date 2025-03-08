import json
from utils.prompt_builder import *

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = createprompt(body=body)
        print(prompt)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

if __name__=='__main__':
    event = {
        "body": json.dumps({  # Converte o dicionário para string JSON
        "new_member": {
            "personal_data": {
                "weight": "135",
                "height": "183"
            },
            "user_purpose": {
                "main_objective": "Gain Muscle",
                "secondary_objective": "Lose Fat"
            },
            "training_preferences": {
                "experience_level": "Beginner",
                "training_frequency_per_week": 4
            },
            "health_conditions": {
                "pre_diabetes": True,
                "high_cholesterol": True,
                "spinal_disorder": False,
                "hypertension": False,
                "dizziness_or_fainting": False,
                "other_health_issues": "Had thyroid issues in the past but no longer."
            },
            "affected_areas": {
                "knee": True,
                "shoulder": True,
                "elbow": False,
                "spine": False,
                "lower_back": False
            }
        }
    })
    }
    lambda_handler(event=event, context=None)