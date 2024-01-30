import logging
import uuid
from dataclasses import dataclass, field
from decimal import Decimal

from src.scripts.helpers.dao import Dao
from src.scripts.xlsx_helpers import csv_to_json

# Constants
INPUT_DOCUMENT_PATH = 'input_data/saldo.xlsx'


def uid() -> str:
    return uuid.uuid4().__str__()

from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import NoCredentialsError


class LocalDynamoDBDAO:
    def __init__(self, table_name, endpoint_url='http://localhost:8000', secondary_index_name='tax_ir_contractId_gsi'):
        self.table_name = table_name
        self.endpoint_url = endpoint_url
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        self.table = self.dynamodb.Table(table_name)
        self.secondary_index_name = secondary_index_name

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


@dataclass
class Facade:
    _ir_list: list = field(default_factory=list)
    response_list: list = field(default_factory=list)
    pdfs_list: list = field(default_factory=list)
    bad_contracts: list = field(default_factory=list)

    def __post_init__(self):
        self.records = csv_to_json(INPUT_DOCUMENT_PATH)
        self.installments_dao = LocalDynamoDBDAO(table_name='tax_ir_installments', endpoint_url='http://localhost:8000')
        self.participants_dao = LocalDynamoDBDAO(table_name='tax_ir_participants', endpoint_url='http://localhost:8000')
        # self.tax_ir_contracts_raw = LocalDynamoDBDAO(table_name='tax_ir_contracts_raw', endpoint_url='http://localhost:8000')
        self.tax_ir_contracts_raw = Dao(table_name="taxReturns_balance")

    def sum_installment_values(self, installments):
        return sum(Decimal(installment['value']) for installment in installments)

    def process_records(self):
        total_records = len(self.records)
        logging.info(f"Total Records: {total_records}")
        self.processed_records = []

        for _record in self.records:
            _id = _record.get('ID', None)  # Ensure the key matches exactly with your data source
            balance = _record.get('balance', None)  # Ensure the key matches exactly with your data source
            if _id is not None:
                installments = self.installments_dao.get_by_secondary_index(str(_id))
                total_paid = self.sum_installment_values(installments)  # Summing installment values
                # print(_id)
                participants = self.participants_dao.get_by_secondary_index(str(_id))
                # print(participants)

                new_record = {
                    'contract_id': str(_id),
                    "balance": balance,
                    "total_paid": total_paid,  # Storing total paid value
                    "installments": installments,
                    "participants": participants,
                }
                self.response_list.append(new_record)  # Storing the processed record
                self.tax_ir_contracts_raw.create_item(new_record)
        # You might want to handle the processed data here (e.g., generating PDFs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Initializing...")
    facade = Facade()
    print("Processing records...")
    facade.process_records()
    print("Generating PDFs...")
    # Add logic for generating PDFs here
