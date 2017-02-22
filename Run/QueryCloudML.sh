#!/bin/bash 

##Query CloudML using a Google Compute Engine
#create docker container instance
gcloud compute instances create gci --image-family gci-stable --image-project google-containers \
--scopes 773889352370-compute@developer.gserviceaccount.com="https://www.googleapis.com/auth/cloud-platform" \
--boot-disk-size "40" \
--metadata-from-file startup-script=SubmitJson.sh $MONTH

##Wait for job to finish
gcloud compute instances describe gci
##Parse Results
Rscript -e "rmarkdown::render('Parse.Rmd')" $MONTH

#Post Results


