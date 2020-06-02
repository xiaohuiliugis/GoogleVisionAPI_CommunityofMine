# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 22:55:02 2020

@author: liux29
"""

import json,os
import shutil

# text_file constains the info of the images with hispanic information
text_file = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract_1\es_14_323_Mexican_84_407_format_2.json'
input_img = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\gsv_images\tl_2018_06073'
test_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\gsv_images\test'
output_img = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\gsv_images\hisp_img'

img_list =[]
with open(text_file,'r') as text:
    img_name = json.loads(text.read())
    for img in img_name:
        img_list.append(img['coordinates'][0])
#    print (img_list[0])


for filename in os.listdir(input_img):
    if filename.rstrip('.png') in img_list:
        shutil.copy2(input_img +'\\'+ filename, output_img)
        
    

