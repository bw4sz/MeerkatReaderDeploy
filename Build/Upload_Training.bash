#!/bin/bash 
#Upload images for model training on Google CloudML

#upload images for now, later write them directly to google cloud storage.
gsutil -m cp -r C:/Users/Ben/Dropbox/MeerkatReader/Output/* gs://api-project-773889352370-ml/TrainingData/
#make files public readable? Still struggling with credentials
gsutil -m acl set -R -a public-read gs://api-project-773889352370-ml/TrainingData
