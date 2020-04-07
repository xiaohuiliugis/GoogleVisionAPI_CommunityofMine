# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:51:46 2020

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

def detectText(img):
    with io.open(img,'rb') as image_file:
        content = image_file.read()
        
        image = vision.types.Image(content=content)
        response = client.text_detection(image = image)
        texts = response.text_annotations
        
        text_content =[]
        image_name = re.search("workflow\\\(.*?)\.png",img).group(0)
        
        start = image_name.find("workflow\\")+len('workflow\\')
        end = image_name.find("\.png")-3
        file_coord = image_name[start:end]
        
        for text in texts:
            dict = {'locale': text.locale, 'description': text.description,'coordinates':file_coord}
            text_content.append(dict)
        with open('text.json','w') as fp:
            json.dump(text_content[0],fp)

filename ='32.619924266559,-116.986577314181_C.png'
FOLDER_PATH = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\workflow'

    #print(detectText(os.path.join(FOLDER_PATH,filename)))
print (detectText(os.path.join(FOLDER_PATH,filename)))
    

