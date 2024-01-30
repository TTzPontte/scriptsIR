# %%
import logging
import uuid
from dataclasses import dataclass, field

from src.scripts.helpers.dao import Dao
from src.scripts.helpers.local_dao import LocalDynamoDBDAO

# Import external functions and modules

# Constants
INPUT_DOCUMENT_PATH = '/Users/Mr-i-me/PycharmProjects/my_scripts/Sam/sam-python-crud-sample/src/scripts/participants/input_data/installments.xlsx'


def uid() -> str: return uuid.uuid4().__str__()


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
        try:
            for idx, contract in enumerate(self.records):
                contract_id = contract.get('TaxReturnId', None)
                participants = contract.get('participants', None)
                for participant in participants:
                    _p = {
                        "id": uid(),
                        'contractId': contract_id,
                        **participant
                    }
                    self._participants.append(_p)
                    print(contract_id)

        except Exception as e:
            self.bad_contracts.append(e)

    def _save_records(self):
        for i in self._participants:
            print("item ___", i)
            item = self.local_dynamodb.put_item(i)


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
