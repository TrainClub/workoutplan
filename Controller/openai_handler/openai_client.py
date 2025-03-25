import openai
from Controller.aws_handler.aws_services import parameter_store
import json 

def call_openai(prompt):
    try:
        print('[INFO] Iniciando criação do treino para usuário')
        api_key = parameter_store(parameter_name="/openai/api_key")
        client = openai.Client(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Você é um personal trainer especializado em criar planos de treino personalizados."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=4096,
            n=1
        )
        
        content = response.choices[0].message.content if response.choices else None
        if content:
            print('[INFO] Treino criado com sucesso.')
            return content
        else:
            raise ValueError("Resposta da OpenAI não contém o conteúdo esperado.")
    
    except ValueError as value_err:
        print(f"[ERROR] Erro de valor: {value_err}")
        return json.dumps({"error": str(value_err)})
    
    except openai.OpenAIError as openai_err:
        print(f"[ERROR] Erro da API OpenAI: {openai_err}")
        return json.dumps({"error": "Erro na API OpenAI. Tente novamente mais tarde."})
    
    except Exception as err:
        print(f"[ERROR] Erro inesperado: {err}")
        return json.dumps({"error": "Erro inesperado. Contate o suporte."})