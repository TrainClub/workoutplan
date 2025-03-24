import boto3
from botocore.exceptions import ClientError

class DynamoDBHelper:
    def __init__(self, table_name):
        """
        Initialize the DynamoDB helper with the table name.
        """
        self.dynamodb = boto3.client('dynamodb')
        self.table = table_name

    def put_item(self, item):
        """
        Insert an item into the DynamoDB table.
        :param item: A dictionary containing the item to insert.
        :return: Response from DynamoDB.
        """
        try:
            response = self.dynamodb.put_item(TableName=self.table,
                                               Item=item)
            return response
        except ClientError as e:
            print(f"Error occurred: {e}")
            raise e

    def get_item(self, key):
        """
        Retrieve an item from the DynamoDB table.
        :param key: A dictionary containing the primary key of the item.
        :return: The retrieved item.
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            raise e