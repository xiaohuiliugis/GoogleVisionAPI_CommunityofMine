# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 01:00:38 2020

@author: liux29
"""
import os
import random
import shutil

folder_path = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\CoM_GIS_Data\GIS\Data_validation\out_image_hispanic\60730100151'

move_file_number=1000
target_path=r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\CoM_GIS_Data\GIS\Data_validation\out_image_hispanic\random_1000_image'

image_names=os.listdir(folder_path)

move_file_names=random.sample(image_names,move_file_number)

count=1
for i_name in move_file_names:
    
    from_files=os.path.join(folder_path,i_name)
    target_files=os.path.join(target_path,i_name)
    shutil.copy2(from_files, target_files)
    count+=1
    print('processing {}/{}'.format(count,move_file_number))