# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:01:33 2020

@author: liux29
"""
import re

filename = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\out_folder\2432output-1-to-99.json'


##regex_2 ="out_folder_0\(\d*.+?)\.png"
regex_2 ="out_folder\\\(\S+)\.json"

result = re.findall(regex_2,filename)
print (result)
#
#uri = r"gs://acculturation/010/33.2307514745719,-116.378659169056_D.png"
#regex ="tion\/0\d\d\/(.*?)\.png"
#
#result_2 = re.findall(regex,uri)
#print (result_2)



cor = ['32.7368638259421,-117.033245462116_B.png']

regex_3 = "(\S+)\,"


lat_0 = re.search(regex_3,cor[0])
lat = float(lat_0[0].replace(',', ''))
print(type(lat))


regex_5 = r",([-+]?\d*\.\d+|\d+)"


lon_0 = re.findall(regex_5,cor[0])
lon = float(lon_0[0].replace(',', ''))

print(type(lon))

text = 'fast'
text_2 = text.replace('\n©','')
print (text_2)

text_3 = "20130 "
if text_3.strip().isdigit():
    print('only digit')