import json
import logging
from decimal import Decimal
import boto3

from src.scripts.local import LocalDynamoDBDAO

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Dao:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    @staticmethod
    def convert_to_decimal(data):
        if isinstance(data, (float, Decimal)):
            return Decimal(str(data))
        elif isinstance(data, dict):
            return {key: Dao.convert_to_decimal(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [Dao.convert_to_decimal(item) for item in data]
        else:
            return data

    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response.get('Item')

    def create_item(self, item):
        item = Dao.convert_to_decimal(item)
        response = self.table.put_item(Item=item)
        return response

    def update_item(self, key, update_expression, expression_attribute_values):
        expression_attribute_values = Dao.convert_to_decimal(expression_attribute_values)
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response

    def delete_item(self, key):
        response = self.table.delete_item(Key=key)
        return response

    def scan_table(self):
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


def load_json(input_json_file):
    try:
        with open(input_json_file, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise e


class Facade:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dao = Dao(table_name)
        self.local_dynamodb = LocalDynamoDBDAO(table_name='tax_ir_contracts_raw', endpoint_url='http://localhost:8000')

    def process(self):
        db_records = self.dao.scan_table()
        # db_records_ids = [int(record['id']) for record in db_records]
        for record_id in db_records:
            print(record_id)
            self.local_dynamodb.put_item({"contract_id": record_id['id'], **record_id})

    def save_to_json(self, output_json_file):
        response = self.dao.scan_table()
        with open(output_json_file, 'w') as json_file:
            json.dump(response, json_file, default=str, indent=2)


if __name__ == "__main__":
    input_json_file = 'contracts_2.json'  # Replace with the actual JSON file path
    table_name = 'Klavi-ClosedStatement-staging'  # Replace with your DynamoDB table name

    facade = Facade(table_name)
    facade.process()

    output_json_file = 'output/dynamodb_data.json'  # Specify the output JSON file path
    facade.save_to_json(output_json_file)
