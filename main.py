import json
from utils.prompt_builder import *
from Controller.openai_handler.openai_client import * 

def lambda_handler(event, context):
    try:
        prompt = create_prompt(body=event)
        training_plan = call_openai(prompt)
        training_plan = json.loads(training_plan.replace("`", "").replace("json", ""))

        if training_plan:
            return {
                "statusCode":200,
                "body":json.dumps(training_plan),
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    
if __name__=='__main__':
    event = {'new_member': {'personal_data': {'gender': 'Masculino', 'weight': '135', 'height': '183', 'date_birth': '13/04/2001'}, 'user_purpose': ['Ganho de Massa Muscular', 'Fortalecimento Muscular'], 'training_preferences': {'experience_level': 'Treinos sem rotina fixa (Intermediario)', 'training_frequency_per_week': 5}, 'health_conditions': ['Joelho', 'Ombro']}}
    lambda_handler(event=event, context='')