import pandas as pd
import numpy as np
import pymongo
import matplotlib.pyplot as plt
import requests
import json
from flatten_json import flatten

def connect_mongo(db, col, host='localhost', port=27017):
    client = pymongo.MongoClient(host, port)
    db = client[db]
    return db[col]

def jsonprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def popula_ceis(paginas=1):
    col = connect_mongo('ceis', 'registro')
    parameters = {"pagina": 1}
    while(parameters['pagina'] <= paginas):
        response = requests.get('http://www.transparencia.gov.br/api-de-dados/ceis', parameters)
        result = col.insert_many(response.json())
        print('pagina = '+str(parameters['pagina'])+' => '+str(result))
        parameters['pagina'] += 1
'''
def read_mongo(db, col, query={}, host='localhost', port=27017, username=None, password=None, no_id=False):
    """ Read from Mongo and Store into DataFrame """
    # Connect to MongoDB
    col = connect_mongo('ceis', 'registro')
    # Make a query to the specific DB and Collection
    cursor = col.find(query)
    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))
    # Delete the _id
    if no_id:
        del df['_id']
    return df

def edaPessoaCnaeSecao():
    col = connect_mongo('ceis', 'registro')
    #data = pd.DataFrame(list(col.find()))

    result = col.aggregate( [ { '$project': { 'pessoa.cnae.secao': 1 } } ] )
    result_list = list(result)
    cnae_secao = []
    for row in result_list:
        cnae_secao.append(row['pessoa']['cnae'])
    #print(cnae_secao)
    df_cnae_secao = pd.DataFrame(cnae_secao)
    #print(df_cnae_secao.head)
    #print(df_cnae_secao.shape)
    #print(df_cnae_secao.describe())
    #print(df_cnae_secao.count())
    print(df_cnae_secao['secao'].value_counts())

def edaTipoPessoa():
    col = connect_mongo('ceis', 'registro')
    result = col.aggregate( [ { '$project': { 'pessoa.tipoPessoa': 1 } } ] )
    result_list = list(result)
    pessoa_tipo = []
    for row in result_list:
        pessoa_tipo.append(row['pessoa'])
    #print(pessoa_tipo)
    df_pessoa_tipo = pd.DataFrame(pessoa_tipo)
    print(df_pessoa_tipo['tipoPessoa'].value_counts())
'''
def flattened_df(db, col):
    col = connect_mongo('ceis', 'registro')
    data = list(col.find())
    data_row_flattened = []
    for data_row in data:
        data_row_flattened.append(flatten(data_row))
    return pd.DataFrame(data_row_flattened)
    #print(df.columns)
    #for col in df.columns: 
    #    print(col)
    #print(df.pessoa_cnae_secao.value_counts())

def printwhf(to_print, header):
    print()
    print('======== '+header+' ========')
    print()
    print(to_print)
    print()
    print()

def print_all_df(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

df = flattened_df('ceis', 'registro')

dataInicioSancao = pd.to_datetime(df['dataInicioSancao'])
#plt.hist(dataInicioSancao.dropna(), bins=30)
#plt.show()

#print(df['dataInicioSancao'])
#df['dataInicioSancao'] = dataInicioSancao
#print(df['dataInicioSancao'])


df['orgaoSancionador_siglaUf'] = df['orgaoSancionador_siglaUf'].str.upper()
df['orgaoSancionador_siglaUf'].replace([''], np.nan, inplace=True)
#print_all_df(df['orgaoSancionador_siglaUf'])
#print(df.orgaoSancionador_siglaUf.value_counts())

#df_sem_pf = df.query('pessoa_tipoCodigo != "CPF"')
#print(df_sem_pf.pessoa_cnae_secao.value_counts())
df['pessoa_cnae_secao'].replace(['Sem informação'], np.nan, inplace=True)
print(df.pessoa_cnae_secao.value_counts())
print(df.pessoa_cnae_secao.count())

'''
printwhf(df.head, 'df.head')

printwhf(df.describe, 'df.describe')

printwhf(df.pessoa_tipoPessoa.value_counts(), 'df.pessoa_tipoPessoa.value_counts()')

printwhf(df.pessoa_municipio_uf_nome.value_counts(), 'df.pessoa_municipio_uf_nome.value_counts()')

printwhf(df.pessoa_cnae_secao.value_counts(), 'df.pessoa_cnae_secao.value_counts()')

printwhf(df.orgaoSancionador_nome.value_counts(), 'df.orgaoSancionador_nome.value_counts()')

printwhf(df.orgaoSancionador_siglaUf.value_counts(), 'df.orgaoSancionador_siglaUf.value_counts()')

printwhf(df.orgaoSancionador_poder.value_counts(), 'df.orgaoSancionador_poder.value_counts()')
'''
