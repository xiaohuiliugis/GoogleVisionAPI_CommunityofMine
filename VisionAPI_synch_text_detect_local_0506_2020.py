# -*- coding: utf-8 -*-
"""
Created on Tue May  5 20:44:54 2020
This script runs synchronous mode from Spyder and send images on local disk to the cloud, after execution, send the result back to local computer. Will work for small # of images as this process is slow

@author: Drs, Xiaohui Liu and Haipeng Tang
"""


import os,io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import re
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\nih-nimhd-pcs-acculturation-249a30766dbf.json'

client = vision.ImageAnnotatorClient()
i=1
outfile = "text_"+ "1" + ".json" 
open(outfile,'w')
f_size = os.path.getsize(outfile)
text_content =[]

            
#filename ='32.619924266559,-116.986577314181_C.png'
FOLDER_PATH = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\test_images'

    #print(detectText(os.path.join(FOLDER_PATH,filename)))
#print (detectText(os.path.join(FOLDER_PATH,filename)))
# track the # of processed image
j=0
for filename in os.listdir(FOLDER_PATH):
    print (filename)
    j= j+1
    print ("Processed: %d images"%j)
    
    
    #print(detectText(os.path.join(FOLDER_PATH,filename)))
#    detectText(os.path.join(FOLDER_PATH,filename))
    img=os.path.join(FOLDER_PATH,filename)
    with io.open(img,'rb') as image_file:
        content = image_file.read()
        
        image = vision.types.Image(content=content)
        response = client.text_detection(image = image)
        texts = response.text_annotations
        
        try:
             # slice the file path, from "test\32.573815034,-117.102451419987_A.png"
            image_name = re.search("test_images\\\(.*?)\.png",img).group(0)
# from the sliced file path, find the position of "test\" and get its length, which is the start position to get the 
            # coordinate value
            start = image_name.find("test_images\\")+len('test_images\\')
            # get the end position, which is the "." before "png"
            end = image_name.find("\.png")-3
            file_coord = image_name[start:end]
            
            # the element that will be extracted from the response result.
            dict = {'locale': texts[0].locale, 'description': texts[0].description,'coordinates':file_coord}
            text_content.append(dict)
            
            outfile = "text_"+ str(i) + ".json" 
            f_size = os.path.getsize(outfile)       
            
            # this cooresponds to the size limit of Json file (10MB)
            if f_size < 9999700:
#                outfile = "text_"+ str(i) + ".json" 
#                f_size = os.path.getsize(outfile)
                with open(outfile,'w') as fp:
                    json.dump(text_content,fp,indent =4, sort_keys = True)   
                
            else: 
                text_content=[]
#                i=cell(f_size/1000)
                i=i+1
                outfile="text_"+str(i)+".json"
#                f_size = os.path.getsize(outfile)
                with open(outfile,'w') as fp:
                    json.dump(text_content,fp,indent =4, sort_keys = True)                                
                   
        except BaseException as e:
            print (e)    
    
    
    
    
    
    
    
    
    
    
    
    
