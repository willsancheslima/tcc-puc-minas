import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils as utl
#pylint:disable=E1101

data = utl.getListFromMongoCol('ceis', 'register')
df = utl.flattenListAsDF(data)

# analises preliminares no dataframe
print(df.shape)
print(df.head())
print(df.columns)
print(df.describe(include='all'))
print(df.pessoa_tipoCodigo.value_counts())
print(df.pessoa_tipoPessoa.value_counts())
print(df.pessoa_municipio_uf_sigla.value_counts())
print(df.pessoa_cnae_secao.value_counts())
print(df.orgaoSancionador_nome.value_counts())
print(df.orgaoSancionador_siglaUf.value_counts())
print(df.orgaoSancionador_poder.value_counts())

# identificados valores vazios => subsituindo por valores nao numericos
df['pessoa_tipoCodigo'].replace([''], np.nan, inplace=True)
print(df.pessoa_tipoCodigo.value_counts())

# identificado valor invalido => substituindo por valor nao numerico
df['pessoa_municipio_uf_sigla'].replace(['-1'], np.nan, inplace=True)
print(df.pessoa_municipio_uf_sigla.value_counts())

# identificados estados com siglas minusculas => padronizando todas para maiusculas
df['orgaoSancionador_siglaUf'] = df['orgaoSancionador_siglaUf'].str.upper()
# identificados estados vazios => substituindo para valores nao numericos
df['orgaoSancionador_siglaUf'].replace([''], np.nan, inplace=True)
print(df.orgaoSancionador_siglaUf.value_counts())

# convertendo series dataInicioSancao de string para dateTime
dataInicioSancao = pd.to_datetime(df['dataInicioSancao'])
df['dataInicioSancao'] = dataInicioSancao

# convertendo serie dataFimSancao de string para dateTime utilizando "coerce"
dataFimSancao = pd.to_datetime(df['dataFimSancao'], errors='coerce') 
df['dataFimSancao'] = dataFimSancao


#inicio do eda

# distribuicao PF/PJ
print(df.pessoa_tipoCodigo.value_counts(normalize=True)*100)

# distribuicao categoria pessoa
print(df.pessoa_tipoPessoa.value_counts(normalize=True)*100)

# pivot para verificar a relacao entre pessoa_tipoCodigo e pessoa_tipoPessoa
pivot = pd.pivot_table(df,index=["pessoa_tipoCodigo","pessoa_tipoPessoa"], values=["id"],aggfunc={"id":len})
result = pivot.sort_values('id', ascending=False)
print(result)

# distribuicao sancoes por estados
print(df.pessoa_municipio_uf_sigla.value_counts(normalize=True)*100)

# distribuicao sancoes por cnae
print(df.pessoa_cnae_secao.value_counts(normalize=True)*100)
# pivot para verificar a relacao entre pessoa_tipoCodigo e pessoa_cnae_secao
pivot = pd.pivot_table(df,index=["pessoa_tipoCodigo","pessoa_cnae_secao"], values=["id"], aggfunc={"id":len})
result = pivot.sort_values('id', ascending=False)
print(result)

# distribuicao sancoes por estado do orgao sancionador
print(df.orgaoSancionador_siglaUf.value_counts(normalize=True)*100)
# pivot para verificar a relacao entre orgaoSancionador_siglaUf e pessoa_municipio_uf_sigla
pivot = pd.pivot_table(df,index=["orgaoSancionador_siglaUf","pessoa_municipio_uf_sigla"], values=["id"], aggfunc={"id":len})
result = pivot.sort_values('orgaoSancionador_siglaUf')
print(result.head)

# distribuicao sancoes pela esfera de poder do orgao sancionador
print(df.orgaoSancionador_poder.value_counts(normalize=True)*100)

# verificando a distribuicao de sancoes por "dataInicioSancao"
plt.hist(df['dataInicioSancao'].dropna(), bins=30)
plt.show()

# verificando a distribuicao de sancoes por "dataFimSancao"
#plt.hist(df['dataFimSancao'].dropna(), bins=30)
#plt.show()

# no grafico anterior foram identificados valores extremos na serie dataFimSancao
# filtrando apenas datas posteriores a 2030 na serie dataFimSancao para analise
print(dataFimSancao[df['dataFimSancao'] > '31/12/2030'].value_counts().sort_index())

