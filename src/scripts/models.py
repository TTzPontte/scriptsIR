import logging
from dataclasses import dataclass

# Configure logging at the beginning of the script
logging.basicConfig(level=logging.INFO)


# Define data classes for better structure and readability
@dataclass
class Contract:
    id: str
    total: float
    balance: float
    base_year: str
    development: str
    contract_number: int
    date: str


@dataclass
class Participant:
    name: str
    email: str
    documentNumber: str
    participationPercentage: float
    contractId: str


@dataclass
class Installment:
    amountPayed: float
    creditDate: str
    payedInstallment: str
    contractId: str
