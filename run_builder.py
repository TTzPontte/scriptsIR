### SCRIPT IDENTIFICA QUAIS SÃO OS CONTRATOS COM FLEXIBILIDADE A PARTIR DE UMA LISTA DE IDS
### PREFERENCIALMENTE USAR RELATÓRIO FLUXO CCI

import pandas as pd
from contract_builder import fixedContract
import datetime

flcci = pd.read_excel(R'C:\Users\PerdoCaiafa\Pontte-Servicer\IR\fluxocci.xlsx')
ids = flcci.loc[flcci['Status do Contrato'] != 'ATIVO (QUITADO)']['Identificador do Contrato'].unique()




flex_ids = pd.DataFrame(columns=['id', 'flex'])
error_ids = pd.DataFrame(columns=['id', 'error', 'msg'])

for id in ids:
    print(id)
    new_data = pd.DataFrame(
        columns= ['id', 'flex']
    )

    try:
        contract = fixedContract(int(id))
        if contract.contrato['flex_month'] != '':
            new_data = pd.DataFrame(
                data = {
                    'id': [contract.contrato['id_contrato']],
                    'flex' : ['pula_parc']
                }
            )
        
        elif contract.contrato['carencia'] == True:
            new_data = pd.DataFrame(
                data = {
                    'id': [contract.contrato['id_contrato']],
                    'flex' : ['carencia']
                }
            )

        flex_ids = pd.concat([flex_ids, new_data])
    
    except Exception as e:
        new_error_data = pd.DataFrame(
                data = {
                    'id': [contract.contrato['id_contrato']],
                    'error' : [e.__class__.__name__] ,
                    'msg': [e]
                }
            )
        
        error_ids = pd.concat([error_ids, new_error_data])    



error_ids.to_excel('erros.xlsx')
flex_ids.to_excel('ids_flex.xlsx')
        