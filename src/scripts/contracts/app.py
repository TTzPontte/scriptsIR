import json
import logging
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import NoCredentialsError

from src.scripts.helpers.dao import Dao

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class LocalDynamoDBDAO:
    def __init__(self, table_name, endpoint_url='http://localhost:8000'):
        self.table_name = table_name
        self.endpoint_url = endpoint_url
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        self.table = self.dynamodb.Table(table_name)
        self.secondary_index_name = 'tax_ir_contractId_gsi'  # Replace with your secondary index name

    def handle_no_credentials_error(self):
        raise Exception("No AWS credentials found. Ensure AWS credentials are configured.")

    @staticmethod
    def convert_floats_to_decimal(data):
        if isinstance(data, float):
            return Decimal(str(data))
        elif isinstance(data, dict):
            return {key: LocalDynamoDBDAO.convert_floats_to_decimal(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [LocalDynamoDBDAO.convert_floats_to_decimal(item) for item in data]
        else:
            return data

    def put_item(self, item):
        try:
            item = self.convert_floats_to_decimal(item)
            response = self.table.put_item(Item=item)
            return response
        except NoCredentialsError as e:
            print(e)
            self.handle_no_credentials_error()

    def get_by_secondary_index(self, secondary_index_key):
        try:
            response = self.table.query(
                IndexName=self.secondary_index_name,
                KeyConditionExpression=Key('contractId').eq(secondary_index_key)
                # Replace with your secondary index key attribute name
            )
            return response.get('Items')
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def get_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def update_item(self, key, update_expression, expression_attribute_values):
        try:
            expression_attribute_values = self.convert_floats_to_decimal(expression_attribute_values)
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return response
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def delete_item(self, key):
        try:
            response = self.table.delete_item(Key=key)
            return response.get('Attributes')
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def scan(self):
        try:
            response = self.table.scan()
            return response.get('Items')
        except NoCredentialsError:
            self.handle_no_credentials_error()


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
        self.installments_dao = LocalDynamoDBDAO(table_name='tax_ir_installments', endpoint_url='http://localhost:8000')

    def process(self):
        db_records = self.dao.get_all()
        # db_records_ids = [int(record['id']) for record in db_records]
        for record in db_records:
            contract_id = record.get('TaxReturnId')
            contract_info = record.get('Contract')
            installments = self.installments_dao.get_by_secondary_index(contract_id)
            print(installments)

            # self.local_dynamodb.put_item({"contract_id": record_id['id'], **record_id})

    def get_participants(self):
        participants = self.local_dynamodb.get_by_secondary_index()
    def save_to_json(self, output_json_file):
        pass
        # response = self.dao.scan_table()
        # with open(output_json_file, 'w') as json_file:
        #     json.dump(response, json_file, default=str, indent=2)


if __name__ == "__main__":
    input_json_file = 'contracts_2.json'  # Replace with the actual JSON file path
    table_name = 'TaxReturnsDynamo-dev'  # Replace with your DynamoDB table name

    facade = Facade(table_name)
    facade.process()

    output_json_file = 'dynamodb_data.json'  # Specify the output JSON file path
    facade.save_to_json(output_json_file)
