# -*- coding: utf-8 -*-
"""
The xiaohui.liu@nih.gov account was created on May 5th, and 1.12 million images processing finished on May 23rd, 2020
Created on Sun May 17 10:31:33 2020
set up:
    1) set os.environ to correct path to the json key file
    2) set the folder of input file: blobs = storage_client.list_blobs(bucket_name, prefix="001/3", delimiter="/")
    3) set the output folder path if needed

 **Loop through folders**
Each run of the code is for N = 113,234 files in each of the 10 folders, which will take 1144 round( 1143*99 + 77(last round) = 113,234). In order to put the output file from the second folder(third...) into the same output_uri, count_2 needs to start from 1145,here is the full details on values of count_2 for each round:
2(1145)
3(2289)
4(3433)
5(4577)
6(5721)
7(6865)
8(8009)
9(9153)
10(10297)

***If timeout error happens, a few places needs to be modified:
	1) j (use this counter to mark the position of processed images. If one execution ended at j position, then next time start at j+1 position. This will determine the position from where images' uri will be sent to the array of request). If no timeout error, j will start at 1, and comment out "if j>8910"
	2) count_2(count_2 represent the # of rounds, each round process 99 images, add str(count_2) after output_uri can help identify each round, otherwise output file from new rounds could overwrite old round's output)
If timeout happen, check how many rounds have been processed, i.e., count_2 = 91 in the variable list means round 90 has at least started, if count = 5, means 90*99 (past 90 rounds) + 5*99 (in the 91th round, processed 5 batches) = 9405(alreayd processed). Then set j =9406, count_2 = 91. 
	3) Request =[], 

@author: Drs, Xiaohui Liu and Haipeng Tang
"""
# pip install --upgrade google-cloud-storage
from google.cloud import storage
from google.cloud import vision_v1
from google.cloud.vision_v1 import enums
import os,re

#created a new GCP service account, gave it owner, cloud storage admin, and cloud storage object admin roles.
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\liux29\OneDrive - National Institutes of Health\Research\Community_Mine\GSV_Images\nih-nimhd-pcs-acculturation-c6066ac06d0e.json'
bucket_name = "acculturation"
output_folder = "/output3/"

requests = []
# def list_blobs(bucket_name):
#    """Lists all the blobs in the bucket."""
# bucket_name = "your-bucket-name"
storage_client = storage.Client()
# the batch size range (0,100),set processingSize to 99 to maximize the output of img to each json output file
processing_size=99

count=0
#count_2=1 #count_2=91 #count_2 = 1145 count_2 = 2289(None internal error, but stopped, why?)
#count_2 = 2458 #count_2 = 4577 count_2 =5721 #count_2 = 8009 (None Stream removed) 
#count_2 = 10297(maxi tries exceeds with this url, SSL network...) #count_2 = 10802 #count_2 =10803 (windows update reboot at count_2 = 11173)
#count_2 = 11174 # count_2 = 11321
count_2 = 9840 

# j is counter used to track # of processed images 
j=0
   # Note: Client.list_blobs requires at least package version 1.17.0.
try:
    blobs = storage_client.list_blobs(bucket_name, prefix="009/3", delimiter="/")
        
    for blob in blobs:
        j= j+1
        # for process w/ interruption, set j> # of processed imgs; for process without interruption,
        # set j >0, as it starts with 1, will always be greater than 0
       
        # use this j>0 for a new round of process
        #if j>0:
        # uncomment the below j condition to be the next image waiting for process
        #if j>64152:
        #if j>50099:
        #if j >86724:
        #if j>101277:
        if j>68000:
    
            count=count+1        
            print ("Processed: %d images"%j)
            input_image_uri = "gs://" + bucket_name + "/" + blob.name
    
            
            source = {"image_uri": input_image_uri}
            image = {"source": source}
            features = [
                    {"type": enums.Feature.Type.TEXT_DETECTION}
            ]
            
            # Each requests element corresponds to a single image.  To annotate more
            # images, create a request element for each image and add it to
            # the array of requests
            requests = requests + [{"image": image, "features": features}]
    
            # the above code increased count by one everytime an image element is added to the arary of request
            # until count reaches processing_size(99), the output of the 99 images will be writien to a json
            if count==processing_size:
                
                
                # count_2 represent the # of rounds, each round process 99 images,
                # add str(count_2) after output_uri can help identify each round, otherwise output file from new
                # rounds could overwrite old round's output
                
                # the reason to add str(count_2) directly after output_uri is, GCS does not have folders or subdirectories, creating an object that ends in a trailing slash can create the illusion of an empty subdirectory
                # 
                output_uri = "gs://" + bucket_name  + output_folder + str(count_2)   
                gcs_destination = {"uri": output_uri}
                # batch_size = The max number of responses to output in each JSON file
                batch_size = 99
                output_config = {"gcs_destination": gcs_destination,
                               "batch_size": batch_size}
                #output_config = {"gcs_destination": gcs_destination}
            
                client = vision_v1.ImageAnnotatorClient()
                operation = client.async_batch_annotate_images(requests, output_config)
                print("Waiting for operation to complete...")
                # set the timeout =5000 will allow enough time to finish the processes
                response = operation.result(6000)
                   
                 # The output is written to GCS with the provided output_uri as prefix
                gcs_output_uri = response.output_config.gcs_destination.uri
                print("Output written to GCS with prefix: {}".format(gcs_output_uri))           
                count=0
                count_2=count_2+1
                
                # clear the request array, so that it will contain images that are not processed yet in the next for loop
                requests=[]
    
    
    # This part is to process the last dozens of images that are less than 99, thus did not enter the above"if count==processing_size:" branch. So process them here and output separately
    output_uri = "gs://" + bucket_name  + output_folder + str(count_2)   
    gcs_destination = {"uri": output_uri}
    batch_size = 99
    output_config = {"gcs_destination": gcs_destination,
                   "batch_size": batch_size}
    #output_config = {"gcs_destination": gcs_destination}

    client = vision_v1.ImageAnnotatorClient()
    operation = client.async_batch_annotate_images(requests, output_config)
    print("Waiting for operation to complete...")
    response = operation.result(6000)
       
     # The output is written to GCS with the provided output_uri as prefix
    gcs_output_uri = response.output_config.gcs_destination.uri
    print("Output written to GCS with prefix: {}".format(gcs_output_uri))  
    
    
    # print(requests, output_config)

# """Perform async batch image annotation."""

except BaseException as e:
    print (e)
