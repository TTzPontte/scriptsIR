import logging
import uuid
from dataclasses import dataclass, field
from decimal import Decimal

from src.scripts.helpers.local_dao import LocalDynamoDBDAO
from src.scripts.helpers.xlsx_helpers import csv_to_json

# Constants
INPUT_DOCUMENT_PATH = 'input_data/saldo.xlsx'


def uid() -> str:
    return uuid.uuid4().__str__()


@dataclass
class Facade:
    _ir_list: list = field(default_factory=list)
    response_list: list = field(default_factory=list)
    pdfs_list: list = field(default_factory=list)
    bad_contracts: list = field(default_factory=list)

    def __post_init__(self):
        self.records = csv_to_json(INPUT_DOCUMENT_PATH)
        self.tax_ir_balance_dao = LocalDynamoDBDAO(table_name='tax_ir_balance', endpoint_url='http://localhost:8000')
        # self.tax_ir_contracts_raw = Dao(table_name="taxReturns_balance")
        self.id_list = [record.get('contract_id') for record in self.records if
                        record.get('contract_id') is not None]

    def sum_installment_values(self, installments):
        return sum(Decimal(installment['value']) for installment in installments)

    def process_records(self):
        total_records = len(self.records)
        logging.info(f"Total Records: {total_records}")
        self.processed_records = []

        for _record in self.records:
            _id = _record.get('contractId', None)  # Ensure the key matches exactly with your data source
            balance = _record.get('balance', None)  # Ensure the key matches exactly with your data source
            print(_record)
            if [*_record].__len__() > 0:
                new_record = {
                    'contractId': str(_id),
                    "balance": balance,
                }
                self.tax_ir_balance_dao.put_item(new_record)
    # You might want to handle the processed data here (e.g., generating PDFs)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Initializing...")
    facade = Facade()
    print("Processing records...")
    facade.process_records()
    print("Generating PDFs...")
    # Add logic for generating PDFs here
