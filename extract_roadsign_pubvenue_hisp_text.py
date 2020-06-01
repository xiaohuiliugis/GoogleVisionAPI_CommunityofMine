# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Wed May 20 18:48:22 2020
This script loop through the folder contains json files to extracte the Language, description, and coordinate information. The json files were the output of Google Vision API.  
Set up:
    1. input folder
    2, output folder, output file name
@author: liux29
"""

#from google.cloud import storage
#from google.cloud import vision_v1
#from google.cloud.vision_v1 import enums
import os,re
import json
import glob

#storage_client = storage.Client()

##created a new GCP service account, gave it owner, cloud storage admin, and cloud storage object admin roles.
#os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\nih-nimhd-pcs-acculturation-c6066ac06d0e.json'
#bucket_name = "acculturation"
#output_folder = "/output/"
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
    for filename in glob.glob(os.path.join(input_dir,'*.json')):
        with open (filename,encoding ='utf-8',mode ='r') as currentFile:
#            data = currentFile.read()
            json_data = json.load(currentFile)
            
            regex ="out_folder\\\(\S+)\.json"

            json_file_name = re.findall(regex,filename)

            print (json_file_name)
            #extract the coordinate from the image name
            regex_1 ="tion\/0\d\d\/(.*?)\.png"
#            regex_2 ="out_folder\\\(\S+)\.json"
            #extract latitude from the coordinate list
            regex_3 = "(\S+)\,"
            #extract longitude from the coordinate list
            regex_4 = r",([-+]?\d*\.\d+|\d+)"
            injson_count=0 
            for item in json_data['responses']:
                
                injson_count=injson_count+1
#                print (injson_count)
                count=count+1
                print (count)
                coordinates = re.findall(regex_1,item['context']['uri'])
                
                lat_0 = re.search(regex_3,coordinates[0])
                lat = float(lat_0[0].replace(',', ''))
                
                lon_0 = re.findall(regex_4,coordinates[0])
                lon = float(lon_0[0].replace(',', ''))
                
                
                #skip the images's content that only contain google logos from the extracted text
                google_logo = ['2019 ','O','© "','Google ','\u00a9','ogle','Coogle','Google ......','Goog ',' Google ','Gongle,','oogle ','Google','Soogle ','© ','\u00a9 Google\nGoogle\n','Google\n\u00a9 Google\n','Googler\n© Google\n','© Google\nGoogler\n','© Google\nGoogle\n%3\n','©Google\nGoogle\n','O Google\nGoogle\n','ogle\n© Google\nGoogle\n']
                
                #replace different forms of google logos 
                try:
                    
                    text_description = item['textAnnotations'][0]['description'].replace('\n©','').replace('Google\n','').replace('\nGoogle','').replace('\u00a9','').replace('Google','').replace('Соogle ','').replace('oogle ','').replace('Soogle ','').replace('Goog ','').replace("Gnogl ",'').replace("Geegle ",'').replace("2019 ",'').replace("Chogle ",'').replace("Googla ",'').replace("\n",'').replace("Gnogl ",'').replace("Coog ",'').replace("Googlu ",'').replace("ngle ",'').replace("bogle",'').replace("Coode ",'').replace("1ogle ",'').replace(r"\u042 ",'').replace("gle ",'').replace("oge ",'').replace(r"\u63a2 ",'').replace(r"\u6548  ",'').replace("Goo ",'').replace("20190 ",'').replace(".Cogle ",'').replace("Go ",'').replace("Googl. ",'').replace("Gog ",'').replace("Goodle ",'').replace("oge ",'').replace(r"\u",'').replace("Gog",'').replace("2018 ",'').replace("Cood",'').replace("Gogle ",'').replace("Gpogle",'').replace("019 ",'').replace("018 ",'').replace("Googl",'').replace("ogle",'').replace("Gogole",'').replace("Ceegle",'').replace("Sougle",'').replace("Cgle",'').replace("Gooole ",'').replace(" Goc",'').replace("GO ",'').replace("ooog",'').replace("Good",'').replace("2017",'').replace("2016",'').replace("201",'').replace("Gootle ",'').replace(" Gon",'').replace("2015",'').replace("Coogl",'').replace("Cougl ",'').replace("Cocgle ",'').replace("Gopgle",'').replace("Gooe ",'').replace("Gonnie",'').replace("Geogla",'').replace("Goonle ",'').replace("Goodl ",'').replace("doogl ",'').replace("Gepgle ",'').replace("CoGegale",'').replace("CGonal ",'').replace("Gooni ",'').replace("Goodl",'').replace("2020 ",'').replace("GOog",'').replace("Guegle",'').replace("Gooale ",'').replace("Cooglo ",'').replace("Goole ",'')
                    
                    if (item['textAnnotations'][0]['description'] in google_logo) or (len(text_description.strip())<=3):
                        
                        continue
                              
                    road_sign_list = ['STOP','STOTOP ','STOR ','Rd','St','ST','BLVD','HWY','SPEEDLIMIT','SPEED','MPH','AVE','PARKING','FedEx','Dr','STO\nTOP','LANE','Ln','YIELD','ONEWAY','ONE WAY','Way', 'Ct']
                    
                    if any(x in item['textAnnotations'][0]['description'] for x in road_sign_list):
                        road_dict = {'locale': item['textAnnotations'][0]['locale'], 'description':text_description,'coordinates':coordinates,'lat':lat,'lon':lon}
                        road_sign.append(road_dict)
                        print(road_dict)
                    else:
                        
                        public_venue_list = ['FedEx','WELLSFARGO','WELLSFARGOATM','BANK','CHASE','HOSPITAL',"HONDA ","NISSAN ","TOYOTA ",'PENSKE','Jeep','eep ','SUBWAY ',r'macy',]
                        if any(x in item['textAnnotations'][0]['description'] for x in public_venue_list):
                            pub_venue_dict = {'locale': item['textAnnotations'][0]['locale'], 'description':text_description,'coordinates':coordinates,'lat':lat,'lon':lon}
                            public_venue.append(pub_venue_dict)
                            print(pub_venue_dict) 
                        
                        else:   
                            
                            if text_description.strip().isdigit():
                                num_dict = {'locale': item['textAnnotations'][0]['locale'], 'description':text_description,'coordinates':coordinates,'lat':lat,'lon':lon}
                                only_number.append(num_dict)
                              
                            elif item['textAnnotations'][0]['locale'] in ['es'] :
                                es_dict = {'locale': item['textAnnotations'][0]['locale'], 'description': text_description,'coordinates':coordinates,'lat':lat,'lon':lon}
                                es_text_content.append(es_dict)
                                print (es_dict)
                            else:
                                no_es_dict = {'locale': item['textAnnotations'][0]['locale'], 'description': text_description,'coordinates':coordinates,'lat':lat,'lon':lon}
                                no_es_text_content.append(no_es_dict)
                                print (no_es_dict)
                except BaseException as e:
                    print ('bad message error: '+ str(injson_count))


    with open(os.path.join(out_dir, 'onl_number_14.txt'),'w') as json_file_5:
        json.dump(only_number, json_file_5, indent =2, sort_keys = True)   

    with open(os.path.join(out_dir, 'public_venue_sign_14.txt'),'w') as json_file_4:
        json.dump(public_venue, json_file_4, indent =2, sort_keys = True)                      
        
    with open(os.path.join(out_dir, 'road_sign_14.txt'),'w') as json_file_3:
        json.dump(road_sign, json_file_3, indent =2, sort_keys = True)              
#      write the non-Spanish content           
    with open(os.path.join(out_dir, 'no_es_14.txt'),'w') as json_file_1:
        json.dump(no_es_text_content, json_file_1,indent =2, sort_keys = True)
#         write the Spanish only content
    with open(os.path.join(out_dir, 'es_14.txt'),'w') as json_file_2:
        json.dump(es_text_content, json_file_2,indent =2, sort_keys = True)
  
    #Close the input file    
    currentFile.close()
    json_file_1.close()
    json_file_2.close()
    json_file_3.close()
    json_file_4.close()
    json_file_5.close()


except BaseException as e:
    print (e)
 

                    



