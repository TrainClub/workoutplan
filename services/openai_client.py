import openai
import json
from openai.error import OpenAIError, Timeout

OPENAIKEY = "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"
openai.api_key = OPENAIKEY

def call_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Você é um personal trainer especializado em criar planos de treino personalizados."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Controle de criatividade (0 = preciso, 1 = criativo)
            max_tokens=1000,  # Limite de tokens na resposta
            n=1,  # Número de respostas
            stop=None,  # Se necessário, defina um token de parada
            timeout=30  # Timeout para a chamada (30 segundos)
        )

        if 'choices' in response and len(response['choices']) > 0:
            content = response['choices'][0].get("message", {}).get("content", "")
            if content:
                return json.loads(content)
            else:
                raise ValueError("Resposta não contém o conteúdo esperado.")
        else:
            raise ValueError("Resposta da API não contém 'choices' válidos.")

    except OpenAIError as openai_err:
        print(f"Erro na API OpenAI: {openai_err}")
        return {"error": f"Erro na API: {str(openai_err)}"}

    except Timeout as timeout_err:
        print(f"Erro de timeout: {timeout_err}")
        return {"error": "Tempo limite da solicitação excedido. Tente novamente."}

    except ValueError as value_err:
        print(f"Erro de valor: {value_err}")
        return {"error": f"Erro de resposta inválida: {str(value_err)}"}

    except Exception as err:
        print(f"Erro inesperado: {err}")
        return {"error": f"Erro inesperado: {str(err)}"}