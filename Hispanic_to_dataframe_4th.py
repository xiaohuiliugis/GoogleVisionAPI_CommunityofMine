# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:19:27 2021

@author: liux29
"""
import json,os,re
import shutil
import pandas as pd


text_file = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\4th_Hispanic_en_n_es.json'

# text_file contains the json file of the 1784 images,the json file contains the description, languages, lat, lon. This step will extract the description, lat, lon, information and save as a csv file for final map making. 
img_list =[]
hispanic =[]
with open(text_file,'r') as text:
    img_name = json.loads(text.read())
    for img in img_name:
        his_dict = {}
 
        his_dict['description'] = img['description']
        his_dict['language'] = img['locale']
        his_dict['lat'] = img['lat']
        his_dict['lon'] = img['lon']
        
        hispanic.append(his_dict)
            
    df= pd.DataFrame(hispanic)
    df.to_csv(r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\hispanic_en_n_es_df_4th.csv')
    
            
            
            
            








    