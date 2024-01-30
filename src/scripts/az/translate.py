import json
import requests
from dataclasses import dataclass
import logging

from src.scripts.helpers.config import AZT_API_TOKEN


@dataclass
class DataNormalizer:
    translation_mapping: dict = None

    def __post_init__(self):
        if self.translation_mapping is None:
            self.translation_mapping = load_json(filename='translation_words.json')

    def normalize_data(self, response_data):
        return self._normalize(response_data)

    def _normalize(self, data):
        if isinstance(data, dict):
            return {self.translation_mapping.get(k, k): self._normalize(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._normalize(item) for item in data]
        else:
            return data


@dataclass
class AztronicHelper:
    BASE_URL: str = 'https://srv1.aztronic.com.br/az/apicollect/api/cliente/'

    def __post_init__(self):
        self.headers = {
            'Authorization': f'Bearer {AZT_API_TOKEN}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint: str):
        url = f'{self.BASE_URL}{endpoint}'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            json_response = response.json()

            # Normalize the data
            data_normalizer = DataNormalizer()
            normalized_data = data_normalizer.normalize_data(json_response)

            return normalized_data
        except requests.exceptions.RequestException as err:
            logging.error(f"Error: {err}")
            return None

    def get_client_email(self, cnpj_cpf: str):
        client_data = self.get_client(cnpj_cpf)
        return client_data.get('cliente', {}).get('email')

    def get_ir(self, uuid: str, year='2023'):
        endpoint = f'GetInformeIR/{uuid}/{year}'
        return self._make_request(endpoint).get('informeir')

    def get_client(self, cpf_cnpj: str):
        endpoint = f'GetCliente/{cpf_cnpj}'
        return self._make_request(endpoint)

    def get_financial_position(self, client_id: str):
        endpoint = f'GetPosicaoFinanceira/{client_id}'
        return self._make_request(endpoint).get('financial_position')


def load_json(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)


def main():
    # Example usage
    contract_id = '130200'  # Replace with a valid contract ID
    aztronic_helper = AztronicHelper()
    ir_data = aztronic_helper.get_ir(contract_id)
    if ir_data is not None:
        print(ir_data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    main()
