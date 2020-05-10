import pandas as pd
import numpy as np
import pymongo
import json
from flatten_json import flatten
import matplotlib.pyplot as plt


def connect_mongo(db, col, host='localhost', port=27017):
    client = pymongo.MongoClient(host, port)
    db = client[db]
    return db[col]

def insertCol(db, col, data):
    col = connect_mongo(db, col)
    result = col.insert(data)
    print(str(result))
    
def getListFromMongoCol(db, col):
    col = connect_mongo(db, col)
    data = list(col.find())
    return data

def flattenListAsDF(data):
    data_row_flattened = []
    for data_row in data:
        data_row_flattened.append(flatten(data_row))
    return pd.DataFrame(data_row_flattened)
    #print(df.columns)
    #for col in df.columns: 
    #    print(col)
    #print(df.pessoa_cnae_secao.value_counts())

def groupedBarWithLabels(bar1, bar2, labels, 
    labelBar1='labelBar1', labelBar2='labelBar2', ylabel='ylabel', title='title'):
    x = np.arange(len(labels))  # the label locations
    width = 0.4  # the width of the bars
    fig, ax = plt.subplots()
    ax.bar(x - width/2, bar1, width, label=labelBar1)
    ax.bar(x + width/2, bar2, width, label=labelBar2)
    fig.tight_layout()
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()
    plt.show()

def jsonprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def print_all_df(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

def printwhf(to_print, header):
    print()
    print('======== '+header+' ========')
    print()
    print(to_print)
    print()
    print()


'''
# QUERY PANDAS
#df_sem_pf = df.query('pessoa_tipoCodigo != "CPF"')
#print(df_sem_pf.pessoa_cnae_secao.value_counts())
df['pessoa_cnae_secao'].replace(['Sem informação'], np.nan, inplace=True)
#print(df.pessoa_cnae_secao.value_counts())
#print(df.pessoa_cnae_secao.count())

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