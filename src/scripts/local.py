from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import NoCredentialsError

class LocalDynamoDBDAO:
    def __init__(self, table_name, endpoint_url='http://localhost:8000', secondary_index_name='tax_ir_contractId_gsi'):
        self.table_name = table_name
        self.endpoint_url = endpoint_url
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        self.table = self.dynamodb.Table(table_name)
        self.secondary_index_name = secondary_index_name

    def handle_no_credentials_error(self):
        raise Exception("No AWS credentials found. Ensure AWS credentials are configured.")

    @staticmethod
    def convert_floats_to_decimal(data):
        if isinstance(data, float):
            return Decimal(str(data))
        elif isinstance(data, dict):
            return {key: LocalDynamoDBDAO.convert_floats_to_decimal(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [LocalDynamoDBDAO.convert_floats_to_decimal(item) for item in data]
        else:
            return data

    def put_item(self, item):
        try:
            item = self.convert_floats_to_decimal(item)
            response = self.table.put_item(Item=item)
            return response
        except NoCredentialsError as e:
            print(e)
            self.handle_no_credentials_error()

    def get_by_secondary_index(self, secondary_index_key):
        try:
            response = self.table.query(
                IndexName=self.secondary_index_name,
                KeyConditionExpression=Key('contractId').eq(secondary_index_key)
                # Replace with your secondary index key attribute name
            )
            return response.get('Items')
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def get_item(self, key):
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def update_item(self, key, update_expression, expression_attribute_values):
        try:
            expression_attribute_values = self.convert_floats_to_decimal(expression_attribute_values)
            response = self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return response
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def delete_item(self, key):
        try:
            response = self.table.delete_item(Key=key)
            return response.get('Attributes')
        except NoCredentialsError:
            self.handle_no_credentials_error()

    def scan(self):
        try:
            response = self.table.scan()
            return response.get('Items')
        except NoCredentialsError:
            self.handle_no_credentials_error()

if __name__ == "__main__":
    # Create an instance of LocalDynamoDBDAO
    local_dynamodb = LocalDynamoDBDAO(table_name='tax_ir_participants', endpoint_url='http://localhost:8000', secondary_index_name="contractId")

    # Example: Query data by secondary index
    secondary_index_key_value = '130026'  # Replace with the value you want to query
    items = local_dynamodb.get_by_secondary_index(secondary_index_key_value)
    print(items)

    # ... Other example operations ...

