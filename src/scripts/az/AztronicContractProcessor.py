import requests
from dataclasses import dataclass, field
from config import AZT_API_TOKEN  # Ensure AZT_API_TOKEN is set in your config.py

@dataclass
class AztronicApiClient:
    BASE_URL: str = 'https://srv1.aztronic.com.br/az/apicollect/api/cliente/'

    def __post_init__(self):
        self.headers = {
            'Authorization': f'Bearer {AZT_API_TOKEN}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, endpoint: str):
        """
        Make an HTTP GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.

        Returns:
            dict: JSON response data.
        """
        url = f'{self.BASE_URL}{endpoint}'
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP Error: {http_error}")
        except requests.exceptions.ConnectionError as connection_error:
            print(f"Connection Error: {connection_error}")
        except requests.exceptions.Timeout as timeout_error:
            print(f"Timeout Error: {timeout_error}")
        except requests.exceptions.RequestException as request_error:
            print(f"Request Error: {request_error}")

    def get_client_email(self, cnpj_cpf: str):
        """
        Get the email of a client using their CNPJ/CPF.

        Args:
            cnpj_cpf (str): CNPJ or CPF of the client.

        Returns:
            str: The client's email.
        """
        client_data = self.fetch_client_data(cnpj_cpf)
        return client_data.get('cliente', {}).get('email')

    def fetch_ir_data(self, uuid: str, year='2022'):
        """
        Fetch IR (Informe de Rendimentos) data for a specific UUID and year.

        Args:
            uuid (str): The UUID of the contract.
            year (str): The year for which to fetch IR data (default is '2022').

        Returns:
            dict: IR data.
        """
        endpoint = f'GetInformeIR/{uuid}/{year}'
        return self._make_request(endpoint)

    def fetch_client_data(self, cpf_cnpj: str):
        """
        Fetch client data using their CNPJ/CPF.

        Args:
            cpf_cnpj (str): CNPJ or CPF of the client.

        Returns:
            dict: Client data.
        """
        endpoint = f'GetCliente/{cpf_cnpj}'
        return self._make_request(endpoint)

    def fetch_financial_position(self, client_id: str):
        """
        Fetch financial position data for a specific client.

        Args:
            client_id (str): The ID of the client.

        Returns:
            dict: Financial position data.
        """
        endpoint = f'GetPosicaoFinanceira/{client_id}'
        return self._make_request(endpoint)

import logging
from dataclasses import dataclass

# Configure logging at the beginning of the script
logging.basicConfig(level=logging.INFO)


# Define data classes for better structure and readability
@dataclass
class ContractInfo:
    balance: float
    block: str
    base_year: str
    contract_number: int
    date: str
    development: str
    email: str
    unit: str


@dataclass
class ParticipantInfo:
    name: str
    email: str
    documentNumber: str
    participationPercentage: float


@dataclass
class InstallmentInfo:
    amountPayed: float
    creditDate: str
    payedInstallment: str
    contractinfoID: str

@dataclass
class AztronicContractProcessor:
    contract_id: str = ''
    ir_data: dict = field(default_factory=dict)
    financial_position_data: dict = field(default_factory=dict)

    def process(self):
        api_client = AztronicApiClient()

        try:
            self.ir_data = api_client.fetch_ir_data(self.contract_id)
            self.financial_position_data = api_client.fetch_financial_position(self.contract_id)
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    contract_id = '130200'  # Replace with a valid contract ID
    contract_processor = AztronicContractProcessor(contract_id=contract_id)
    contract_processor.process()
    print("IR Data:", contract_processor.ir_data)
    print("Financial Position Data:", contract_processor.financial_position_data)



