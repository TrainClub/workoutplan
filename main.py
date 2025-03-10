import json
from utils.prompt_builder import *
from services.OpenAIClient.openai_client import * 
from services.DBClient.db_client import insert_data

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = createprompt(body=body)
        training_plan = call_openai(prompt)
        training_plan = json.loads(training_plan.replace("`", "").replace("json", ""))
        training_plan['user_id'] = json.loads(event['body'])['new_member']['user_data']['user_id']
        insert_data(data=training_plan, table_name='workout_plans')
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }