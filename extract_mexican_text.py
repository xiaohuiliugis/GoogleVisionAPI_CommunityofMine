# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:18:03 2020

@author: liux29
"""
import json
import re,os

filename = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract_1\no_es_14.json'
out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\extract_1'

mexican_list = []
count = 1
try:
    with open (filename,encoding ='utf-8',mode ='r') as currentFile:
        json_data = json.load(currentFile)
        
        check_list = ['Mexican','Mexic','MEXIC','mexic','MexiC','MExic','El Ranchero','Macho','Las Tapas','The Tasty Quesadilla','Bigotes y Sombreros','La Placa Caliente','Tequila N' 'Taquitos','Macho Tacos','El Ranchero','Las Tapas','La Haba Burrito','El Ranchero Baile','La Sangria Sabroso','El Burrito Haba','¡Olé, Olé, Olé!','Los Amigos Restaurante','The Enchilada Man','Restaurante de Mexico','Three Amigos','Margaritas','La Familia Restaurante','Hot Tamales','Burrito Country','Mis Amigos Restaurante','Enchiladas','Nacho Queso','Su Vecindario Restaurante','Uno, Dos, Tequila','Tiempo de Salsa','Mas Tequila','Beans N','Rice','Picante','Frijoles Picante','Carmelitas','Sombreros','Nachos Crujiente','aguardenteria','azucareria','bizcocheria','boleteria','cafeteria','calceteria','carniceria','charcuteria','cerveceria','confiteria','drogueria','ebanisteria','ferreteria','floristeria','fruteria','heladeria','herboristeria','herreria','joyeria','jugueteria','lavanderia','lecheria','lenceria','libreria','muebleria','panaderia','papeleria','pasteleria','peluqueria','perfumeria','pescaderia','pizzeria','plateria','pulperia','ropavejeria','salchicheria','sastreria','sombrereria','tabaqueria','tapiceria','tintoreria','verduleria','zapateria','abierto','cajero','cerrado','descuento, rebaja','empuje','entrada','jale','oferta','precios bajos','tienda']
        for item in json_data:
             if any(x in item['description'] for x in check_list):
                mexican_list.append(item)
                #print (mexican[:])
                print (mexican_list)
                count = count+1
                print(count)
                
        try:    
            with open(os.path.join(out_dir, 'Mexican_16.txt'),'w') as json_file:
                json.dump(mexican_list, json_file, indent =2, sort_keys = True) 
        except BaseException as e:
            print ('find error: '+str(count))          
        json_file.close()    
                
            
                       
#            text_description = item['textAnnotations'][0]['description']
#            
#            
#            if (x in text_description for x in check_list) :
#                mexci_dict = {'locale': item['textAnnotations'][0]['locale'], 'description':text_description,'coordinates':coordinates,'lat':lat,'lon':lon}
#                mexican.append(mexci_dict)
#                print(mexci_dict)
#                
#                count=count+1
#                print (count)
#        
#        with open(os.path.join(out_dir, 'Mexican_14.txt'),'w') as json_file:
#            json.dump(mexican, json_file, indent =2, sort_keys = True) 
#            
except BaseException as e:
    print (e)  
    
            