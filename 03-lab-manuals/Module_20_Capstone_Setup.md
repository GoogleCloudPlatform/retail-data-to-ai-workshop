# Module 20: Capstone Setup


<hr>

## 3. Upload the data to GCS

### 3.1. Clone the repo if you have not already
```
git clone https://github.com/GoogleCloudPlatform/retail-data-to-ai-workshop.git
```

### 3.2. Create a bucket to load data to

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
PROJECT_NAME=`gcloud projects describe ${PROJECT_ID} | grep name | cut -d':' -f2 | xargs`
LOCATION="us-central1"
DATA_BUCKET="capstone_stage_$PROJECT_NBR"

gcloud storage buckets create gs://$DATA_BUCKET --location=$LOCATION 
```


### 3.3. Prepare the data for upload to the bucket

Switch to the `retail-data-to-ai-workshop` directory and run the below.

```
cd 01-data-assets/
mv capstone_data_1 capstone_data
mv capstone_data_2/* capstone_data/
mv capstone_data_3/fridge_userguides/* capstone_data/fridge_userguides/
mv capstone_data_4/fridge_userguides/* capstone_data/fridge_userguides/
rm -rf capstone_data_1
rm -rf capstone_data_2
rm -rf capstone_data_3
rm -rf capstone_data_4
cd capstone_data/fridge_userguides
tar -xvzf bottom-freezer.tgz 
tar -xvzf compact.tgz 
tar -xvzf french-door.tgz 
tar -xvzf one-door.tgz 
tar -xvzf side-by-side.tgz
tar -xvzf top-freezer.tgz
tar -xvzf wine-cellar.tgz
rm -rf *.tgz
```

### 3.4. Upload to the data bucket

Again, navigate on cloud shell to retail-data-to-ai-workshop
```
gsutil -m cp -r 01-data-assets

```


### 3.4. Run the setup notebook in BigQuery



<hr>

## 4. Overview of objects in BigQuery



<hr>

## 5. Overview of Data Insights




<hr>

We have completed the data foundations for the capstone, proceed to the next module.
