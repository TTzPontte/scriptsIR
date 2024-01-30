import logging
import uuid
from dataclasses import dataclass, field
from src.scripts.helpers.local_dao import LocalDynamoDBDAO
from src.scripts.helpers.xlsx_helpers import csv_to_json

# Constants
INPUT_DOCUMENT_PATH = 'output/modified_installments.xlsx'


def generate_unique_id() -> str:
    return str(uuid.uuid4())


@dataclass
class InstallmentsFacade:
    bad_contracts: list = field(default_factory=list)

    def __post_init__(self):
        self.records = csv_to_json(INPUT_DOCUMENT_PATH)
        self.local_dynamodb = LocalDynamoDBDAO(
            table_name='tax_ir_installments',
            endpoint_url='http://localhost:8000'
        )

    def process_records(self):
        total_records = len(self.records)
        logging.info(f"Total Records: {total_records}")
        self.processed_records = []
        for idx, contract in enumerate(self.records):
            contract_id = contract.get('contractId')
            if contract_id:
                record = {
                    "id": generate_unique_id(),
                    **contract,
                    "contractId": str(contract_id)
                }
                self.processed_records.append(record)
            else:
                self.bad_contracts.append(f"Missing 'contractId' in record {idx + 1}")

    def save_records(self):
        for record in self.processed_records:
            self.local_dynamodb.put_item(record)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Initializing...")
    facade = InstallmentsFacade()
    print("Processing records...")
    facade.process_records()

    if facade.bad_contracts:
        for error in facade.bad_contracts:
            logging.error(error)

    print("Saving records to DynamoDB...")
    facade.save_records()
    print("DONE!")
