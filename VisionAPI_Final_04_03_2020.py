# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:51:46 2020
!!change the destination file name in line 39 before execute!!!
@author: liux29
"""

import os,io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import re
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\Images Text Recognition-COM-83a8e6192f7e.json'

client = vision.ImageAnnotatorClient()

text_content =[]

def detectText(img):
    with io.open(img,'rb') as image_file:
        content = image_file.read()
        
        image = vision.types.Image(content=content)
        response = client.text_detection(image = image)
        texts = response.text_annotations
        
        try:
            image_name = re.search("test_images\\\(.*?)\.png",img).group(0)
            
            start = image_name.find("test_images\\")+len('test_images\\')
            end = image_name.find("\.png")-3
            file_coord = image_name[start:end]
            
            
            dict = {'locale': texts[0].locale, 'description': texts[0].description,'coordinates':file_coord}
            text_content.append(dict)
            with open('text_894.json','w') as fp:
                json.dump(text_content,fp,indent =4, sort_keys = True)
        except BaseException as e:
            print (e)
            
#filename ='32.619924266559,-116.986577314181_C.png'
FOLDER_PATH = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\test_images'

    #print(detectText(os.path.join(FOLDER_PATH,filename)))
#print (detectText(os.path.join(FOLDER_PATH,filename)))

for filename in os.listdir(FOLDER_PATH):
    print (filename)
    
    #print(detectText(os.path.join(FOLDER_PATH,filename)))
    detectText(os.path.join(FOLDER_PATH,filename))

