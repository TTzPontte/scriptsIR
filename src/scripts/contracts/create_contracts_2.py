import json
import logging
from decimal import Decimal
import boto3

from src.scripts.helpers.dao import Dao

# from src.scripts.local import LocalDynamoDBDAO

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        self.taxReturns_balance_dao = Dao('taxReturns_balance')
        self.scripts_ir_balance_dao = Dao('scripts-ir-balance')

    def process(self):
        self.taxReturns_balance_records = self.taxReturns_balance_dao.get_all()
        taxReturns_balance_records = self.taxReturns_balance_records
        # db_records_ids = [int(record['id']) for record in db_records]
        for record in taxReturns_balance_records:
            print(record.keys())
            contract_id = record['contract_id']
            self.scripts_ir_balance_dao.create_item(
                {"contractId": contract_id, 'balace': record['balance'], 'total': record['total_paid']})

    def save_to_json(self, output_json_file):
        pass
        # response = self.dao.scan_table()
        # with open(output_json_file, 'w') as json_file:
        #     json.dump(response, json_file, default=str, indent=2)


if __name__ == "__main__":
    input_json_file = 'contracts_2.json'  # Replace with the actual JSON file path
    table_name = 'Klavi-ClosedStatement-staging'  # Replace with your DynamoDB table name

    facade = Facade(table_name)
    facade.process()

    output_json_file = 'dynamodb_data.json'  # Specify the output JSON file path
    facade.save_to_json(output_json_file)
