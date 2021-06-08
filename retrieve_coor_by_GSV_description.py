# -*- coding: utf-8 -*-
"""
06/20/2021
# this step extract the coordinates (also the GSV's id) of images that contained street names. The coord will be used to remove the GSV with street names
@author: liux29
"""

import csv,os
import json
import pandas as pd

from rapidfuzz import fuzz

# The below file "no_es_n_es_14.json" contains both english and spanish text records
filename = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\no_es_n_es_14.json'
out_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories'
repetitiveID = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\2nd_ID_of_Repititive GSV_image_and User image _to remove from no_es_14.csv'

# Those street names matched records in GSV, so need to be removed from GSV so that the remining GSV do not contain many street name text
matched_street_names = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\GSV_contained_street_names.csv'

matched_street_names_test = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\Extracted_text_categories\GSV_contained_street_names_test.csv'

street_names_to_remove =[]
with open(matched_street_names,'r', encoding="utf8") as street_names:
    reader = csv.reader(street_names)
    for row in reader:
        street_names_to_remove.append(row)
        
print (street_names_to_remove)
"""
The above file "2nd_ID_of_Repititive GSV_image_and User image _to remove from no_es_14.csv" contains the repetitive IDs and IDs of user generated 
"""

try:
    
    with open (filename,encoding ='utf-8',mode ='r') as currentFile:
        json_data = json.load(currentFile)
        
        gsv_cor_to_remove=[]        
# this step exports the records whose coordinates do not match any repetitive records in the repetitive IDs file.
        for item in json_data:
           for x in street_names_to_remove:
               if x[0] == item['description']:
                   
                   gsv_cor_to_remove.append(item['coordinates'][0])
#                   print (gsv_cor_to_remove[:10])
        df_gsv_cor_to_remove= pd.DataFrame(gsv_cor_to_remove,columns =['cor_to_remove'])
        df_gsv_cor_to_remove.drop_duplicates(subset ="cor_to_remove",keep = False, inplace = True)
        print(df_gsv_cor_to_remove['cor_to_remove'].head())
                
        df_gsv_cor_to_remove.to_csv(out_dir +'\gsv_cor_of_street_name_to_remove.csv')



#            with open(os.path.join(out_dir, '3nd_no_rep_no_user_eng_n es_14.txt'),'w') as json_file:
#                json.dump(no_rep_list, json_file, indent =2, sort_keys = True) 
#            
#            with open(os.path.join(out_dir, 'match_score.txt'),'w') as json_file:
#                json.dump(match_score, json_file, indent =2, sort_keys = True) 
#                
#        except BaseException as e:
#            print ('find error: '+str(count))          
#        json_file.close()  

                
 
except BaseException as e:
    print (e)  
    