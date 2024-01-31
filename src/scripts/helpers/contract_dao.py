import json
import logging
from decimal import Decimal
from pprint import PrettyPrinter

import requests
from openpyxl import Workbook

from src.scripts.helpers.dao import Dao  # Import Dao from the appropriate location

pp = PrettyPrinter(indent=4).pprint

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ContractsDao:
    def __init__(self, table_name='tax_ir_balance'):
        self.dao = Dao(table_name)
        self.participants_dao = Dao(table_name='tax_ir_participants')
        self.installments_dao = Dao(table_name='tax_ir_installments')
        self.ir_list_dao = Dao(table_name='taxReturns_ir_list')

    def get_contract_by_id(self, contract_id):
        key = {'contractId': contract_id}
        return self.dao.get_item(key)

    def sum_installment_values(self, installments):
        total = Decimal(0)
        for installment in installments:
            total += Decimal(installment.get('value', 0))
        return total

    def make_contract(self, contract_id):

        contract = self.get_contract_by_id(contract_id)
        if contract:
            # Extract relevant contract data
            balance = Decimal(contract.get('balance', 0))

            # Retrieve installments and calculate total paid
            installments = self.installments_dao.get_by_secondary_index('tax_ir_contractId_gsi', str(contract_id))

            # Retrieve participants
            participants = self.participants_dao.get_by_secondary_index('tax_ir_contractId_gsi', str(contract_id))

            ir_list = self.ir_list_dao.get_item({'id': contract_id})

            new_record = {
                "total": contract['total'],
                "development": "PONTTE - HOME EQUITY",
                "date": ir_list['data'],
                'contractNumber': str(contract_id),
                "baseYear": "2023",
                "balance": balance,
                "Installments": {'items': installments},
                "Participants": {'items': participants},
            }

            return new_record
        else:
            return None


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Convert Decimal to string for JSON serialization
        return super(DecimalEncoder, self).default(obj)


def main():
    dao = Dao('tax_ir_balance')
    contracts = dao.get_all()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Contract Data"
    sheet["A1"] = "ContractId"
    sheet["B1"] = "URL"

    i = 2  # Start from row 2, as the first row is for headers
    # for contract in contracts:
    # if i <= 12:  # Adjusted to include 100 records
    contractId = '130431'
    print(i)
    new_contract_record = contracts_dao.make_contract(contractId)
    json_data = json.dumps(new_contract_record, cls=DecimalEncoder, indent=4)
    api_url = 'https://gse2clq54c.execute-api.us-east-1.amazonaws.com/Prod/tax-returns/pdf'
    payload = {
        "data": {
            "getContractInfo": json.loads(json_data)
        }
    }
    headers = {'Content-Type': 'application/json'}
    print(json.dumps(payload))
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    print(response.text)
    # Write data to Excel sheet
    sheet[f"A{i}"] = contractId
    sheet[f"B{i}"] = response.text

    i += 1


if __name__ == '__main__':
    # Example usage of ContractsDao

    # Create an instance of ContractsDao
    contracts_dao = ContractsDao()

    # Example contract data
    main()
    # Get a contract by ID
    # contract_id = '130458'
    # new_contract_record = contracts_dao.make_contract(contract_id)
    #
    # if new_contract_record:
    #     json_data = json.dumps(new_contract_record, cls=DecimalEncoder, indent=4)
    #     print(json_data)
    # else:
    #     print(f"Contract with ID {contract_id} not found.")
