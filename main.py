import json
from utils.prompt_builder import create_prompt
from Controller.openai_handler.openai_client import call_openai
from Controller.dynamo_handler.dbhelper import DynamoDBHelper
from Controller.trainning_registration.registrations import DataProcessor

def lambda_handler(event, context):
    try:
        print("[INFO] Evento recebido:", event)
        
        # Verifica se a estrutura do evento está correta
        if 'Records' not in event or not event['Records']:
            raise ValueError("[ERROR] Evento inválido, 'Records' ausente ou vazio")
        
        sns_message = event['Records'][0].get('Sns', {}).get('Message')
        if not sns_message:
            raise ValueError("[ERROR] Mensagem SNS ausente no evento")
        
        event_data = json.loads(sns_message)
        
        # Gera o prompt e chama a OpenAI
        prompt = create_prompt(body=event_data)
        if not prompt:
            raise ValueError("[ERROR] Prompt gerado está vazio")
        
        training_plan_response = call_openai(prompt)
        try:
            training_plan = json.loads(training_plan_response.replace("`", "").replace("json", ""))
        except json.JSONDecodeError:
            raise ValueError("[ERROR] Falha ao decodificar a resposta da OpenAI")
        
        if not training_plan:
            raise ValueError("[ERROR] Resposta da OpenAI vazia ou inválida")
        
        processor = DataProcessor(event=event_data, workout_event=training_plan)
        
        record_map = ['workout_create_status', 'workout_plans']
        dynamo_helper = DynamoDBHelper('BioFit')
        
        for record in record_map:
            try:
                print(f'[INFO] Processando {record} para importação no banco de dados')
                table = processor.create_record(record)
                
                if not table:
                    print(f'[WARNING] Nenhum dado gerado para {record}')
                    continue
                
                if record == 'workout_plans':
                    for item in table:
                        if item:
                            dynamo_helper.put_item(item)
                        else:
                            print(f'[WARNING] Item vazio em {record}')
                else:
                    dynamo_helper.put_item(table)
                
            except Exception as err:
                print(f'[ERROR] Erro ao salvar {record} na base de dados: {err}')
                
    except Exception as e:
        print(f"[ERROR] Erro inesperado na execução: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
    
if __name__ == '__main__':
    event = {
        'Records': [
            {
                'EventSource': 'aws:sns',
                'Sns': {
                    'Message': json.dumps({
                        "new_member": {
                            "user_data": {"user_id": "1", "email": "mateusjrcosta@hotmail.com", "user_name": "Mateus Costa"},
                            "personal_data": {"gender": "masculino", "weight": "135", "height": "183", "date_birth": "13/04/2001"},
                            "user_purpose": ["Ganho de Massa Muscular", "Perda de Peso"],
                            "training_preferences": {"experience_level": "Intermediário", "training_frequency_per_week": 5},
                            "health_conditions": ["Joelho", "Ombro"]
                        }
                    })
                }
            }
        ]
    }
    lambda_handler(event=event, context='')
