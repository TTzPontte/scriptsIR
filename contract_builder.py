#### SCRIPT P/ IDENTIFICAR QUAIS SÃO OS CONTRATOS COM FLEXIBILIDADE

import requests as re
import pandas as pd
import numpy as np
import datetime
import json

def get_data(id, operation):
   payload = {"idContract": id, "action": operation, "env": "prod"}
   data = re.post(
      'https://0qilw2i5ub.execute-api.us-east-1.amazonaws.com/default',
      data= json.dumps(payload) 
   ).json()
   
   return data

def get_principal_dates(series: pd.Series):
   try:
      series = pd.to_datetime(series)
      days = series.dt.day.value_counts()
      
      return series.where(
         series.dt.day == days.index[0]
      ).dropna()
   
   except KeyError:
      return np.nan


class fixedContract:

    """
    Classe criada a partir do retorno dos métodos do AzTronic Collect
    
     """

    def __init__(self, id) -> None:
        data = get_data(id, 'getFinances')
        self.parcelas = pd.DataFrame(
            data = data['data']['posicaofinanceira']['parcelas']
            )
        
        self.parcelas['data_vencimento'] = pd.to_datetime(self.parcelas['data_vencimento'])
        self.parcelas['venc_year'] = self.parcelas['data_vencimento'].dt.year 
        self.parcelas['venc_month'] = self.parcelas['data_vencimento'].dt.month

        self.parcelas = self.parcelas.groupby(by=['venc_year', 'venc_month']).agg({
                'data_vencimento': get_principal_dates,
                'valor_principal': 'sum',
                'valor_juros' : 'sum',
                'valor_original' : 'sum',
                'valor_correcao' : 'sum',
                'valor_corrigido' : 'sum',
                'valor_multa' : 'sum',
                'valor_mora': 'sum',
                'valor_desconto': 'sum',
                'valor_mip': 'sum',
                'valor_dfi': 'sum',
                'valor_taxa_adm': 'sum',
                'valor_cobrado': 'sum',
                'data_pagamento': 'first',
                'valor_pago': 'sum',
                'valor_saldo': 'sum',
                'juros_incorrido': 'sum',
                'correcao_proporcional': 'sum'                            

            })            

        

        self.contrato = data['data']['posicaofinanceira']['contrato']
        #self.identifica_flex()
        #self.identifica_amort()
        #self.identifica_grace()


    
    def identifica_flex(self):
        # identifica se contrato tem pula parcela e informa o mês
        if  self.parcelas.index.get_level_values(1).value_counts().iloc[-1] <= self.parcelas.index.get_level_values(1).value_counts().iloc[0] / 2:
            flex_month = self.parcelas.index.get_level_values(1).value_counts().index[-1]
        else:
            try:
                months = self.parcelas.index.get_level_values(1).unique()
                flex_month = list(set([1,2,3,4,5,6,7,8,9,10,11,12]) - set(months))[0]
            except IndexError:
                flex_month = ''
                
        self.contrato['flex_month'] = flex_month

    
    def identifica_parcela(self):
        # identifica o número de cada uma das parcelas
        pass


    def identifica_amort(self):
        if self.parcelas['valor_principal'].iloc[0] == self.parcelas['valor_principal'].iloc[-1]:
            self.contrato['amort'] = 'sac'
        else:
            self.contrato['amort'] = 'price'


    def identifica_grace(self):
        data_base = datetime.datetime.strptime(self.contrato['data_base'][:10], '%Y-%m-%d')
        if self.parcelas['data_vencimento'].iloc[0].month != data_base.month:
            if pd.to_datetime(datetime.datetime.now()) < self.parcelas['data_vencimento'].iloc[0]:
                self.contrato['carencia'] = True
            else:
                self.contrato['carencia'] = False

        else:
            self.contrato['carencia'] = False
      
 
        
