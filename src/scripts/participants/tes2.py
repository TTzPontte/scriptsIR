import json

from src.scripts.helpers.dao import Dao
from src.scripts.local import LocalDynamoDBDAO


def load_json(input_json_file):
    try:
        with open(input_json_file, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"File '{input_json_file}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{input_json_file}': {e}")
    return None


if __name__ == "__main__":
    local_dynamodb = LocalDynamoDBDAO(table_name='az_cliente_raw', endpoint_url='http://localhost:8000')
    # local_dynamodb = Dao(table_name='az_cliente_raw')

    json_file_name = '__test__.json'
    contracts_obj = load_json(json_file_name)
    participants_list = []
    if contracts_obj is not None:
        id_list = list(contracts_obj.keys())
        print(contracts_obj)

        for _id in id_list:
            item = contracts_obj.get(_id)
            for i in item:
                _i = {
                    'contract_id': _id,
                    **i
                }
                print(_i)
            _item = local_dynamodb.put_item(_i)

            # print(i)
            # pass
