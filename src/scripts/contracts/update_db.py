import json
import logging

from src.scripts.helpers.dao import Dao
from src.scripts.local import LocalDynamoDBDAO

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def load_json(input_json_file):
    try:
        with open(input_json_file, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise e


class Facade:
    def __init__(self, table_name='taxReturns_ir_list'):
        self.table_name = table_name
        self.prod_dao = Dao(self.table_name)
        self.local_dynamodb = LocalDynamoDBDAO(table_name='tax_ir_contracts_raw', endpoint_url='http://localhost:8000')
        self.installments_dao = LocalDynamoDBDAO(table_name='tax_ir_installments', endpoint_url='http://localhost:8000')

    def process(self):
        db_records = self.prod_dao.get_all()
        # db_records_ids = [int(record['id']) for record in db_records]
        for record in db_records:
            print(record)
            contract_id = record.get('TaxReturnId')
            contract_info = record.get('Contract')
            # installments = self.installments_dao.get_by_secondary_index(contract_id)
            # print(installments)

            # self.local_dynamodb.put_item({"contract_id": record_id['id'], **record_id})

    def save_to_json(self):
        output_json_file = f'output/dynamodb_data__{self.table_name}.json'  # Specify the output JSON file path

        response = self.prod_dao.get_all()
        with open(output_json_file, 'w') as json_file:
            json.dump(response, json_file, default=str, indent=2)


if __name__ == "__main__":
    facade = Facade()
    # facade.process()

    facade.save_to_json()
