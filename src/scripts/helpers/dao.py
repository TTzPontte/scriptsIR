import json
import logging
from dataclasses import dataclass
from decimal import Decimal
import boto3

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Dao:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

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
