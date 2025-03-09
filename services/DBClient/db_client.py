import psycopg2
from services.AWSClient.aws_services import parameter_store
import json 

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
    except Exception as error:
        print(f'[ERROR] Nao foi possivel estabelecer conexao, erro: {error}')

def insert_data():
    pass