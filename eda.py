import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import requests
import json

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


result = col.aggregate( [ { '$project': { 'pessoa.tipoPessoa': 1 } } ] )
result_list = list(result)
pessoa_tipo = []
for row in result_list:
    pessoa_tipo.append(row['pessoa'])
#print(pessoa_tipo)
df_pessoa_tipo = pd.DataFrame(pessoa_tipo)
print(df_pessoa_tipo['tipoPessoa'].value_counts())