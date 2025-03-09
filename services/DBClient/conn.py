import psycopg2
from psycopg2 import sql

def dbconnect():
    try:
        print('[INFO] Iniciando conexao com banco de dados.')
        connection = psycopg2.connect(
            host="localhost",  # e.g. "localhost"
            database="biotrainningdb",  # e.g. "fitness_app"
            user="postgres",  # e.g. "postgres"
            password="Alfa1204@"  # e.g. "password123"
        )
    except Exception as error:
        print(f'[ERROR] Nao foi possivel estabelecer conexao, erro: {error}')