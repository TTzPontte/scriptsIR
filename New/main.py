import pandas as pd

path = '/Users/Mr-i-me/code/Mr-i-me-pontte/Pontte/ir/scriptsIR/Data/IR_CRI_V2_short.xlsx'
flcci = pd.read_excel(path)

print(flcci)
gb = flcci.groupby('Identificador do Contrato')


Av. Brg. Faria Lima, 1485 - 18º andar - Pinheiros, São Paulo - SP, 01452-002