# -*- coding: utf-8 -*-
"""
# this script used knn matrix to compute the match score of GSV text and San Diego street names. Exact match will get a score of -1, and two records with almost no match will get a score close to 0. 
06/02/21: 
@author: liux29
"""

import csv,os,re
import json
import pandas as pd

from tqdm import tqdm
from ftfy import fix_text

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

# conda install -c conda-forge sparse_dot_topn to install
# if error occurs, then update conda first by running: conda update --force conda 
import sparse_dot_topn.sparse_dot_topn as ct

#!to install nmslib, use: conda install -c conda-forge nmslib
import nmslib
from scipy.sparse import csr_matrix # may not be required 
from scipy.sparse import rand # may not be required

# The below file "no_es_n_es_14.json" contains both english and spanish text records
filename = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\no_es_n_es_14.json'
filename_test = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\no_es_n_es_14_test.json'

out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories'

street_name_file_test = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\SanDiegoCounty_RoadNames_Jay_XL_revised_test.csv'

street_name_file = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\SanDiegoCounty_RoadNames_Jay_XL_revised.csv'

'''Create a dataframe Road_Name to store the road names in San Diego
'''
street_name_lst =[]
with open(street_name_file,'r') as street_names:
    reader = csv.reader(street_names)
    for row in reader:
        street_name_lst.append(row[0])
df_street_name = pd.DataFrame(street_name_lst, columns =['street_name'])
        
''' ngrams to both clean the text data and also split text into ngrams
'''
def ngrams(string, n=3):
    string = str(string)
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'","*","å","æ","¥","®","ã","ˆ","¤","º","-","+","‡","€",]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

''' Finding close matches through cosine similarity
'''
'''
###FIRST TIME RUN - takes about 5 minutes... used to build the matching table
'''

try:
    
    with open (filename,encoding ='utf-8',mode ='r') as currentFile:
        json_data = json.load(currentFile)
        
        gsv_text = []       
# this step extract the gsv text .
        count_time=0
        gsv_text = [item['description'] for item in json_data ]
        df_CF =pd.DataFrame(gsv_text, columns =['GSV text'])
        
        vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
        tf_idf_matrix = vectorizer.fit_transform(street_name_lst)
        
        gsv_tf_idf_matrix = vectorizer.transform(gsv_text)
          
        # create a random matrix to index
        data_matrix = tf_idf_matrix#[0:1000000]
        # Set index parameters
        # These are the most important ones
        M = 80
        efC = 1000
                
        num_threads = 4 # adjust for the number of threads
        # Intitialize the library, specify the space, the type of the vector and add data points 
        index = nmslib.init(method='simple_invindx', space='negdotprod_sparse_fast', data_type=nmslib.DataType.SPARSE_VECTOR) 
        index.addDataPointBatch(data_matrix)
                
        # Create an index
        index.createIndex() 
        
        # Number of neighbors 
        num_threads = 4
        K=1
        query_matrix = gsv_tf_idf_matrix
#        query_matrix = messy_tf_idf_matrix
        
        query_qty = query_matrix.shape[0]
        nbrs = index.knnQueryBatch(query_matrix, k = K, num_threads = num_threads)
                
        mts =[]
        for i in range(len(nbrs)):
            origional_nm = gsv_text[i]
#            origional_nm = messy_names[i]
            try:
                matched_nm   = street_name_lst[nbrs[i][0][0]]
#                matched_nm   = org_names[nbrs[i][0][0]]
                conf         = nbrs[i][1][0]
            except:
                matched_nm   = "no match found"
                conf         = None
            mts.append([origional_nm,matched_nm,conf])
        
        mts = pd.DataFrame(mts,columns=['gsv_text','matched_name','conf'])
        # exports the matched result of gsv text and street names
        mts.to_csv(out_dir +'\GSV_StreetName_match_result.csv')
                        
                
except BaseException as e:
    print (e)  
    
