# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:27:54 2021

@author: liux29
"""

import json,os
import shutil

# text_file constains the info of the images with hispanic information
text_file = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\es_14_323_Mexican_1767_sum_2090_format.json'
input_img = r'C:\Users\liux29\Downloads\images\tl_2018_06073'
test_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\gsv_images\test'
output_img = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Hispanic_image_2nd_rnd'

img_list =[]
with open(text_file,'r') as text:
    img_name = json.loads(text.read())
    for img in img_name:
        img_list.append(img['coordinates'][0])
#    print (len(img_list))


for folder in os.listdir(input_img):
    for filename in os.listdir(input_img + '\\'+ folder):
        if filename.rstrip('.png') in img_list:
            shutil.copy2(input_img + '\\'+ folder +'\\'+ filename, output_img)
        