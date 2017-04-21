#!/bin/bash 
#Query already run model on cloudml

#Create images to run model
#gcloud compute ssh benweinstein2010@gci 

#Custom docker env
docker pull gcr.io/api-project-773889352370/cloudml:latest
docker run --privileged -it --rm  -p "127.0.0.1:8080:8080" \
  --entrypoint=/bin/bash \
  gcr.io/api-project-773889352370/cloudml:latest
  
#usage reporting very slow
gcloud config set disable_usage_reporting True
 
#Mount directory (still working on it )
export GCSFUSE_REPO=gcsfuse-jessie
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg |  apt-key add -
apt-get update
apt-get install -y gcsfuse

# # cd ~
# #make empty directory for mount
mkdir /mnt/gcs-bucket

# #give it permissions
chmod a+w /mnt/gcs-bucket

#MOUNT 
gcsfuse --implicit-dirs api-project-773889352370-ml /mnt/gcs-bucket

#must be run in the same directory of cloud training
#Model properties
declare MODEL_NAME=MeerkatReader

#process images#clone the git repo
git clone https://github.com/bw4sz/MeerkatReader.git

#need imutils
pip install imutils

#Which images need to be run?
#Check files

#generate list of files 
cd mnt/gcs-bucket/Hummingbirds/
find . -name "*.jpg" -type f > original_files.txt

#extract letters
python MeerkatReader/RunModel/main.py -paths $(cat original_files.txt) -outdir staging/letters/ -limit=5 

gsutil ls gs://api-project-773889352370-ml/staging/letters/*.jpg > jpgs.txt

python MeerkatReader/RunModel/images_to_json.py -o staging/letters/request.json $(cat jpgs.txt)

#submit job
JOB_NAME=predict_Meerkat_$(date +%Y%m%d_%H%M%S)
gcloud beta ml jobs submit prediction ${JOB_NAME} \
    --model=${MODEL_NAME} \
    --data-format=TEXT \
    --input-paths=gs://api-project-773889352370-ml/staging/letters/request.json \
    --output-path=gs://api-project-773889352370-ml/Hummingbirds/prediction/ \
    --region=us-central1
    
#describe job
gcloud beta ml jobs describe ${JOB_NAME}
 
#exit ssh
exit