
import pandas as pd

names = ['TIPO DE PESSOA','CPF OU CNPJ DO SANCIONADO','NOME INFORMADO PELO ORGAO SANCIONADOR','RAZAO SOCIAL - CADASTRO RECEITA','NOME FANTASIA - CADASTRO RECEITA','NUMERO DO PROCESSO','TIPO SANCAO','DATA INICIO SANCAO','DATA FINAL SANCAO','ORGAO SANCIONADOR','UF ORGAO SANCIONADOR','ORIGEM INFORMACOES','DATA ORIGEM INFORMACOES','DATA PUBLICACAO','PUBLICACAO','DETALHAMENTO','ABRAGENCIA DEFINIDA EM DECISAO JUDICIAL','FUNDAMENTACAO LEGAL','DESCRICAO DA FUNDAMENTACAO LEGAL','DATA DO TRÂNSITO EM JULGADO','COMPLEMENTO DO ORGAO','OBSERVACOES']

df = pd.read_csv('sources/CEIS.csv', sep=';', encoding='latin_1', header=0, names=names)

#df['ESTADO'] = df['UF ORGAO SANCIONADOR']

#print(df['UF ORGAO SANCIONADOR'])
#print(df['ESTADO'])

uf_sigla = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
uf_nome = ['Acre', 'Alagoas', 'Amapa', 'Amazonas', 'Bahia', 'Ceara', 'Brasilia', 'Espirito Santo', 'Goias', 'Maranhao', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Para', 'Paraiba', 'Parana', 'Pernambuco', 'Piaui', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondonia', 'Roraima', 'Santa Catarina', 'Sao Paulo', 'Sergipe', 'Tocantins']

df['ESTADO'] = df['UF ORGAO SANCIONADOR'].replace(uf_sigla, uf_nome)

#print(df['ESTADO'])

df.to_csv('sources/CEIS_NORMALIZED.csv', index=False)

