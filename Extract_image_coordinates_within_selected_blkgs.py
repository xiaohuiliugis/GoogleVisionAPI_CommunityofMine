# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 22:52:00 2020
This code is to extract images that fall within 9 selected census blockgroups. 
The name of images contain the coordinates of the locations where the images were taken. 
Steps:
    1. Loop through folder, extract the coordinate pairs and covert to point geometry
    2. Loop through shapefile of 9 census block group), check which point in P_list falls within each block group, save those points in pnt_cord list. 
    3. Loop through the folder containing the images, check if the coordinates of each images can be found from the above pnt_cord (the points within each census block group). If so, copy the images to a new folder.

@author: liux29
"""

import os
import re
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from shapely.geometry import shape
import fiona
from geopandas.geoseries import *
import ogr
import shutil


input_img = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV text_detection\GSV_Vision_API_Code\Hispanic_image'
input_img_2 = r'C:\Users\liux29\Downloads\images\tl_2018_06073'
shapefile_dir = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\CoM_GIS_Data\GIS\Data_validation\blkg'
out_img = r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\CoM_GIS_Data\GIS\Data_validation\out_image'

'''
This block of code identify the list of shapefiles in the folder
'''
shp_driver = ogr.GetDriverByName('ESRI Shapefile')
shapefile_list =[]
for shp_file  in os.listdir(shapefile_dir):
    if shp_file.endswith(".shp"):
        full_shapefile_path = os.path.join(shapefile_dir,shp_file)
        shapefile_list.append(full_shapefile_path)
        
regex_1 = "([^\s\\])_[ABCD]"
regex_2 = "^[^_]+(?=_)"


'''loop through the folders that contains images, extract coordinates, convert them to Point geometry
'''
P_list=[]
for folder in os.listdir(input_img_2):
    for filename in os.listdir(input_img_2 + '\\'+ folder):
        coor = re.findall(regex_2, filename.rstrip('.png'))
        lat = float(coor[0].split(',')[0])
        lon = float(coor[0].split(',')[1])
        P_list.append(Point(lon,lat))

'''Loop through shapefiles (census block group), check which point in P_list falls within each block group, save those points in pnt_cord list. 
'''        
for shapefile in shapefile_list:
    for pol in fiona.open(shapefile):
        geometry = pol['geometry']
  # the geometry contains (x,y,z), the next line remove the z coordinates 
    poly_lst = [tuple(ele for ele in sub if ele!=0.0) for sub in geometry['coordinates'][0]]
    poly = Polygon(poly_lst)
    
    i=0
    within_p = []
    pnt_cord =[] 
    for p in P_list:
        if p.within(poly):
            pnt_cord.append(p.coords[0])
            i=i+1
    print(i)
    # get the name of the output folder to store the extracted image
    shp_name = re.search("blkg\\\(.*?)\.shp",shapefile).group(0)
    print (shp_name)
'''Loop through the folder containing the images, check if the coordinates of each images can be found from the above pnt_cord (the points within each census block group). If so, copy the images to a new folder.
'''        
    for folder in os.listdir(input_img_2):
        for filename in os.listdir(input_img_2 + '\\'+ folder):
            coor = re.findall(regex_2, filename.rstrip('.png'))
            lat = float(coor[0].split(',')[0])
            lon = float(coor[0].split(',')[1])
            if (lon,lat) in pnt_cord:
                shutil.copy2(input_img_2 +'\\'+ folder +'\\'+ filename, out_img +'\\'+ shp_name.strip('blkg\\').strip('.shp'))

'''
The following is to extract coordinates from images name, convert to a geopandas dataframe,and visualize it
#lat_ls =[]
#lon_ls =[]
#
#for folder in os.listdir(input_img_2):
#    for filename in os.listdir(input_img_2 + '\\'+ folder):
#        coor = re.findall(regex_2, filename.rstrip('.png'))
#        lat = float(coor[0].split(',')[0])
#        lon = float(coor[0].split(',')[1])
#        lat_ls.append(lat)
#        lon_ls.append(lon)
                
#df =pd.DataFrame(
#        {'ID':list(range(1,i+1)),
#         'lat':lat_ls,
#         'lon':lon_ls})
#gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))

#base = MJ_BLKG.plot(color ='white', edgecolor='black')
#gdf.plot(ax= base,marker='o', color='red', markersize=5)

#base = High_blkg.plot(color ='white', edgecolor='black')
#gdf.plot(ax= base,marker='o', color='red', markersize=5)   