# atribuindo valor NaT para data outlier
df.loc[df['dataFimSancao'] == '31/12/2099', 'dataFimSancao'] = pd.Timedelta('nat')
# atribuindo a correcao a variavel dataFimSancao
dataFimSancao = df['dataFimSancao']
# vizualizando datas acima de 2030 para verificar a exclusao da data outlier 
print(dataFimSancao[df['dataFimSancao'] > '31/12/2030'].value_counts().sort_index())

# exibindo o histograma apos exclusao da data outlier
plt.hist(dataFimSancao.dropna(), bins=30)
plt.show()

# obtendo os prazos das sancoes para analises
prazoSancao = dataFimSancao - dataInicioSancao
# describe para analisar os dados ref prazo das sancoes
print(prazoSancao.describe(include='all'))

# no describe acima foi identificado que o min e negativo, o que nao faz sentido
# essas datas serao removidas do dataframe
# filtrando os prazos negativos (onde dataFimSancao < dataInicioSancao)
dataFimSancao_negative_boolean = dataFimSancao < dataInicioSancao
# substituindo essas datas por NaT no dataframe
df.at[dataFimSancao_negative_boolean, 'dataFimSancao'] = pd.Timedelta('nat')
# atribuindo os valores atualizados a serie dataFimSancao
dataFimSancao = df['dataFimSancao']

# recalculando o prazo
prazoSancao = dataFimSancao - dataInicioSancao
# visualizando o describe para validar a correcao
print(prazoSancao.describe(include='all'))

# obtendo o valor medio em meses
prazoSancao_mean = prazoSancao.describe().loc['mean']
prazoSancao_meses = prazoSancao_mean / np.timedelta64(1, 'M')
print(prazoSancao_meses)

# obtivemos um prazo medio de 59 meses
# mas o desvio padrao e muito alto, precisamos analisar mais para entender melhor essas caracteristicas

# analisando prazos das sancoes por tipo de sancao
df_tipoSancao = df['tipoSancao_descricaoResumida'].unique()
df_tipoSancao = list(df_tipoSancao)
df_tipoSancao = np.sort(df_tipoSancao)

labels = []
prazo_mean = []
prazo_std = []
for tipoSancao in df_tipoSancao:
    df_tipoSancao_it = df[df['tipoSancao_descricaoResumida'] == tipoSancao]
    prazo_tipoSancao = (df_tipoSancao_it["dataFimSancao"] - df_tipoSancao_it["dataInicioSancao"])
    labels.append(tipoSancao[:30])
    prazo_mean.append(prazo_tipoSancao.describe().loc['mean'] / np.timedelta64(1, 'M'))
    prazo_std.append(prazo_tipoSancao.describe().loc['std'] / np.timedelta64(1, 'M'))

utl.groupedBarWithLabels(prazo_mean, prazo_std, labels, 
        'Prazo medio', 'Desvio padrao', 'Meses', 'Prazos das Sancoes por Tipo de Sancao')

# analisando prazos das sancoes por estado
df_uf = df['pessoa_municipio_uf_sigla'].unique()
df_uf = list(df_uf)
df_uf.remove(np.nan)
df_uf = np.sort(df_uf)

labels = []
prazo_mean = []
prazo_std = []
prazoSancao_uf = []
for uf in df_uf:
    df_uf_it = df[df['pessoa_municipio_uf_sigla'] == uf]
    prazo_uf = (df_uf_it["dataFimSancao"] - df_uf_it["dataInicioSancao"])
    prazoSancao_uf.append(prazo_uf.describe())
    labels.append(uf)
    prazo_mean.append(prazo_uf.describe().loc['mean'] / np.timedelta64(1, 'M'))
    prazo_std.append(prazo_uf.describe().loc['std'] / np.timedelta64(1, 'M'))

utl.groupedBarWithLabels(prazo_mean, prazo_std, labels, 
        'Prazo medio', 'Desvio padrao', 'Meses', 'Prazos das Sancoes por UF')

# a analise de prazos nao ofereceu nenhum insight visto que os valores de desvios padroes sao muito altos

# efetuando analises nas entidades sancionadas
# verificando o indice de reincidencia de sancoes por entidades
pessoaCodigo = df['pessoa_codigoFormatado']
pessoaCodigo_value_counts = pessoaCodigo.value_counts()
print(pessoaCodigo_value_counts[pessoaCodigo_value_counts > 2].sum() / pessoaCodigo_value_counts.sum())

