import json

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
    local_dynamodb = LocalDynamoDBDAO(table_name='tax_ir_participants_raw', endpoint_url='http://localhost:8000')

    json_file_name = '__test__.json'
    ids = load_json(json_file_name)
    participants_list = []
    if ids is not None:
        object_list = list(ids.values())

        for obj in object_list:
            print(ids)
            for i in obj:
                # _item = local_dynamodb.put_item(i)
                print(obj)
                print(i)