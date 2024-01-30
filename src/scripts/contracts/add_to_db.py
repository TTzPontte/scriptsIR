import json

from src.scripts.helpers.dao import Dao


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
    # local_dynamodb = LocalDynamoDBDAO(table_name='az_posicao_financeira_raw', endpoint_url='http://localhost:8000')
    local_dynamodb = Dao(table_name='az_informe_ir_raw')

    json_file_name = 'input_data/_informeir_list.json'
    contracts_obj = load_json(json_file_name)
    participants_list = []
    if contracts_obj is not None:
        id_list = list(contracts_obj.keys())
        #
        for _id in id_list:
            item = contracts_obj.get(_id).get('informeir', None)
            if item is not None:
                _i = {
                    'id': _id,
                    'contract_id': _id,
                    **item
                }
                print(item)
                _item = local_dynamodb.create_item(_i)

# print(i)
# pass
