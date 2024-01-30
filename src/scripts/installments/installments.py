import logging
from dataclasses import dataclass, field

from src.scripts.helpers.local_dao import LocalDynamoDBDAO
from src.scripts.xlsx_helpers import csv_to_json

# Import external functions and modules

# Constants
INPUT_DOCUMENT_PATH = 'input_data/installments.xlsx'
import uuid


def uid() -> str: return uuid.uuid4().__str__()


@dataclass
class Facade:
    _ir_list: list = field(default_factory=list)
    response_list: list = field(default_factory=list)
    pdfs_list: list = field(default_factory=list)
    bad_contracts: list = field(default_factory=list)

    def __post_init__(self):
        self.local_dynamodb = LocalDynamoDBDAO(table_name='tax_ir_installments', endpoint_url='http://localhost:8000')
        self.records = self.local_dynamodb.scan()

    def process_records(self):
        total_records = len(self.records)
        logging.info(f"Total Records: {total_records}")
        self.processed_records = []
        try:
            for idx, contract in enumerate(self.records):
                contract_id = contract.get('id', None)
                self.processed_records.append({"id":contract_id})
                print(contract_id)

        except Exception as e:
            self.bad_contracts.append(e)

    def _save_records(self):
        for i in self.processed_records:
            item = self.local_dynamodb.delete_item(i)
            print(item)


if __name__ == '__main__':
    print("Initializing...")
    facade = Facade()
    print("Processing records...")
    facade.process_records()
    print("Generating PDFs...")
    items = facade.local_dynamodb.scan()
    print(items)
    facade._save_records()
    print("DONE!")
