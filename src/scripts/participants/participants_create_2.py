# %%
import logging
import uuid
from dataclasses import dataclass, field

from src.scripts.helpers.dao import Dao
from src.scripts.helpers.local_dao import LocalDynamoDBDAO

# Import external functions and modules

# Constants
INPUT_DOCUMENT_PATH = '/Users/Mr-i-me/PycharmProjects/my_scripts/Sam/scripts-ir/src/scripts/participants/input_data/installments.xlsx'


def uid() -> str: return uuid.uuid4().__str__()


@dataclass
class Facade:
    _ir_list: list = field(default_factory=list)
    response_list: list = field(default_factory=list)
    pdfs_list: list = field(default_factory=list)
    bad_contracts: list = field(default_factory=list)

    def __post_init__(self):
        self.local_dynamodb = Dao('tax_ir_participants')

        self.records = self.local_dynamodb.get_all()
        # print(self.records)

    def process_records(self):
        total_records = len(self.records)
        logging.info(f"Total Records: {total_records}")
        self._participants = []
        try:
            for idx, contract in enumerate(self.records):
                participation = contract.get('participation', None)

                contract['participationPercentage'] = participation
                del contract['participation']
                print(contract.keys())
                self._participants.append(contract)
        except Exception as e:
            self.bad_contracts.append(e)

    def _save_records(self):
        for i in self._participants:
            print("item ___", i)
            item = self.local_dynamodb.create_item(i)


if __name__ == '__main__':
    print("Initializing...")
    facade = Facade()
    print("Processing records...")
    facade.process_records()
    print("Generating PDFs...")
    facade._save_records()
    print("DONE!")
