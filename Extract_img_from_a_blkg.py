# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:19:28 2020

@author: liux29

1. This script first loop through a folder contains some images, extract their coordinates, put them in a list test_img_list. 
2. Then loop through all json files and get the coordinates of all images, if any of the coordinates exist in test_img_list, save the associated description, language, and coordinate information into a list of dictionaries.
3. Convert the list of dictionaries into a dataframe, then export as a csv file.
The csv file will then be exported to ArcGIS online to convert to a shapefile. 

@author: liux29
"""

#from google.cloud import storage
#from google.cloud import vision_v1
#from google.cloud.vision_v1 import enums
import os,re
import json
import glob
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from shapely.geometry import shape
import fiona
from geopandas.geoseries import *
import ogr
import shutil


blkg_img_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Validation\img_repetition\60730108002'
json_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\G_VisionAPI_DetectedText'
test_json_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\test_json_dir'

regex_1 = "([^\s\\])_[ABCD]"
regex_2 = "^[^_]+(?=_)"

test_img_list =[]
for filename in os.listdir(blkg_img_dir):
    coor = re.findall(regex_2, filename.rstrip('.png'))
#    print (coor)
    lat = float(coor[0].split(',')[0])
    lon = float(coor[0].split(',')[1])
    test_img_list.append((lon,lat))
        
#print (test_img_list)


#out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract'
out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract_1'
#out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract_0'
input_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\out_folder'
#input_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\out_folder_0'
test_in_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\test'
test_out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\test_output'

try:
    # read json files in a folder
    no_es_text_content =[]
    es_text_content =[]
    road_sign = []
    public_venue =[]
    only_number = []
    count=1
    injson_count=1
    
    test_blkg = {}
    test_blkg_list =[]
    count_2 = 0
    count_1= 0
    for filename in glob.glob(os.path.join(json_dir,'*.json')):
        with open (filename,encoding ='utf-8',mode ='r') as currentFile:
#            data = currentFile.read()
            json_data = json.load(currentFile)
            
            #extract the coordinate from the image name
            regex_3 ="tion\/0\d\d\/(.*?)\.png"
#            regex_2 ="out_folder\\\(\S+)\.json"
            #extract latitude from the coordinate list
            regex_4 = "(\S+)\,"
            #extract longitude from the coordinate list
            regex_5 = r",([-+]?\d*\.\d+|\d+)"
            
            
            
            for item in json_data['responses']:
                coordinates =re.findall(regex_3,item['context']['uri'])
                              
                lat_0 = re.search(regex_4,coordinates[0])
                lat = float(lat_0[0].replace(',', ''))
                
                lon_0 = re.findall(regex_5,coordinates[0])
                lon = float(lon_0[0].replace(',', ''))
                #print(lat,lon)
                                
                if (lon,lat) in test_img_list:
                    
                    count_2+=1              
                    test_blkg['description'] = item['textAnnotations'][0]['description']
                    test_blkg['language'] = item['textAnnotations'][0]['locale']
                    test_blkg['lat'] = lat
                    test_blkg['lon'] = lon
                    print (lat,lon)
                    # Important fact on append dictionary!
                    # create a shallow copy of test_blkg, and then append it to test_blkg_list
                    # without creating a shallow copy, it will append the address of each dictionary to the list, and retrieve the values from the same address, which will point to the same value at the end of the for loop. This cause the list to contain 360 same dictionaries, namely, 360 identical records
                    
                    copy_test_blkg=test_blkg.copy()
                    test_blkg_list.append(copy_test_blkg)
        count_1+=1
        print(count_1)
#        print('{}.filename:{}'.format(count_1,filename[-25:]))  
    df = pd.DataFrame(test_blkg_list)
    df.to_csv(r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Validation\img_repetition\test_blkg.csv')
    print (df.head())
    print (count_2)
                
                    
                
                
#             
#    overlap_list =[]
#    count = 0
#    for img in all_img_list:
#        if img in test_img_list:
#            overlap_list.append(img)
#            count +=1
#    print (count)
            
                
                
            

#            print (json_data)
            
            
except BaseException as e:
    print (e)