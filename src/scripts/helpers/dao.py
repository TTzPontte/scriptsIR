import json
import logging
from dataclasses import dataclass
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import NoCredentialsError
from dataclasses import dataclass

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Dao:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def handle_no_credentials_error(self):
        raise Exception("No AWS credentials found. Ensure AWS credentials are configured.")

    def get_by_secondary_index(self, secondary_index_name, secondary_index_key):
        try:
            response = self.table.query(
                IndexName=secondary_index_name,
                KeyConditionExpression=Key('contractId').eq(secondary_index_key)
                # Replace with your secondary index key attribute name
            )
            return response.get('Items')
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def batch_create_items(self, items):
        items = [Dao.convert_floats_to_decimal(item) for item in items]
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    @staticmethod
    def convert_floats_to_decimal(data):
        if isinstance(data, float):
            return Decimal(str(data))
        elif isinstance(data, dict):
            return {key: Dao.convert_floats_to_decimal(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [Dao.convert_floats_to_decimal(item) for item in data]
        else:
            return data

    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def create_item(self, item):
        item = Dao.convert_floats_to_decimal(item)
        response = self.table.put_item(Item=item)
        return response

    def update_item(self, key, update_expression, expression_attribute_values):
        expression_attribute_values = Dao.convert_floats_to_decimal(expression_attribute_values)
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response

    def delete_item(self, key):
        response = self.table.delete_item(Key=key)
        return response

    def get_all(self):
        items = []
        last_evaluated_key = None

        while True:
            params = {'ExclusiveStartKey': last_evaluated_key} if last_evaluated_key else {}
            response = self.table.scan(**params)
            scanned_items = response.get('Items', [])
            last_evaluated_key = response.get('LastEvaluatedKey', None)

            items.extend(scanned_items)

            if not last_evaluated_key:
                break

        return items
