# -*- coding: utf-8 -*-
"""

Created on Sun May 16 10:31:33 2020
set up:
    1) set os.environ to correct path to the json key file
    2) set the folder of input file: blobs = storage_client.list_blobs(bucket_name, prefix="001/3", delimiter="/")
    3) set the output folder path if needed
If timeout error happens, refer to another script "batch_text_detect_w_Timeout_0516.py", where a few places needs to be modified:
	1) j (use this counter to mark the position of processed images. If one execution ended at j position, then next time start at j+1 position. This will determine the position from where images' uri will be sent to the array of request)  
	2) count_2(count_2 represent the # of rounds, each round process 99 images, add str(count_2) after output_uri can help identify each round, otherwise output file from new rounds could overwrite old round's output)
If timeout happen, check how many rounds have been processed, i.e., count_2 = 91 in the variable list means round 90 has at least started, if count = 5, means 90*99 (past 90 rounds) + 5*99 (in the 91th round, processed 5 batches) = 9405(alreayd processed). Then set j =9406, count_2 = 91. 
	3) Request =[], use console 


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
output_folder = "/output/"

requests = []
# def list_blobs(bucket_name):
#    """Lists all the blobs in the bucket."""
# bucket_name = "your-bucket-name"
storage_client = storage.Client()

j=0
   # Note: Client.list_blobs requires at least package version 1.17.0.
try:
    blobs = storage_client.list_blobs(bucket_name, prefix="test/3", delimiter="/")
#    for i in range(1, 1000, 500):
        
    for blob in blobs:
                
        print(blob)
        j= j+1
        print ("Processed: %d images"%j)
        input_image_uri = "gs://" + bucket_name + "/" + blob.name
        output_uri = "gs://" + bucket_name + output_folder
        
        source = {"image_uri": input_image_uri}
        image = {"source": source}
        features = [
                {"type": enums.Feature.Type.TEXT_DETECTION}
        ]
        
        # Each requests element corresponds to a single image.  To annotate more
        # images, create a request element for each image and add it to
        # the array of requests
        requests = requests + [{"image": image, "features": features}]
        gcs_destination = {"uri": output_uri}
    
    # The max number of responses to output in each JSON file
    batch_size = 99
    output_config = {"gcs_destination": gcs_destination,
                   "batch_size": batch_size}
    #output_config = {"gcs_destination": gcs_destination}

    client = vision_v1.ImageAnnotatorClient()
    operation = client.async_batch_annotate_images(requests, output_config)
    print("Waiting for operation to complete...")
    response = operation.result(5000)
       
     # The output is written to GCS with the provided output_uri as prefix
    gcs_output_uri = response.output_config.gcs_destination.uri
    print("Output written to GCS with prefix: {}".format(gcs_output_uri))           


    # print(requests, output_config)

# """Perform async batch image annotation."""

except BaseException as e:
    print (e)