# filtrando o dataframe para obter apenas pessoas com quantidade de sancoes > 2
pessoaReincidente = pessoaCodigo_value_counts[pessoaCodigo_value_counts > 2]
df_pessoaReincidente = df[df.pessoa_codigoFormatado.isin(pessoaReincidente.index)]
print(df_pessoaReincidente.describe(include='all'))

# verificarndo os tipos de pessoa (PF ou PJ?)
print(df_pessoaReincidente.pessoa_tipoCodigo.value_counts(normalize=True)*100)

# verificando onde se encontram as entidades com maior indice de reincidencia
print(df_pessoaReincidente.pessoa_municipio_uf_sigla.value_counts(normalize=True)*100)

# verificando a distribuicao de sancoes das entidades reincidentes
print(df_pessoaReincidente.tipoSancao_descricaoResumida.value_counts(normalize=True)*100)

# tempo de vida das empresas reincidentes
df_pessoaReincidente_pj = df_pessoaReincidente[df_pessoaReincidente.pessoa_tipoCodigo == 'CNPJ']
pessoaReincidentePJ_dataAbertura = pd.to_datetime(df_pessoaReincidente_pj['pessoa_dataAbertura'], errors='coerce')
pessoaReincidentePJ_tempoVida = pd.Timestamp.today() - pessoaReincidentePJ_dataAbertura
print(pessoaReincidentePJ_tempoVida.describe())

# comparando com o tempo de vida das empresas nao reincidentes
pessoaNaoReincidente = pessoaCodigo_value_counts[pessoaCodigo_value_counts == 1]
df_pessoaNaoReincidente = df[df.pessoa_codigoFormatado.isin(pessoaNaoReincidente.index)]
df_pessoaNaoReincidente_pj = df_pessoaNaoReincidente[df_pessoaNaoReincidente.pessoa_tipoCodigo == 'CNPJ']
pessoaNaoReincidentePJ_dataAbertura = pd.to_datetime(df_pessoaNaoReincidente_pj['pessoa_dataAbertura'], errors='coerce')
pessoaNaoReincidentePJ_tempoVida = pd.Timestamp.today() - pessoaNaoReincidentePJ_dataAbertura
print(pessoaNaoReincidentePJ_tempoVida.describe())

pivot = pd.pivot_table(df,index=["pessoa_municipio_uf_sigla","tipoSancao_descricaoResumida"], values=["id"],aggfunc={"id":len})
pivot = pivot.reindex(axis=1)
utl.print_all_df(pivot)

# arquivos csv para geracao de graficos no power bi
utl.serieToPercQtdeCSV(df.pessoa_tipoCodigo, 'pessoa_tipoCodigo') 
utl.serieToPercQtdeCSV(df.pessoa_tipoPessoa, 'pessoa_tipoPessoa') 
utl.serieToPercQtdeCSV(df.pessoa_municipio_uf_sigla, 'pessoa_municipio_uf_sigla') 
utl.serieToPercQtdeCSV(df.pessoa_cnae_secao, 'pessoa_cnae_secao') 
utl.serieToPercQtdeCSV(df.orgaoSancionador_nome, 'orgaoSancionador_nome') 
utl.serieToPercQtdeCSV(df.orgaoSancionador_siglaUf, 'orgaoSancionador_siglaUf') 
utl.serieToPercQtdeCSV(df.orgaoSancionador_poder, 'orgaoSancionador_poder') 
utl.serieToPercQtdeCSV(df.tipoSancao_descricaoResumida, 'tipoSancao_descricaoResumida') 
dataInicioSancao = df['dataInicioSancao'].dropna()
dataInicioSancao.to_csv('sources/graph.dataInicioSancao.csv') 
dataFimSancao = df['dataFimSancao'].dropna()
dataFimSancao.to_csv('sources/graph.dataFimSancao.csv')
df_filtered = df.filter(items=['dataInicioSancao', 'tipoSancao_descricaoResumida'])
df_filtered.to_csv('sources/graph.datasTipoSancao.csv')

df_geo = df.filter(items=['pessoa_municipio_nomeIBGE', 'pessoa_municipio_uf_nome', 'pessoa_municipio_pais'])
df_geo['pessoa_municipio_uf_pais'] = df['pessoa_municipio_nomeIBGE']+', '+df['pessoa_municipio_uf_nome']+', '+df['pessoa_municipio_pais' ]
df_geo['pessoa_municipio_uf_pais'].replace(['Sem Informação, Sem informação, S/I'], np.nan, inplace=True)
df_geo['pessoa_municipio_uf_pais'].dropna()
df_geo.to_csv('sources/graph.georef.csv') 