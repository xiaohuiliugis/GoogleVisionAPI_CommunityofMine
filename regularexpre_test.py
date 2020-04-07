# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 02:36:27 2020

@author: liux29
"""

import re

FOLDER_PATH = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\workflow\32.619924266559,-116.986577314181_C.png'



image_name = (re.search("workflow\\\(.*?)\.png",FOLDER_PATH).group(0))
start = image_name.find("workflow\\")+len('workflow\\')
end = image_name.find("\.png")-3
substring = image_name[start:end]
print(substring)