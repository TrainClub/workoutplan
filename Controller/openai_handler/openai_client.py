import openai
from Controller.aws_handler.aws_services import parameter_store

def call_openai(prompt):
    try:
        print('[INFO] Iniciando criação do treino para usuario')
        api_key = parameter_store(parameter_name="/openai/api_key")  # Obtendo a API Key
        client = openai.Client(api_key=api_key)  # Passando a chave diretamente para o cliente
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Você é um personal trainer especializado em criar planos de treino personalizados."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,  # Controle de criatividade (0 = preciso, 1 = criativo)
            max_tokens=4096,  # Limite de tokens na resposta
            n=1,  # Número de respostas
            stop=None,  # Se necessário, defina um token de parada
        )

        content = response.choices[0].message.content
        if content:
            print('[INFO] Treino criado com sucesso.')
            return content
        else:
            raise ValueError("Resposta não contém o conteúdo esperado.")

    except ValueError as value_err:
        print(f"Erro de valor: {value_err}")
        return {"error": f"Erro de resposta inválida: {str(value_err)}"}

    except Exception as err:
        print(f"Erro inesperado: {err}")
        return {"error": f"Erro inesperado: {str(err)}"}