import logging
from decimal import Decimal
from src.scripts.helpers.dao import Dao  # Import Dao from the appropriate location

LOG_FILE_PATH = 'output/create_facade.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ContractsDao:
    def __init__(self, table_name='tax_ir_balance'):
        self.dao = Dao(table_name)
        self.participants_dao = Dao(table_name='tax_ir_participants')
        self.installments_dao = Dao(table_name='tax_ir_installments')

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
            _id = contract.get('contract_id')
            balance = Decimal(contract.get('balance', 0))

            # Retrieve installments and calculate total paid
            installments = self.installments_dao.get_by_secondary_index('tax_ir_contractId_gsi', str(contract_id))
            total_paid = self.sum_installment_values(installments)

            # Retrieve participants
            participants = self.participants_dao.get_by_secondary_index('tax_ir_contractId_gsi', str(contract_id))

            new_record = {
                'contract_id': str(_id),
                "balance": balance,
                "total_paid": total_paid,
                "installments": installments,
                "participants": participants,
            }

            return new_record
        else:
            return None


if __name__ == '__main__':
    # Example usage of ContractsDao

    # Create an instance of ContractsDao
    contracts_dao = ContractsDao()

    # Example contract data

    # Get a contract by ID
    contract_id = '130458'
    new_contract_record = contracts_dao.make_contract(contract_id)
    if new_contract_record:
        print(f"Created Contract: {new_contract_record}")
    else:
        print(f"Contract with ID {contract_id} not found.")
