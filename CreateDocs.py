'''
Create documents for training a tensorflow model on google cloud machine learning engine.
This script is built for a two class training dataset, images with desired objects (positives) and images with ignored objects (negatives)
'''

import os
from google.cloud import storage
from oauth2client.client import GoogleCredentials
import random
import csv
import tempfile

# Serice account credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Ben/Dropbox/Google/MeerkatReader-9fbf10d1e30c.json"

class Organizer:
    def __init__(self,positives,negatives):

        credentials = GoogleCredentials.get_application_default()
        """Downloads a blob from the bucket."""
        storage_client = storage.Client()
        
        #parse names
        bucket_name=positives.split("/")[2]
    
        #open bucket
        self.bucket = storage_client.get_bucket(bucket_name)
        
        #positives
        positives_folder_name=positives.split("/")[3:]
        pos_ls=self.bucket.list_blobs(fields="items",prefix="/".join(positives_folder_name))        
        self.positives_files=[]
        for f in pos_ls:
            self.positives_files.append("gs://" + f.bucket.name + "/" + f.name)
            
        #negatives
        negatives_folder_name=negatives.split("/")[3:]
        pos_ls=self.bucket.list_blobs(fields="items",prefix="/".join(negatives_folder_name))        
        self.negatives_files=[]
        for f in pos_ls:
            self.negatives_files.append("gs://" + f.bucket.name + "/" + f.name)
    
    def divide_data(self,training_prop=0.8):
        
        #Shuffle positive datasets and divide
        positives_random=self.positives_files
        random.shuffle(positives_random)
        
        self.positives_training=positives_random[int(len(positives_random)*training_prop):]
        self.positives_testing=positives_random[:int(len(positives_random)*training_prop)]

        #Shuffle negatives datasets and divide
        negatives_random=self.negatives_files
        random.shuffle(negatives_random)
        
        self.negatives_training=negatives_random[int(len(negatives_random)*training_prop):]
        self.negatives_testing=negatives_random[:int(len(negatives_random)*training_prop)]
        
    
    def write_data(self):
        
        #Write to temp then send to google cloud
        handle, fn = tempfile.mkstemp(suffix='.csv')
        
        with open(handle,"w") as f:
            writer=csv.writer(f)
            for eachrow in  self.positives_training:
                writer.writerow([eachrow,"positive"])
            for eachrow in  self.negatives_training:
                writer.writerow([eachrow,"negative"])
        
        #write to google cloud
        blob=self.bucket.blob("Hummingbirds/trainingdata.csv")
        blob.upload_from_filename(fn)
        
        
        
if __name__ == "__main__":
    p=Organizer(positives="gs://api-project-773889352370-ml/Hummingbirds/Negatives", negatives="gs://api-project-773889352370-ml/Hummingbirds/to_upload")
    p.divide_data(training_prop=0.8)
    p.write_data()