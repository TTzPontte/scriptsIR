


import boto3
import botocore
import sys
import json
import requests
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

sys.argv.append("dev")  # TODO: retirar; teste local
sys.argv.append("TaxReturns") # TODO: retirar; teste local

if len(sys.argv) > 1 and sys.argv[1] in ["dev", "prod", "test", "staging"]:
    env = sys.argv[1]
else:
    env = "dev"


if not sys.argv[2]:
    print("Nenhuma tabela mensionada")
    sys.exit(0)

dynamodb = boto3.resource("dynamodb")

dbTable = dynamodb.Table("{}.{}".format(sys.argv[2], env))
# dbTableRef = dynamodb.Table("{}.{}".format(sys.argv[2], "dev"))


def put_item(db, item):
    db.put_item(Item=item)


with open('irDataNovo2.txt', 'r', encoding='UTF8') as file:
    data = file.read()
    for ir in data:
        item = json.loads(json.dumps(ir), parse_float=Decimal) #Fix: TypeError: Float types are not supported. Use Decimal types instead.
        put_item(dbTable, item)

