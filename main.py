import json
from utils.prompt_builder import *
from services.OpenAIClient.openai_client import * 

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = createprompt(body=body)
        training_plan = call_openai(prompt)
        
        with open(r"database\output\workoutplan.json", "w", encoding="utf-8") as file:
            file.write(training_plan)

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
                "gender":"male",
                "weight": "50",
                "height": "162"
            },
            "user_purpose": {
                "main_objective": "Gain Muscle",
                "secondary_objective": "Tone and define"
            },
            "training_preferences": {
                "experience_level": "intermediate",
                "training_frequency_per_week": 5
            },
            "health_conditions": {
                "pre_diabetes": False,
                "high_cholesterol": False,
                "spinal_disorder": False,
                "hypertension": False,
                "dizziness_or_fainting": False,
                "other_health_issues": "Tenho desgaste na lombar e escoliose"
            },
            "affected_areas": {
                "knee": False,
                "shoulder": False,
                "elbow": False,
                "spine": False,
                "lower_back": False
            }
        }
    })
    }
    lambda_handler(event=event, context=None)