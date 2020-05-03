import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils as utl


data = utl.getListFromMongoCol('ceis', 'register')
df = utl.flattenListAsDF(data)

# analises basicas no dataframe
'''
utl.printwhf(df.head, 'df.head')

utl.printwhf(df.describe, 'df.describe')

utl.printwhf(df.pessoa_tipoPessoa.value_counts(), 'df.pessoa_tipoPessoa.value_counts()')

utl.printwhf(df.pessoa_municipio_uf_nome.value_counts(), 'df.pessoa_municipio_uf_nome.value_counts()')

utl.printwhf(df.pessoa_cnae_secao.value_counts(), 'df.pessoa_cnae_secao.value_counts()')

utl.printwhf(df.orgaoSancionador_nome.value_counts(), 'df.orgaoSancionador_nome.value_counts()')

utl.printwhf(df.orgaoSancionador_siglaUf.value_counts(), 'df.orgaoSancionador_siglaUf.value_counts()')

utl.printwhf(df.orgaoSancionador_poder.value_counts(), 'df.orgaoSancionador_poder.value_counts()')
#'''

# identificado estados com siglas minusculas => padronizando todos para maiusculas
df['orgaoSancionador_siglaUf'] = df['orgaoSancionador_siglaUf'].str.upper()
# identificado estados vazios => trocando para valor nao numerico => https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
df['orgaoSancionador_siglaUf'].replace([''], np.nan, inplace=True)
# contagem atualizada apos correcao
### print(df.orgaoSancionador_siglaUf.value_counts())

# convertendo series dataInicioSancao de string para dateTime
dataInicioSancao = pd.to_datetime(df['dataInicioSancao'])
df['dataInicioSancao'] = dataInicioSancao
# verificando a distribuicao de datas
### plt.hist(df['dataInicioSancao'].dropna(), bins=30)
### plt.show()

# convertendo serie dataFimSancao de string para dateTime utilizando "coerce"
# passing errors=’coerce’ will force an out-of-bounds date to NaT, in addition to forcing non-dates (or non-parseable dates) to NaT
dataFimSancao = pd.to_datetime(df['dataFimSancao'], errors='coerce') 
df['dataFimSancao'] = dataFimSancao
### plt.hist(dataFimSancao.dropna(), bins=30)
### plt.show()

# no grafico anterior foram identicados valores extremos da serie dataFimSancao
# obtendo os indices das datas posteriores a 2030 para analise
dataFimSancao_outlier_boolean = df['dataFimSancao'] > '31/12/2030'
# filtrando apenas datas posteriores a 2030 para analise
dataFimSancao_outlier_dates = dataFimSancao[dataFimSancao_outlier_boolean]
# contando as datas posteriores a 2030
print(dataFimSancao_outlier_dates.value_counts())

df_dataFimSancao_outlier = df[dataFimSancao_outlier_boolean]
### print(df_dataFimSancao_outlier['tipoSancao_descricaoResumida'].value_counts())
#print(dataFimSancao_outlier.sum())

#print(dataFimSancao - dataInicioSancao)

#'''