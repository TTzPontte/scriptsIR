### SCRIPT GERA PAYLOAD P/ GERAÇÃO DE IR A PARTIR DE UMA BASE NESSE FORMATO:
"""
      id    |    saldo
"""

### SALDO DEVE VIR DO RELATÓRIO FLUXO SCCI (DATA BASE 31/12/ano) - SOMENTE CONTRATOS SEM FLEX

from functools import reduce
import requests as re
import json
import pandas as pd
import numpy as np
from contract_builder import fixedContract, get_data

def getIR(id):
    header = {
    'Authorization': 'Basic QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ==',
    'Content-Type': 'application/json'
    }

    endpoint = 'https://srv1.aztronic.com.br/az/apicollect/api/cliente/{0}/{1}/2021'.format('GetInformeIR', id)

    dataIR = re.get(
    endpoint,
    headers = header
    ).json()

    return dataIR

def bateApi(id, operation):
    header = {
    'Authorization': 'Basic QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ==',
    'Content-Type': 'application/json'
    }

    endpoint = 'https://srv1.aztronic.com.br/az/apicollect/api/cliente/{0}/{1}'.format(operation, id)

    dataApi = re.get(
    endpoint,
    headers = header
    ).json()

    return dataApi


def createPayload(data: pd.DataFrame):
  payload = {
    'body': {
      'data' : []
    }
  }

  error_ids = pd.DataFrame(columns=['id', 'error', 'msg'])

  for id in data.index:
    try:
      print(id)
      AztFinances = get_data(id, 'getFinances')
      AztContrato = AztFinances['data']['posicaofinanceira']['contrato']

      AztIR = getIR(id)
      mainParticipant = max(AztIR['informeir']['participantes'], key = lambda x: x['participacao'])
      docNumber = int(mainParticipant['cnpj_cpf'])

      AztDadosCadastrais = bateApi(docNumber, 'GetCliente')


      Contract = { 'contractInfo': {
        'EMPREENDIMENTO': AztContrato['empreendimento'],
        'CONTRATO': id,
        'ANO BASE': '2021',
        'BLOCO': AztContrato['bloco'],
        'UNIDADE': AztContrato['unidade'],
        'DATA': '25/02/2021',
        'EMAIL': AztDadosCadastrais['cliente']['email'],
        'SALDO': data.loc[id,'saldo']         
      },

      'installments': [],
      'participants': [],
      
      'receiverInfo': {
            'receiver': "MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO",
            'cnpj': "30.982.547/0001-09",
            'address': "AV BRIGADEIRO FARIA LIMA, 2277 - SÃO PAULO",
            'date': "SÃO PAULO, 05 DE FEVEREIRO DE 2021"
          }   
      }




      for pmt in AztIR['informeir']['pagamentos']:
        parcela = {
          'creditDate': pmt['mes'],
          'payedInstallment': str(pmt['mes']) + ' - Mensal',
          'amoutPayed': pmt['valor_pago']
        }
        Contract['installments'].append(parcela)

    
      for person in AztIR['informeir']['participantes']:
          participante = {
              'name': person['nome'],
              'documentNumber': person['cnpj_cpf'],
              'participation': person['participacao']
              } 

          Contract['participants'].append(participante)  


      
      #send2payload
      payload['body']['data'].append(Contract)
      print(Contract)


    except Exception as e:
        Contract = { 'contractInfo': {
        'CONTRATO': id,
        'ANO BASE': '2021',
        'DATA': '25/02/2021',
        'SALDO': data.loc[id,'saldo']   
        },

        'installments': [],
        'participants': [], 
  
          'receiverInfo': {
            'receiver': "MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO",
            'cnpj': "30.982.547/0001-09",
            'address': "AV BRIGADEIRO FARIA LIMA, 2277 - SÃO PAULO",
            'date': "SÃO PAULO, 05 DE FEVEREIRO DE 2021"}
            }

        if AztIR['informeir'] != None:
            for pmt in AztIR['informeir']['pagamentos']:
                parcela = {
                'creditDate': pmt['mes'],
                'payedInstallment': str(pmt['mes']) + ' - Mensal',
                'amoutPayed': pmt['valor_pago']
                }

                Contract['installments'].append(parcela) 

            for person in AztIR['informeir']['participantes']:
                participante = {
                    'name': person['nome'],
                    'documentNumber': person['cnpj_cpf'],
                    'participation': person['participacao']
                    }    
                
                Contract['participants'].append(participante)  


        else:
          pass  


        payload['body']['data'].append(Contract)
        print('------------------------ Exception -------------------------------')
        print(e.__class__.__name__)
        print(e)
        print(Contract)
    
  return payload


database = pd.read_excel('3ids.xlsx')
database['id'] = database['id'].astype(int)
database.fillna('undefined', inplace=True)
database.set_index('id',inplace=True)
database = database[~database.index.duplicated(keep='first')]

dadosIR = createPayload(database)

with open ('CONTRATOS.txt', 'w') as file:
    file.write(str(dadosIR))