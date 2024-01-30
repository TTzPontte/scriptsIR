# %%
import pandas as pd
import requests as re


def getIR(id):
    header = {
        'Authorization': 'Basic QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ==',
        'Content-Type': 'application/json'
    }

    endpoint = 'https://srv1.aztronic.com.br/az/apicollect/api/cliente/{0}/{1}/2021'.format('GetInformeIR', id)

    dataIR = re.get(
        endpoint,
        headers=header
    ).json()

    return dataIR

    # api/cliente/GetInformeIR

    # if __name__ == '__main__':

def read_excel():
    pd.DataFrame.from_dict()


idd = 129241
resp = getIR(idd)
