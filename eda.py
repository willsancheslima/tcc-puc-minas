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

# identifiquei estados com siglas minusculas => padronizando todos para maiusculas
df['orgaoSancionador_siglaUf'] = df['orgaoSancionador_siglaUf'].str.upper()
# identifiquei estados vazios => trocando para valor nao numerico => https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
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

# no grafico anterior identifiquei valores extremos da serie dataFimSancao
# vou pegar os indices das datas posteriores a 2030 para analise
dataFimSancao_outlier_boolean = df['dataFimSancao'] > '31/12/2030'
# filtrando apenas datas posteriores a 2030 na serie dataFimSancao para analise
dataFimSancao_outlier_dates = dataFimSancao[dataFimSancao_outlier_boolean]
# visualizando as datas posteriores a 2030
### print(dataFimSancao_outlier_dates.value_counts())
### print(sum(dataFimSancao_outlier_dates.value_counts()))
# identifiquei 25 datas acima de 2030 sendo que 14 sao exatamente o mesmo dia => 2039-10-07

# filtrando apenas datas posteriores a 2030 no dataframe para analise
df_dataFimSancao_outlier = df[dataFimSancao_outlier_boolean]

# verificando se existe alguma relacao entre as datas e os tipos de sancoes
### print(df_dataFimSancao_outlier['tipoSancao_descricaoResumida'].value_counts())
# aqui tambem identifiquei 14 tipos iguais de tipoSancao => "Decisao judicial liminar/cautelar que impeça contratacao"

# verificando se as 14 datas iguais tem relacao com os 14 tipos de sancoes iguais
### print(df_dataFimSancao_outlier[['tipoSancao_descricaoResumida','dataFimSancao']].sort_values(by=['tipoSancao_descricaoResumida']))
### print()
### print()
### print(df_dataFimSancao_outlier[['dataFimSancao','tipoSancao_descricaoResumida']].sort_values(by=['dataFimSancao']))

# a analise acima nao foi conclusiva, vamos entao buscar mais informacoes
# subtraindo a data inicial da data final para obter o prazo das sancoes em dias
prazoSancao = dataFimSancao - dataInicioSancao
# describe para analisar os dados ref prazo das sancoes
print(prazoSancao.describe())
# no describe acima identifiquei que o min e negativo, o que nao faz sentido
# filtrando os prazos negativos
dataFimSancao_negative_boolean = dataFimSancao < dataInicioSancao
# obtendo a quantidade de linhas afetadas para avaliar a extensao
print(dataFimSancao_negative_boolean.value_counts())
# removendo essas linhas do dataframe para nao interferir nas analises
df_dataOk = df[~dataFimSancao_negative_boolean]
prazoSancao = df_dataOk['dataFimSancao'] - df_dataOk['dataInicioSancao']
# describe para verificar os numeros
print(prazoSancao.describe())
# removendo as linhas com datas extremas para nao interferis nas alises
df_dataOk = df_dataOk[~dataFimSancao_outlier_boolean]
prazoSancao = df_dataOk['dataFimSancao'] - df_dataOk['dataInicioSancao']
# verificando os numeros apos remover prazos extremos e negativos
print(prazoSancao.describe())
print()
print()
print()
# describe da serie prazoSancao_outlier para confrontar com os numeros de prazoSancao
prazoSancao_outlier = df_dataFimSancao_outlier['dataFimSancao'] - df_dataFimSancao_outlier['dataInicioSancao']
print(prazoSancao_outlier.describe())
# verifiquei que a media de prazo em dias do daframe df_dataOk e quase cinco vezes menor que do  apenas 20% do df_dataFimSancao_outlier
# isso nos leva a crer que essas datas estão incorretas
# @TO-DO remover as datas outliers do dataframe df