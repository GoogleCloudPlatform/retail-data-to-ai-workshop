# Module 20: Capstone Setup

## 1. Motivation
The IT leadership of Shoonya, our fictitious retail chain would like to see a functional prototype of an agentic solution for demand, inventory, procurement and logistics, so that they can get business buy-in for building an agent ensemble that can serve as digital counterparts of their human personas. They also want to explore what autonomous agent action looks like and what guardrails can be put in place. This module provides exactly such an immersive learning experience with refrigerators as the focus product category.

<hr>

## 2. Module scope
This module provides the data foundations for the capstone. <br>
1. Create BigQuery datasets
2. Create tables and views
3. Load data
4. Create astored procedures
5. Run Data Insights table and dataset documentation scans.
6. Create a file with Data Insights (dataset, table and column descriptions, and relationships) and persist to a GCS bucket

<hr>

## 3. Duration and prerequisites

1. This module should take about 30 minutes or so, largely due to the time taken for Data Insights and the Gemini limits enforced for Data Insights
2. This capstone can be run indepenently - without any dependency on the previous learning modules

## 4. IAM permissions

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`
UMSA="capstone-umsa"
UMSA_FQN="$UMSA@$PROJECT_ID.iam.gserviceaccount.com"



```


## 4. Clone the repo if you have not already
```
git clone https://github.com/GoogleCloudPlatform/retail-data-to-ai-workshop.git
```

## 5. Create a bucket to load data to

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
PROJECT_NAME=`gcloud projects describe ${PROJECT_ID} | grep name | cut -d':' -f2 | xargs`
LOCATION="us-central1"
DATA_BUCKET="capstone_stage_$PROJECT_NBR"

gcloud storage buckets create gs://$DATA_BUCKET --location=$LOCATION 
```


## 6. Prepare the data for upload to the bucket

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

## 7. Upload to the data bucket

Again, navigate on cloud shell to retail-data-to-ai-workshop

```
gsutil -m cp -r 01-data-assets/* gs://$DATA_BUCKET/
```


## 8. Run the setup notebook in BigQuery to complete all else



<hr>

## 9. About the data 


<hr>

## 10. About the BigQuery objects created in the nitebook






<hr>

## 11. About the Data Insights scan results



## 12. About the BQ metadata persisted to GCS for agentic grounding


<hr>

We have completed the data foundations for the capstone, proceed to the next module.
