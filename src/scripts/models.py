import logging
from dataclasses import dataclass

# Configure logging at the beginning of the script
logging.basicConfig(level=logging.INFO)


# Define data classes for better structure and readability
@dataclass
class ContractInfo:
    total: float
    balance: float
    base_year: str
    development: str
    contract_number: int
    date: str


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
