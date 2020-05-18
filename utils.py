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

def serieToPercQtdeCSV(serie, serieName):
    perc = serie.value_counts(normalize=True)*100
    qtde = serie.value_counts()
    dfPercQtde = pd.concat([perc, qtde], axis=1, sort=False)
    dfPercQtde.to_csv('sources/graph.'+serieName+'.csv')