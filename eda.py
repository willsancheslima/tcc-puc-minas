import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils as utl
#pylint:disable=E1101


data = utl.getListFromMongoCol('ceis', 'register')
df = utl.flattenListAsDF(data)

# analises basicas no dataframe
#>>> utl.printwhf(df.head, 'df.head')
#>>> utl.printwhf(df.describe, 'df.describe')
#>>> utl.printwhf(df.pessoa_tipoPessoa.value_counts(), 'df.pessoa_tipoPessoa.value_counts()')
#>>> utl.printwhf(df.pessoa_municipio_uf_sigla.value_counts(), 'df.pessoa_municipio_uf_sigla.value_counts()')
#>>> utl.printwhf(df.pessoa_cnae_secao.value_counts(), 'df.pessoa_cnae_secao.value_counts()')
#>>> utl.printwhf(df.orgaoSancionador_nome.value_counts(), 'df.orgaoSancionador_nome.value_counts()')
#>>> utl.printwhf(df.orgaoSancionador_siglaUf.value_counts(), 'df.orgaoSancionador_siglaUf.value_counts()')
#>>> utl.printwhf(df.orgaoSancionador_poder.value_counts(), 'df.orgaoSancionador_poder.value_counts()')

# identifiquei estados com siglas minusculas na serie orgaoSancionador_siglaUf => padronizando todos para maiusculas
df['orgaoSancionador_siglaUf'] = df['orgaoSancionador_siglaUf'].str.upper()
# identifiquei estados vazios => trocando para valor nao numerico => https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
df['orgaoSancionador_siglaUf'].replace([''], np.nan, inplace=True)
# contagem atualizada apos correcao
#>>> print(df.orgaoSancionador_siglaUf.value_counts())

# identifiquei um valor nao valido na serie pessoa_municipio_uf_sigla => trocando para valor nao numerico
df['pessoa_municipio_uf_sigla'].replace(['-1'], np.nan, inplace=True)
# contagem atualizada apos correcao
#>>> print(df.pessoa_municipio_uf_sigla.value_counts())

# convertendo series dataInicioSancao de string para dateTime
dataInicioSancao = pd.to_datetime(df['dataInicioSancao'])
df['dataInicioSancao'] = dataInicioSancao
# verificando a distribuicao de datas
#>>> plt.hist(df['dataInicioSancao'].dropna(), bins=30)
#>>> plt.show()

# convertendo serie dataFimSancao de string para dateTime utilizando "coerce"
# passing errors=’coerce’ will force an out-of-bounds date to NaT, in addition to forcing non-dates (or non-parseable dates) to NaT
dataFimSancao = pd.to_datetime(df['dataFimSancao'], errors='coerce') 
df['dataFimSancao'] = dataFimSancao
#>>> plt.hist(dataFimSancao.dropna(), bins=30)
#>>> plt.show()

# no grafico anterior identifiquei valores extremos na serie dataFimSancao
# filtrando os indices das datas posteriores a 2030 para analise
dataFimSancao_outlier_boolean = df['dataFimSancao'] > '31/12/2030'
# filtrando apenas datas posteriores a 2030 na serie dataFimSancao para analise
dataFimSancao_outlier_dates = dataFimSancao[dataFimSancao_outlier_boolean]
# visualizando as datas posteriores a 2030
#>>> print(dataFimSancao_outlier_dates.value_counts())
#>>> print(sum(dataFimSancao_outlier_dates.value_counts()))
# identifiquei 25 datas acima de 2030 sendo que 14 sao exatamente o mesmo dia => 2039-10-07

# filtrando apenas datas posteriores a 2030 no dataframe para analise
df_dataFimSancao_outlier = df[dataFimSancao_outlier_boolean]

# verificando se existe alguma relacao entre as datas e os tipos de sancoes
#>>> print(df_dataFimSancao_outlier['tipoSancao_descricaoResumida'].value_counts())
# aqui tambem identifiquei 14 tipos iguais de tipoSancao => "Decisao judicial liminar/cautelar que impeça contratacao"

# verificando se as 14 datas iguais tem relacao com os 14 tipos de sancoes iguais
#>>> print(df_dataFimSancao_outlier[['tipoSancao_descricaoResumida','dataFimSancao']].sort_values(by=['tipoSancao_descricaoResumida']))
#>>> print(df_dataFimSancao_outlier[['dataFimSancao','tipoSancao_descricaoResumida']].sort_values(by=['dataFimSancao']))

