
from __future__ import print_function
import numpy as np
import pandas as pd
import nltk
import re
#import os
#import codecs
from sklearn import feature_extraction
#import mpld3



df = pd.read_csv('sources/CEIS_NORMALIZED.csv', encoding='utf-8')

orgao_sancionador = df['ORGAO SANCIONADOR']

stopwords = nltk.corpus.stopwords.words('portuguese')

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("portuguese")

'''
for orgao in orgao_sancionador:
    #print(orgao)
    print(tokenize_only(orgao))
'''

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


#not super pythonic, no, not at all.
#use extend so it's a big flat list of vocab
orgao_stemmed = []
orgao_tokenized = []
for orgao in orgao_sancionador:
    allwords_stemmed = tokenize_and_stem(orgao) #for each item in 'orgao_sancionador', tokenize/stem
    orgao_stemmed.extend(allwords_stemmed) #extend the 'orgao_stemmed' list
    
    allwords_tokenized = tokenize_only(orgao)
    orgao_tokenized.extend(allwords_tokenized)

orgao_frame = pd.DataFrame({'words': orgao_tokenized}, index = orgao_stemmed)

#print('there are ' + str(orgao_frame.shape[0]) + ' items in orgao_frame')
#print(orgao_frame.head())


from sklearn.feature_extraction.text import TfidfVectorizer

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words=stopwords,
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(orgao_sancionador) #fit the vectorizer to orgao_sancionador

#print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)


from sklearn.cluster import KMeans
num_clusters = 10
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

from sklearn.externals import joblib

#uncomment the below to save your model 
#since I've already run my model I am loading from the pickle

joblib.dump(km,  'clusterizerModel.pkl')

km = joblib.load('clusterizerModel.pkl')
clusters = km.labels_.tolist()

'''
categorias = { 'orgao': orgao_sancionador, 'cluster': clusters }

frame = pd.DataFrame(categorias, index = [clusters] , columns = ['orgao', 'cluster'])

frame['cluster'].value_counts() #number of orgaos per cluster (clusters from 0 to 4)

grouped = frame['orgao'].groupby(frame['cluster']) #groupby cluster for aggregation purposes

grouped.mean() #average rank (1 to 100) per cluster
'''



print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    
    for ind in order_centroids[i, :10]: #replace 6 with n words per cluster
        print(' %s' % orgao_frame.loc[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
        #print(orgao_frame)
    print() #add whitespace
    print() #add whitespace
    
print()
print()

