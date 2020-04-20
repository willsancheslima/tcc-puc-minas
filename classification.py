#Ppython program to check if two  
# to get unique values from list 
# using numpy.unique  
import numpy as np
import pandas as pd
  
# function to get unique values 
def unique(list1): 
    x = np.array(list1) 
    return np.unique(x)


df = pd.read_csv('sources/CEIS_NORMALIZED.csv', encoding='utf-8')
orgao_sancionador = df['ORGAO SANCIONADOR']

df_unique = pd.DataFrame(unique(orgao_sancionador))

df_unique.to_csv('sources/orgao_unique.csv', index=False)