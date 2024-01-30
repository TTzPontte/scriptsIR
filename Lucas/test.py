# %%
from dataclasses import field, dataclass

import requests as re

from Lucas.helpers import csv_to_json

DOCUMENT_PATH = '/Data/data_file.xlsx'


@dataclass
class Facade:
    _current_id: str = ''
    _ir_list: list = field(default_factory=list)
    records: list = field(default_factory=list)
    id_list: list = field(default_factory=list)

    def __post_init__(self):
        xlsx = csv_to_json(DOCUMENT_PATH)
        print(xlsx)
        self.records = xlsx
        self.id_list = [i.get('Identificador do Contrato') for i in xlsx if
                        i.get('Identificador do Contrato') is not None]

    def get_ir(self):
        header = {
            'Authorization': 'Basic QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ==',
            'Content-Type': 'application/json'
        }

        endpoint = 'https://srv1.aztronic.com.br/az/apicollect/api/cliente/{0}/{1}/2021'.format('GetInformeIR',
                                                                                                self._current_id)

        response = re.get(
            endpoint,
            headers=header
        ).json()
        self._ir_list.append(response)
        return response

        # api/cliente/GetInformeIR

        # if __name__ == '__main__':

    def process(self):
        for i in self.records:
            # print(i)
            uuid = i.get('Identificador do Contrato')
            print("uuid", uuid)
            self._current_id = str(uuid)
            self.get_ir()
            # self.get_ir(i)


if __name__ == '__main__':
    _f = Facade()
    _f.process()

    # idd = 129241
    # resp = getIR(idd)
    # x = csv_to_json(url)


# {contractInfo, participants, receiverInfo, installments }

def receiver_info():
    return {
        'receiver': "MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO",
        'cnpj': "30.982.547/0001-09",
        'address': "AV BRIGADEIRO FARIA LIMA, 2277 - SÃO PAULO",
        'date': "SÃO PAULO, 05 DE FEVEREIRO DE 2021"
    }


