#%%
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
    cnpj_cpf: str
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
        cnpj_cpf=informeiro_data['cnpj_empresa'],
        dt_contrato=informeiro_data['dt_contrato'],
        saldo=informeiro_data['saldo'],
        participantes=participantes,
        pagamentos=pagamentos
    )


@dataclass
class IR:
    data: Informeiro

    def make_parcela(self, pmt):
        return {
            'creditDate': pmt.mes,
            'payedInstallment': f"{pmt.mes} - Mensal",
            'amoutPayed': pmt.valor_pago
        }

    def participantes(self, i):
        return {
            "name": i.nome,
            "documentNumber": i.cnpj_cpf,
            "participation": i.participacao
        }

    def run(self):
        self.installments = [self.make_parcela(i) for i in self.data.pagamentos]
        self.participants = [self.participantes(i) for i in self.data.participantes]
        self.contractInfo = {'SALDO': self.data.saldo}


if __name__ == '__main__':
    response = {
        'informeir': {
            'empresa': 'True Securitizadora ',
            'cnpj_empresa': '12130744000100',
            'dt_contrato': '2019-07-17T00:00:00',
            'saldo': 958728.43,
            'participantes': [
                {'cnpj_cpf': '19433573668',
                 'nome': 'LEONARDO DUTRA DE MORAES HORTA',
                 'participacao': 50.0},
                {'cnpj_cpf': '57599521704',
                 'nome': 'MARIA CRISTINA BREGA BALDI HORTA',
                 'participacao': 50.0}],
            'pagamentos': [
                {'mes': 1, 'valor_pago': 18767.56},
                {'mes': 2, 'valor_pago': 0.0},
                {'mes': 3, 'valor_pago': 17612.56},
                {'mes': 4, 'valor_pago': 17654.02},
                {'mes': 5, 'valor_pago': 0.0},
                {'mes': 6, 'valor_pago': 17720.27},
                {'mes': 7, 'valor_pago': 9195.67},
                {'mes': 8, 'valor_pago': 0.0},
                {'mes': 9, 'valor_pago': 0.0},
                {'mes': 10, 'valor_pago': 0.0},
                {'mes': 11, 'valor_pago': 0.0},
                {'mes': 12, 'valor_pago': 0.0}]
        }
    }

    p = parse_json(response)
    # print(p)
    xx = IR(p)
    print(xx)