# a analise acima nao foi conclusiva, vamos entao buscar mais informacoes
# subtraindo a data inicial da data final para obter o prazo das sancoes em dias
prazoSancao = dataFimSancao - dataInicioSancao
# describe para analisar os dados ref prazo das sancoes
#>>> print(prazoSancao.describe())

# no describe acima identifiquei que o min e negativo, o que nao faz sentido
# vamos limpar essas datas do dataframe
# filtrando os prazos negativos (onde dataFimSancao < dataInicioSancao)
dataFimSancao_negative_boolean = dataFimSancao < dataInicioSancao
# substituindo essas datas por NaT no dataframe
df.at[dataFimSancao_negative_boolean, 'dataFimSancao'] = pd.Timedelta('nat')
# atribuindo os valores atualizados a serie dataFimSancao
dataFimSancao = df['dataFimSancao']
# recalculando o prazo
prazoSancao = dataFimSancao - dataInicioSancao
# visualizando o describe para validar a correcao
#>>> print(prazoSancao.describe())

# continuando a analise de datas extremas
# desconsiderando as datas extremas para nao interferir nas analises
df_dataOk = df[~dataFimSancao_outlier_boolean]
prazoSancaoOk = df_dataOk['dataFimSancao'] - df_dataOk['dataInicioSancao']
# verificando os numeros com describe apos desconsiderar valores extremos de dataFimSancao
#>>> print(prazoSancaoOk.describe())
# verificando o describe da serie prazoSancao_outlier para confrontar com o describe da serie prazoSancaook
prazoSancao_outlier = df_dataFimSancao_outlier['dataFimSancao'] - df_dataFimSancao_outlier['dataInicioSancao']
#>>> print(prazoSancao_outlier.describe())
# verifiquei que a media de prazo em dias do daframe df_dataOk e quase cinco vezes menor que do dataframe df_dataFimSancao_outlier
# visualizando a contagem ordenada dos anos para ilustrar melhor a situacao
dataFimSancao_year = pd.DatetimeIndex(df['dataFimSancao']).year
#>>> print(dataFimSancao_year.value_counts().sort_index())
# verifiquei que essa quantidade representa 0.0018% do total de datas validas da serie dataFimSancao
# vamos entao definir essas datas como NaT, para nao interferirem nas analises de prazos, visto que sao 5 vezes superiores
# atribuindo valor NaT para todas datas superiores a 2030
df.loc[df['dataFimSancao'] > '31/12/2030', 'dataFimSancao'] = pd.Timedelta('nat')
# verificando se das datas foram efetivamente substituidas
#>>> print((df['dataFimSancao'] > '31/12/2030').value_counts())

# vamos então retomar as analises das datas exibindo o histograma atualizada da dataFimSancao
#>>> plt.hist(dataFimSancao.dropna(), bins=30)
#>>> plt.show()
# agora temos um distribuicao mais homogenea da serie dataFimSancao, sem datas futuras extremas

# apos validacoes e limpezas, vamos obter os prazos das sancoes novamente para analises
prazoSancao = dataFimSancao - dataInicioSancao
# describe para analisar os indicadores ref aos prazos das sancoes
#>>> print(prazoSancao.describe(include='all'))
# obtendo o valor medio em meses
prazoSancao_mean = prazoSancao.describe().loc['mean']
prazoSancao_meses = prazoSancao_mean / np.timedelta64(1, 'M')
#>>> print(round(prazoSancao_meses))
# obtivemos um prazo medio de 60 meses
# mas o desvio padrao e muito alto, precisamos analisar mais para entender melhor essas caracteristicas

# analisando prazos das sancoes por tipo de sancao
df_tipoSancao = df['tipoSancao_descricaoResumida'].unique()
#print(df_tipoSancao)
prazoSancao_tipoSancao = []
for tipoSancao in df_tipoSancao:
    df_tipoSancao_boolean = df['tipoSancao_descricaoResumida'] == tipoSancao
    df_tipoSancao_it = df[df_tipoSancao_boolean]
    prazo_tipoSancao = (df_tipoSancao_it["dataFimSancao"] - df_tipoSancao_it["dataInicioSancao"])
    prazoSancao_tipoSancao.append(prazo_tipoSancao.describe())
    #>>> print(tipoSancao)
    #>>> print(prazo_tipoSancao.describe())
    #>>> print()
