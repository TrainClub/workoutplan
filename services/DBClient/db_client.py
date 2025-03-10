import psycopg2
from services.AWSClient.aws_services import parameter_store
import json 
import sys 

def dbconnect():
    print('[INFO] Desempacotando credenciais.')
    credentials = parameter_store(parameter_name="/biotrainningdb/credentials")    
    credentials = json.loads(credentials)

    try:
        print('[INFO] Iniciando conexao com banco de dados.')
        connection = psycopg2.connect(
            host=credentials['host'],
            database=credentials['db'],
            user=credentials['user'],
            password=credentials['pwd']
        )
        return connection
    except psycopg2.OperationalError as error:
        print(f'[ERROR] Nao foi possivel estabelecer conexao, erro: {error}')

def insert_data(data, table_name):
    conn = dbconnect()
    if conn is None:
        print("[ERROR] Falha na conexão com o banco de dados.")
        sys.exit(0)

    cursor = conn.cursor()

    try:
        for day_trainning in data["training_plan"]:
            day = day_trainning['day']
            exercises = day_trainning['exercises'] 
            user_id = data['user_id']

            for exercise in exercises:
                muscle_groups = exercise['muscle_groups']
                name = exercise['name']
                sets = exercise['sets']
                reps = exercise['reps']
                tips = exercise['tips']
                alternatives = exercise['alternatives']
                affected_muscles = exercise['affected_muscles']

                query = f"""
                INSERT INTO workout_plans (user_id, day, muscle_group, name, sets, reps, tips, alternatives, affected_muscles)
                VALUES ('{user_id}', '{day}', '{muscle_groups}', '{name}', '{sets}', 
                '{reps}', '{tips}', '{json.dumps(alternatives)}', '{json.dumps(affected_muscles)}');
                """

                cursor.execute(query)
                conn.commit()
    
        print("[INFO] Dados inseridos com sucesso!")
    except Exception as error:
        print(f"[ERROR] Erro ao inserir dados: {error}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()