import awswrangler as wr
import boto3
from botocore.exceptions import ClientError

def parameter_store(parameter_name, with_decryption=False):
    try:
        print('[INFO] obtendo parametro.')

        ssm = boto3.client('ssm')
        
        response = ssm.get_parameter(
            Name=parameter_name, 
            WithDecryption=with_decryption
        )
        
        parameter_value = response['Parameter']['Value']
        print(f'[INFO] Parametro retornado com sucesso: {parameter_name}')
        return parameter_value
    
    except ClientError as error:
        print(f'[ERROR] Não foi possível recuperar o parâmetro: {parameter_name}. Error: {error}')
        return None
    except KeyError as e:
        print(f'[ERROR] Formato de resposta inesperado do SSM: Chave ausente {e}')
        return None
    except Exception as error:
        print(f'[ERROR] Um erro inesperado ocorreu durante o a recuperacao: {parameter_name}. Error: {error}')
        return None