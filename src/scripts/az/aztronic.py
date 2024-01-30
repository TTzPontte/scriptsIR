import requests
from dataclasses import dataclass, field
from config import AZT_API_TOKEN  # Ensure AZT_API_TOKEN is set in your config.py


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
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")

    def get_client_email(self, cnpj_cpf: str):
        client_data = self.get_client(cnpj_cpf)
        return client_data.get('cliente', {}).get('email')

    def get_ir(self, uuid: str, year='2022'):
        endpoint = f'GetInformeIR/{uuid}/{year}'
        return self._make_request(endpoint)

    def get_client(self, cpf_cnpj: str):
        endpoint = f'GetCliente/{cpf_cnpj}'
        return self._make_request(endpoint)

    def get_financial_position(self, client_id: str):
        endpoint = f'GetPosicaoFinanceira/{client_id}'
        return self._make_request(endpoint)

@dataclass
class AztronicContractDao:
    contract_id: str = ''
    _ir: dict = field(default_factory=dict)
    _financial_position: dict = field(default_factory=dict)

    def process(self):
        aztronic_helper = AztronicHelper()

        try:
            self._ir = aztronic_helper.get_ir(self.contract_id)
            self._financial_position = aztronic_helper.get_financial_position(self.contract_id)
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    facade = AztronicContractDao(contract_id='130200')  # Replace with a valid contract ID
    facade.process()
    print("IR Data:", facade._ir)
    print("Financial Position Data:", facade._financial_position)
