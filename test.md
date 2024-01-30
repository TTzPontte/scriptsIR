write a python parser for the logic bellow 


input

```json
{
  'informeir': {
    'empresa': 'True Securitizadora ',
    'cnpj_empresa': '12130744000100',
    'dt_contrato': '2019-07-17T00:00:00',
    'saldo': 958728.43,
    'participantes': [
      {
        'cnpj_cpf': '19433573668',
        'nome': 'LEONARDO DUTRA DE MORAES HORTA',
        'participacao': 50.0
      },
      {
        'cnpj_cpf': '57599521704',
        'nome': 'MARIA CRISTINA BREGA BALDI HORTA',
        'participacao': 50.0
      }
    ],
    'pagamentos': [
      {
        'mes': 1,
        'valor_pago': 18767.56
      },
      {
        'mes': 2,
        'valor_pago': 0.0
      },
      {
        'mes': 3,
        'valor_pago': 17612.56
      },
      {
        'mes': 4,
        'valor_pago': 17654.02
      },
      {
        'mes': 5,
        'valor_pago': 0.0
      },
      {
        'mes': 6,
        'valor_pago': 17720.27
      },
      {
        'mes': 7,
        'valor_pago': 9195.67
      },
      {
        'mes': 8,
        'valor_pago': 0.0
      },
      {
        'mes': 9,
        'valor_pago': 0.0
      },
      {
        'mes': 10,
        'valor_pago': 0.0
      },
      {
        'mes': 11,
        'valor_pago': 0.0
      },
      {
        'mes': 12,
        'valor_pago': 0.0
      }
    ]
  }
}
```

processing

```python
pmt = informeir['pagamento'][0]
installment = {'creditDate': pmt.mes,
               'payedInstallment': str(pmt.mes) + ' - Mensal',
               'amoutPayed': pmt.valor_pago
               }
```

output

```json
{
  "contractInfo": {
    "EMPREENDIMENTO": "PONTTE - HOME EQUITY",
    "CONTRATO": "129259",
    "ANO BASE": "2020",
    "BLOCO": "ÚNICO",
    "UNIDADE": "31",
    "DATA": "25/02/2021"
  },
  "installments": [
    {
      "creditDate": "30/12/2020",
      "payedInstallment": "12 - Mensal.",
      "amoutPayed": "R$ 18.822,13"
    }
  ],
  "participants": [
    {
      "name": "PADANIA CONSULTORIA EIRELI",
      "documentNumber": "06.109.309/0001-09",
      "participation": "0%"
    }
  ],
  "receiverInfo": {
    "receiver": "MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO",
    "cnpj": "30.982.547/0001-09",
    "address": "AV BRIGADEIRO FARIA LIMA, 2277 - SÃO PAULO",
    "date": "SÃO PAULO, 05 DE FEVEREIRO DE 2021"
  }
}
```