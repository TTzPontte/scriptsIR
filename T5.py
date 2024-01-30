from dataclasses import dataclass
from typing import List

@dataclass
class Participante:
    cnpj_cpf: str
    nome: str
    participacao: float

@dataclass
class Pagamento:
    mes: int
    valor_pago: float

@dataclass
class Informeiro:
    empresa: str
    cnpj_empresa: str
    dt_contrato: str
    saldo: float
    participantes: List[Participante]
    pagamentos: List[Pagamento]

def parse_json(data: dict) -> Informeiro:
    informeiro_data = data['informeir']
    participantes = [Participante(**participante) for participante in informeiro_data['participantes']]
    pagamentos = [Pagamento(**pagamento) for pagamento in informeiro_data['pagamentos']]
    return Informeiro(
        empresa=informeiro_data['empresa'],
        cnpj_empresa=informeiro_data['cnpj_empresa'],
        dt_contrato=informeiro_data['dt_contrato'],
        saldo=informeiro_data['saldo'],
        participantes=participantes,
        pagamentos=pagamentos
    )

@dataclass()
class IR:
    data: Informeiro

    def make_parcela(self, pmt):
        return {
            'creditDate': pmt.mes,
            'payedInstallment': f"{pmt.mes} - Mensal",
            'amoutPayed': pmt.valor_pago
        }

    def participants(self, participant):
        return {
            "name": participant.nome,
            "documentNumber": participant.cnpj_cpf,
            "participation": participant.participacao
        }

    def run(self):
        self.installments = [self.make_parcela(p) for p in self.data.pagamentos]
        self.participants = [self.participants(p) for p in self.data.participantes]
        self.contractInfo = {'SALDO': self.data.saldo}
