# %%
import logging
import uuid
from dataclasses import dataclass, field

import pandas

from src.scripts.helpers.dao import Dao
from src.scripts.helpers.local_dao import LocalDynamoDBDAO

# Import external functions and modules

# Constants
INPUT_DOCUMENT_PATH = '/Users/Mr-i-me/PycharmProjects/my_scripts/Sam/sam-python-crud-sample/src/scripts/participants/input_data/installments.xlsx'


def uid() -> str: return uuid.uuid4().__str__()

import re

def remove_special_characters(input_string):
    pattern = r'[^a-zA-Z0-9\s]'
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string


@dataclass
class Facade:
    _ir_list: list = field(default_factory=list)
    response_list: list = field(default_factory=list)
    pdfs_list: list = field(default_factory=list)
    bad_contracts: list = field(default_factory=list)

    def __post_init__(self):
        self.local_dynamodb = LocalDynamoDBDAO(table_name='tax_ir_participants', endpoint_url='http://localhost:8000')
        self._dao2 = Dao('TaxReturnsDynamo-dev')

        self.records = self._dao2.get_all()
        # print(self.records)

    def process_records(self):
        total_records = len(self.records)
        logging.info(f"Total Records: {total_records}")
        self._participants = []
        self._unique_participant = {}
        try:
            for idx, contract in enumerate(self.records):
                contract_id = contract.get('TaxReturnId', None)
                participants = contract.get('participants', None)
                for participant in participants:
                    documentNumber = remove_special_characters(participant.get('documentNumber', ''))
                    _p = {
                        "id": uid(),
                        **participant
                    }

                    self._participants.append({'contractId': contract_id, **_p})

                    self._unique_participant[documentNumber] = _p
                    print(contract_id)

        except Exception as e:
            self.bad_contracts.append(e)

    def _save_records(self):
        pandas.DataFrame(self._unique_participant).to_excel('./_unique_participant.xlsx')


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
