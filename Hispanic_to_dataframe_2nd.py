# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:19:27 2021

@author: liux29
"""
import json,os,re
import shutil
import pandas as pd


text_file = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\es_14_323_Mexican_1767_sum_2090_format.json'
input_img = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Hispanic_image_2nd_rnd'


#input_img folder contains the final 1845 images that had Hispanic related signs
regex_1 = "^[^_]+(?=_)_[ABCD]"
coor_lst =[]
for filename in os.listdir(input_img):
    coor = re.findall(regex_1, filename.rstrip('.png'))
    coor_lst.append(coor[0])
    
# text_file contains the json file of the 2090 images,the json file contains the description, languages, lat, lon. This step will extract the description, lat, lon, information and save as a csv file for final map making. 
img_list =[]
hispanic =[]
with open(text_file,'r') as text:
    img_name = json.loads(text.read())
    for img in img_name:
        his_dict = {}
        if img['coordinates'][0] in coor_lst:
            
            his_dict['description'] = img['description']
            his_dict['language'] = img['locale']
            his_dict['lat'] = img['lat']
            his_dict['lon'] = img['lon']
            
            hispanic.append(his_dict)
            
    df= pd.DataFrame(hispanic)
    df.to_csv(r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\hispanic_df_2nd.csv')
    
            
            
            
            








    