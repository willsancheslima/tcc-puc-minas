import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils as utl

utl.insertPagedApiData('ceis', 'register', 'http://www.transparencia.gov.br/api-de-dados/ceis', 'pagina')

#TO-DO => implementar insertCol()
#utl.insertCol('ceis', 'register', data)

#data = utl.getListFromMongoCol('ceis', 'register')
#df = utl.flattenListAsDF(data)

'''
utl.printwhf(df.head, 'df.head')

utl.printwhf(df.describe, 'df.describe')

utl.printwhf(df.pessoa_tipoPessoa.value_counts(), 'df.pessoa_tipoPessoa.value_counts()')

utl.printwhf(df.pessoa_municipio_uf_nome.value_counts(), 'df.pessoa_municipio_uf_nome.value_counts()')

utl.printwhf(df.pessoa_cnae_secao.value_counts(), 'df.pessoa_cnae_secao.value_counts()')

utl.printwhf(df.orgaoSancionador_nome.value_counts(), 'df.orgaoSancionador_nome.value_counts()')

utl.printwhf(df.orgaoSancionador_siglaUf.value_counts(), 'df.orgaoSancionador_siglaUf.value_counts()')

utl.printwhf(df.orgaoSancionador_poder.value_counts(), 'df.orgaoSancionador_poder.value_counts()')
'''

'''
dataInicioSancao = pd.to_datetime(df['dataInicioSancao'])
#plt.hist(dataInicioSancao.dropna(), bins=30)
#plt.show()

dataFimSancao = pd.to_datetime(df['dataFimSancao'], errors='coerce') #Passing errors=’coerce’ will force an out-of-bounds date to NaT, in addition to forcing non-dates (or non-parseable dates) to NaT.
df['dataFimSancao'] = dataFimSancao
#plt.hist(dataFimSancao.dropna(), bins=50)
#plt.show()

dataFimSancao_outlier = df['dataFimSancao'] > '31/12/2030'
#dataFimSancao_outlier = dataFimSancao[dataFimSancao_outlier]
#print(dataFimSancao_outlier)
df_dataFimSancao_outlier = df[dataFimSancao_outlier]
print(df_dataFimSancao_outlier['tipoSancao_descricaoResumida'])
#print(dataFimSancao_outlier.sum())

#print(dataFimSancao - dataInicioSancao)

#df['orgaoSancionador_siglaUf'] = df['orgaoSancionador_siglaUf'].str.upper()
#df['orgaoSancionador_siglaUf'].replace([''], np.nan, inplace=True)
#print_all_df(df['orgaoSancionador_siglaUf'])
#print(df.orgaoSancionador_siglaUf.value_counts())
'''