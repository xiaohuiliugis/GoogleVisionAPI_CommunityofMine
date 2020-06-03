# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:00:49 2020

@author: liux29
"""

import pandas as pd
import re
import json
from pandas.io.json import json_normalize

input_file = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract_1\es_14_323_Mexican_84_407_format.json'
# '0327_0503_geo_txt.txt' can be mapped,but the there was limited # for each race or career group, thus was not used and adopted the file with city name
#input_file = r'C:\data\covid\COVID_analysis\0327_0503_geo_txt.txt'

f = open(input_file,'r')
hispanic =[]

with open (input_file,encoding ='utf-8',mode ='r') as currentFile:
    
    json_data = json.load(currentFile)
    for item in json_data:
        try:
            his_dict = {}
                # if tweet is retweet, or not geo_enabled, or place is null, filter out those tweets
            his_dict['description'] = item['description']
            his_dict['language'] = item['locale']
            his_dict['lat'] = item['lat']
            his_dict['lon'] = item['lon']

            hispanic.append(his_dict)

        except BaseException as e:
            print (e)
    df = pd.DataFrame(hispanic)
    df.to_csv(r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract_1\hispanic_df.csv')
    #Close the input file
    f.close()              
                


        