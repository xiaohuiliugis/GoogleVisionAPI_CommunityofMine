# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 11:23:32 2021
# this step exports the records whose coordinates do not match any repetitive records in the repetitive IDs file and user generaged image IDs. Then extract records w/ Hispanic info. 
05/04/21: this version did not work
@author: liux29
"""

import csv,os
import json
import pandas as pd

from rapidfuzz import fuzz

# The below file "no_es_n_es_14.json" contains both english and spanish text records
filename = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\no_es_n_es_14.json'
out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories'
repetitiveID = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\2nd_ID_of_Repititive GSV_image_to remove from no_es_14.csv'
user_img_ID = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\ID_of_User image _to remove from no_es_14.csv'

# Those street names matched records in GSV, so need to be removed from GSV so that the remining GSV do not contain many street name text
matched_street_ID = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\gsv_cor_of_street_name_to_remove.csv'


street_names_remove =[]
with open(matched_street_ID,'r') as street_names:
    reader = csv.reader(street_names)
    for row in reader:
        street_names_remove.append(row[0])
"""
The above file "2nd_ID_of_Repititive GSV_image_and User image _to remove from no_es_14.csv" contains the repetitive IDs and IDs of user generated 
"""
repeID_list =[]
with open(repetitiveID) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        repeID_list.append(row[0])

''' create a list with IDs of user contributed images
'''
user_img_ID_lst =[]
with open(user_img_ID) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        user_img_ID_lst.append(row[0])


no_rep_street_user_mexican_coor = []
no_rep_street_user_mexican_js =[]
count = 1
no_rep_list = []
json_list = []
shared_list =[]
match_score =[]
no_rep_street_user =[]

 #skip the images's content that only contain google logos from the extracted text
google_logo = ['2019 ','O','© "','Google ','\u00a9','ogle','Coogle','Google ......','Goog ',' Google ','Gongle,','oogle ','Google','Soogle ','© ','\u00a9 Google\nGoogle\n','Google\n\u00a9 Google\n','Googler\n© Google\n','© Google\nGoogler\n','© Google\nGoogle\n%3\n','©Google\nGoogle\n','O Google\nGoogle\n','ogle\n© Google\nGoogle\n']

check_list = ['El Ranchero','Macho','Las Tapas','The Tasty Quesadilla','Bigotes y Sombreros','La Placa Caliente','Tequila N','Taquitos','Macho Tacos','El Ranchero','Las Tapas','La Haba Burrito','El Ranchero Baile','La Sangria Sabroso','El Burrito Haba','¡Olé, Olé, Olé!','Los Amigos Restaurante','The Enchilada Man','Restaurante de Mexico','Three Amigos','Margaritas','La Familia Restaurante','Hot Tamales','Burrito Country','Mis Amigos Restaurante','Enchiladas','Nacho Queso','Su Vecindario Restaurante','Uno, Dos, Tequila','Tiempo de Salsa','Mas Tequila','Picante','Frijoles Picante','Carmelitas','Sombreros','Nachos','Crujiente','aguardentería ','azucarería ','bizcochería ','boletería ','cafetería ','calcetería ','carnicería ','charcutería ','cervecería ','confitería ','droguería ','ebanistería ','ferretería ','floristería ','frutería ','heladería ','herboristería ','herrería ','joyería ','juguetería ','lavandería ','lechería ','lencería ','librería ','mueblería ','panadería ','papelería ','pastelería ','peluquería ','perfumería ','pescadería ','pizzería ','platería ','pulpería ','ropavejería ','salchicheria ','sastrería ','sombrerería ','tabaquería ','tapicería ','tintorería ','verdulería ','zapatería ','cajero — cashier','cerrado — closed','descuento, rebaja — discount','empuje — push (on a door)','entrada — entrance','jale — pull (on a door)','oferta — sale','precios bajos — low prices','tienda','shop','Mexico','Colombia','Argentina','Bolivia','Chile','Cuba','Dominican Republic','Ecuador','El Salvador','Guatemala','Honduras','Nicaragua','Peru','Venezuela','entregamos ','Tijuana','Paloma','chula','Vista','Camino De Norte','CANASTO','Palomar','Peligro','Hidalgo','Hodalgo','El Camino eal','Rio ','Verde ','El Cajon','De La','Baja','Baja Mex','Ysidro','CASA DE CAMBIO','VALERO','PLAZA MAYO','La Amistad','OTAY MESA','agencia','aduan','FRONTERA','SIEMPRE','ENSENADA','AVENIDA DE LA FUENTE','Enrlico','Caliente','MARISCOS','ga chien er ','cha trung','el toro taqueria','carniceria','pollos ','de','rancho','seguro de auto con ','matricula','el cajon ','El Camino','Avenida De Anita','El Camino Real','Avenida De Louisa','Avenida De','Calle','Calle Susana','Bernado','Camino ','del','Norte','El Camino Real','Rio Verde','Hidalqo']

try:
    
    with open (filename,encoding ='utf-8',mode ='r') as currentFile:
        json_data = json.load(currentFile)
           
# this step exports the records whose coordinates do not match any repetitive records in the repetitive IDs file.
        count_time=0
        for item in json_data:
    #replace different forms of google logos 
            text_description = item['description'].replace('\n©','').replace('Google\n','').replace('\nGoogle','').replace('\u00a9','').replace('Google','').replace('Соogle ','').replace('oogle ','').replace('Soogle ','').replace('Goog ','').replace("Gnogl ",'').replace("Geegle ",'').replace("2019 ",'').replace("Chogle ",'').replace("Googla ",'').replace("\n",'').replace("Gnogl ",'').replace("Coog ",'').replace("Googlu ",'').replace("ngle ",'').replace("bogle",'').replace("Coode ",'').replace("1ogle ",'').replace(r"\u042 ",'').replace("gle ",'').replace("oge ",'').replace(r"\u63a2 ",'').replace(r"\u6548  ",'').replace("Goo ",'').replace("20190 ",'').replace(".Cogle ",'').replace("Go ",'').replace("Googl. ",'').replace("Gog ",'').replace("Goodle ",'').replace("oge ",'').replace(r"\u",'').replace("Gog",'').replace("2018 ",'').replace("Cood",'').replace("Gogle ",'').replace("Gpogle",'').replace("019 ",'').replace("018 ",'').replace("Googl",'').replace("ogle",'').replace("Gogole",'').replace("Ceegle",'').replace("Sougle",'').replace("Cgle",'').replace("Gooole ",'').replace(" Goc",'').replace("GO ",'').replace("ooog",'').replace("Good",'').replace("2017",'').replace("2016",'').replace("201",'').replace("Gootle ",'').replace(" Gon",'').replace("2015",'').replace("Coogl",'').replace("Cougl ",'').replace("Cocgle ",'').replace("Gopgle",'').replace("Gooe ",'').replace("Gonnie",'').replace("Geogla",'').replace("Goonle ",'').replace("Goodl ",'').replace("doogl ",'').replace("Gepgle ",'').replace("CoGegale",'').replace("CGonal ",'').replace("Gooni ",'').replace("Goodl",'').replace("2020 ",'').replace("GOog",'').replace("Guegle",'').replace("Gooale ",'').replace("Cooglo ",'').replace("Goole ",'')
          
            if (item['description'] in google_logo) or (len(text_description.strip())<=3):
                continue
            count_time=count_time+1
            #print(f'{count_time} for iteration.............')   
           #exclude user contributed, repetitive, and street sign images
            if item['coordinates'][0] not in user_img_ID_lst + repeID_list + street_names_remove:
                #select images with Hispanic information
                if any(x in item['description'] for x in check_list):
                    print (item['coordinates'][0])
                    no_rep_street_user_mexican_js.append(item)
                #print (mexican[:])
                    #print (no_rep_street_user_mexican_js)
                
        try:    
            with open(os.path.join(out_dir, '4th_Hispanic_en_n_es.txt'),'w') as json_file:
                json.dump(no_rep_street_user_mexican_js, json_file, indent =2, sort_keys = True)
        except BaseException as e:
            print (e)     
        
                
except BaseException as e:
    print (e)  
    