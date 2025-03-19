import json
import os
from datetime import datetime

def create_prompt(body: json) -> str:
    try:
        user_data = body.get("new_member", {})

        # Define a data de nascimento do usuário para calcular a idade
        date_of_birth = user_data.get("personal_data", {}).get("date_birth", "01/01/1900")
        birth_date = datetime.strptime(date_of_birth, "%d/%m/%Y")
        age = (datetime.now() - birth_date).days // 365  # Calcula a idade em anos

        # Define o diretório base e o caminho do arquivo de prompt
        base_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.abspath(os.path.join(base_dir, "..", "templates", "prompt.txt"))

        # Lê o template do prompt
        with open(file_path, 'r', encoding='utf-8') as file:
            prompt = file.read()

        # Define os campos de dados para substituir no template
        fields = {
            "{age}": str(age),
            "{weight}": user_data.get("personal_data", {}).get("weight", "Not provided"),
            "{height}": user_data.get("personal_data", {}).get("height", "Not provided"),
            "{main_objective}": ', '.join(user_data.get("user_purpose", [])) if user_data.get("user_purpose") else "Not provided",
            "{secondary_objective}": "Not provided",  # Não há campo para objetivo secundário no exemplo fornecido
            "{experience_level}": user_data.get("training_preferences", {}).get("experience_level", "Not provided"),
            "{training_frequency_per_week}": str(user_data.get("training_preferences", {}).get("training_frequency_per_week", "Not provided")),
            "{pre_diabetes}": "Not provided",  # Não há campo correspondente no exemplo fornecido
            "{high_cholesterol}": "Not provided",  # Não há campo correspondente no exemplo fornecido
            "{spinal_disorder}": "Not provided",  # Não há campo correspondente no exemplo fornecido
            "{hypertension}": "Not provided",  # Não há campo correspondente no exemplo fornecido
            "{dizziness_or_fainting}": "Not provided",  # Não há campo correspondente no exemplo fornecido
            "{other_health_issues}": "None",  # Não há campo correspondente no exemplo fornecido
            "{knee}": "Yes" if "Joelho" in user_data.get("health_conditions", []) else "Not provided",
            "{shoulder}": "Yes" if "Ombro" in user_data.get("health_conditions", []) else "Not provided",
            "{elbow}": "Not provided",  # Não há dado fornecido
            "{spine}": "Not provided",  # Não há dado fornecido
            "{lower_back}": "Not provided"  # Não há dado fornecido
        }

        # Substitui os placeholders no template com os dados do usuário
        for placeholder, value in fields.items():
            prompt = prompt.replace(placeholder, value)

        return prompt

    except FileNotFoundError:
        return "Erro: O arquivo de template não foi encontrado."
    except KeyError as e:
        return f"Erro: Dados ausentes para a chave: {e}"
    except Exception as e:
        return f"Ocorreu um erro inesperado: {str(e)}"