#for item in prazoSancao_tipoSancao:
#    print(item[1])

# analisando prazos das sancoes por estado
df_uf = df['pessoa_municipio_uf_nome'].unique()
#print(type(df_uf))
prazoSancao_uf = []
for uf in df_uf:
    df_uf_boolean = df['pessoa_municipio_uf_nome'] == uf
    df_uf_it = df[df_uf_boolean]
    prazo_uf = (df_uf_it["dataFimSancao"] - df_uf_it["dataInicioSancao"])
    prazoSancao_uf.append(prazo_uf.describe())
    #>>> print(uf)
    #>>> print(prazo_uf.describe())
    #>>> print()
#for item in prazoSancao_uf:
#    print(item[1])

# a analise de prazos nao ofereceu nenhum insight visto que os valores de desvios padroes sao muito altos

# vamos, entao, efetuar analises pelo prisma das entidades sancionadas
# vamos verificar o indice de reincidencia de sancoes por entidades
pessoaCodigo = df['pessoa_codigoFormatado']
pessoaCodigo_value_counts = pessoaCodigo.value_counts()
#>>> print(pessoaCodigo_value_counts[pessoaCodigo_value_counts > 2].sum() / pessoaCodigo_value_counts.sum())
# o indice de reincidencia e de cerca de 16,3 %, uma taxa razoavel que vale a pena analisarmos

# filtrando o dataframe para obter apenas pessoas com quantidade de sancoes > 2
pessoaReincidente = pessoaCodigo_value_counts[pessoaCodigo_value_counts > 2]
df_pessoaReincidente = df[df.pessoa_codigoFormatado.isin(pessoaReincidente.index)]
#>>> print(df_pessoaReincidente)

# quais os tipos (PF ou PJ?)
#>>> print(df_pessoaReincidente.pessoa_tipoCodigo.value_counts())
#>>> df_pessoaReincidente_value_counts = df_pessoaReincidente.pessoa_tipoCodigo.value_counts()
#>>> labels = ['Pessoa Física', 'Pessoa Jurídica', 'Não informado']
#>>> sizes = df_pessoaReincidente_value_counts.values
#>>> fig1, ax1 = plt.subplots()
#>>> ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
#>>> ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#>>> plt.show()

# analisar onde se encontram as entidades com maior indice de reincidencia
#>>> print(df_pessoaReincidente.pessoa_municipio_uf_sigla.value_counts())

# agora vamos verificar se elas reincidem nas mesmas sancoes
#>>> print(df_pessoaReincidente.tipoSancao_descricaoResumida.value_counts())

# tempo de vida das empresas reincidentes
df_pessoaReincidente_pj = df_pessoaReincidente[df_pessoaReincidente.pessoa_tipoCodigo == 'CNPJ']
pessoaReincidentePJ_dataAbertura = pd.to_datetime(df_pessoaReincidente_pj['pessoa_dataAbertura'], errors='coerce')
pessoaReincidentePJ_tempoVida = pd.Timestamp.today() - pessoaReincidentePJ_dataAbertura
#>>> print(pessoaReincidentePJ_tempoVida.describe())

# comparando com o tempo de vida das empresas nao reincidentes
pessoaNaoReincidente = pessoaCodigo_value_counts[pessoaCodigo_value_counts == 1]
df_pessoaNaoReincidente = df[df.pessoa_codigoFormatado.isin(pessoaNaoReincidente.index)]
df_pessoaNaoReincidente_pj = df_pessoaNaoReincidente[df_pessoaNaoReincidente.pessoa_tipoCodigo == 'CNPJ']
pessoaNaoReincidentePJ_dataAbertura = pd.to_datetime(df_pessoaNaoReincidente_pj['pessoa_dataAbertura'], errors='coerce')
pessoaNaoReincidentePJ_tempoVida = pd.Timestamp.today() - pessoaNaoReincidentePJ_dataAbertura
#>>> print(pessoaNaoReincidentePJ_tempoVida.describe())


pivot = pd.pivot_table(df,index=["pessoa_municipio_uf_sigla","tipoSancao_descricaoResumida"], values=["id"],aggfunc={"id":len})
#new_order= ["id"]
#pivot = pivot.reindex(new_order, axis=1)
utl.print_all_df(pivot)