import json
from utils.prompt_builder import *
from Controller.openai_handler.openai_client import * 
from Controller.dynamo_handler.dbhelper import DynamoDBHelper
from Controller.trainning_registration.registrations import DataProcessor

def lambda_handler(event, context):
    try:
        print(event)
        event = json.loads(event['Records'][0]['Sns']['Message'])
        prompt = create_prompt(body=event)
        training_plan = call_openai(prompt)
        training_plan = json.loads(training_plan.replace("`", "").replace("json", ""))

        processor = DataProcessor(event=event, workout_event=training_plan)
        if training_plan:
            record_map = [
                'workout_create_status',
                'workout_plans',
            ]

            dynamo_helper = DynamoDBHelper('BioFit')
            for record in record_map:
                table = processor.create_record(record)
                if 'workout_plans' in record:
                    for tb in table:
                        dynamo_helper.put_item(tb)
                else:
                    dynamo_helper.put_item(table)
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    
if __name__=='__main__':
    event  = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:539247461774:createWorkoutPlan:0b5ddd13-ed88-4262-971b-5b1e763cec18', 'Sns': {'Type': 'Notification', 'MessageId': 'b583cb7c-e6a5-5c40-ac5f-ab2744788d09', 'TopicArn': 'arn:aws:sns:us-east-1:539247461774:createWorkoutPlan', 'Subject': None, 'Message': '{"new_member": {"user_data": {"user_id": "1", "email": "mateusjrcosta@hotmail.com", "user_name": "Mateus Costa"}, "personal_data": {"gender": "masculino", "weight": "135", "height": "183", "date_birth": "13/04/2001"}, "user_purpose": ["Ganho de Massa Muscular", "Perda de Peso"], "training_preferences": {"experience_level": "Treinos sem rotina fixa (Intermedi\\u00e1rio)", "training_frequency_per_week": 5}, "health_conditions": ["Joelho", "Ombro"]}}', 'Timestamp': '2025-03-24T18:12:45.006Z', 'SignatureVersion': '1', 'Signature': 'BWMugnXU2iCAd41nhbTKj/2mZFBWtmVasm7yoSAwNCnyD74PI02yJPL8klOYS6ggOssWwRTz+eHYZLOSq6ptlhtegY0eWgiQxd6k3lDwkrcX4Fb7pdh9d2rQcWyVcJt2qkKsGhUfGUR9+h4SYuB0ghtCjOID6OnbCZIknCiC1FpS2tfaaK3q6rdegSbctQHQoPhp+akf/T60Mxt/qEbK6Kb/4Vk+zZLCWeh3C4XuXztThhPkaOeQw1um4eOeMjZEEmHDynfogaDHFg04QTDYbqiQjTw/QXLrwTR4J9T+NsaZ3VI5I1UeK8c2qry3QW5FU0cxe/A1F0jDCw6pb+lK9w==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-9c6465fa7f48f5cacd23014631ec1136.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:539247461774:createWorkoutPlan:0b5ddd13-ed88-4262-971b-5b1e763cec18', 'MessageAttributes': {}}}]}
    lambda_handler(event=event, context='')