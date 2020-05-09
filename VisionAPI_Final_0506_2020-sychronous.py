# -*- coding: utf-8 -*-
"""
Created on Tue May  5 20:44:54 2020
!!change the destination file name in line 39 before execute!!!
1. Log on to Google Cloud console using liux29@nih.gov
2. Follow the video tutorial https://www.youtube.com/watch?v=wfyDiLMGqDM, to enable Vision API, create service account and api credential
3. Update the name of API credential, folder path, and output file name. Make sure there are images in the folder path

@author: liux29
"""


import os,io
from google.cloud import vision
from google.cloud.vision import types
import re
import json

# the Google Vision API  credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\nih-nimhd-pcs-acculturation-249a30766dbf.json'

client = vision.ImageAnnotatorClient()
i=1

#set the name of the initial file
outfile = "text_"+ "1" + ".json" 
open(outfile,'w')
#get the size (byte) of the output json file
f_size = os.path.getsize(outfile)
text_content =[]

            
#filename ='32.619924266559,-116.986577314181_C.png'
FOLDER_PATH = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\gsv_images\images\test_images'

#print(detectText(os.path.join(FOLDER_PATH,filename)))
#print (detectText(os.path.join(FOLDER_PATH,filename)))
#use j to track the # of processed image
j=0
#loop through the images in the folder path
for filename in os.listdir(FOLDER_PATH):
    print (filename)
    j= j+1
    print ("Processed: %d images"%j)
    
    
#    detectText(os.path.join(FOLDER_PATH,filename))
    img=os.path.join(FOLDER_PATH,filename)
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
            
            # extracted text from images will be stored in a dictionary and append to text_content
            dict = {'locale': texts[0].locale, 'description': texts[0].description,'coordinates':file_coord}
            text_content.append(dict)
            
            # Each time a json file reach 10MB, create a new file and name it based on the sequence #. i.e., the 2nd created file 
            # will be named text_2.json
            outfile = "text_"+ str(i) + ".json" 
            f_size = os.path.getsize(outfile)
            
            if f_size < 9999700:
#                outfile = "text_"+ str(i) + ".json" 
#                f_size = os.path.getsize(outfile)
                with open(outfile,'w') as fp:
                    json.dump(text_content,fp,indent =4, sort_keys = True)   
                
            else: 
                text_content=[]

                i=i+1
                outfile="text_"+str(i)+".json"
#                f_size = os.path.getsize(outfile)
                with open(outfile,'w') as fp:
                    json.dump(text_content,fp,indent =4, sort_keys = True)                                
                   
        except BaseException as e:
            print (e)    
    
    
    
    
    
    
    
    
    
    
    
    
