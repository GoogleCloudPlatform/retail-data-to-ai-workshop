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

## 4. Enable APIs

From cloud shell, run the below:
```
gcloud services enable orgpolicy.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable discoveryengine.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable dataplex.googleapis.com
gcloud services enable datalineage.googleapis.com
gcloud services enable generativelanguage.googleapis.com
gcloud services enable cloudaicompanion.googleapis.com
gcloud services enable bigqueryunified.googleapis.com
gcloud services enable servicenetworking.googleapis.com
```

## 5. IAM permissions for yourself

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.studioAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/dataplex.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/dataplex.dataScanAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/dataplex.catalogEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/aiplatform.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/discoveryengine.admin"


gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/compute.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/compute.networkAdmin"

```

## 6. Update Organization Policies 

**(needed for Argolis environment on GCP)** <br><br>

The organization policies include the superset applicable for all flavors of Dataproc, required in Argolis.<br>
Paste these and run in cloud shell-

### 6.a. Relax require OS Login
```
rm os_login.yaml

cat > os_login.yaml << ENDOFFILE
name: projects/${PROJECT_ID}/policies/compute.requireOsLogin
spec:
  rules:
  - enforce: false
ENDOFFILE

gcloud org-policies set-policy os_login.yaml 

rm os_login.yaml
```

### 6.b. Disable Serial Port Logging

```
rm disableSerialPortLogging.yaml

cat > disableSerialPortLogging.yaml << ENDOFFILE
name: projects/${PROJECT_ID}/policies/compute.disableSerialPortLogging
spec:
  rules:
  - enforce: false
ENDOFFILE

gcloud org-policies set-policy disableSerialPortLogging.yaml 

rm disableSerialPortLogging.yaml
```

### 6.c. Disable Shielded VM requirement

```
shieldedVm.yaml 

cat > shieldedVm.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.requireShieldedVm
spec:
  rules:
  - enforce: false
ENDOFFILE

gcloud org-policies set-policy shieldedVm.yaml 

rm shieldedVm.yaml 
```

### 6.d. Disable VM can IP forward requirement

```
rm vmCanIpForward.yaml

cat > vmCanIpForward.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.vmCanIpForward
spec:
  rules:
  - allowAll: true
ENDOFFILE

gcloud org-policies set-policy vmCanIpForward.yaml

rm vmCanIpForward.yaml
```

### 6.e. Enable VM external access

```
rm vmExternalIpAccess.yaml

cat > vmExternalIpAccess.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.vmExternalIpAccess
spec:
  rules:
  - allowAll: true
ENDOFFILE

gcloud org-policies set-policy vmExternalIpAccess.yaml

rm vmExternalIpAccess.yaml
```

### 6.f. Enable restrict VPC peering

```
rm restrictVpcPeering.yaml

cat > restrictVpcPeering.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.restrictVpcPeering
spec:
  rules:
  - allowAll: true
ENDOFFILE

gcloud org-policies set-policy restrictVpcPeering.yaml

rm restrictVpcPeering.yaml
```

<br><br>

<hr>


## 6. Create a VCP and Subnet

We will need this for BigQuery notebook runtime

```
VPC_NM="capstone-vpc"
SUBNET_NM_CATCHALL="capstone-catchall-snet"
SUBNET_CATCHALL_FQN="projects/$PROJECT_ID/global/networks/$VPC_NM"
SUBNET_CIDR_CATCHALL="10.0.0.0/16"
PEERING_NM="capstone-vpc-peering-to-service-networking"
PEERING_RANGE_NAME="capstone-vpc-peering-reserved-range"

# Create VPC
gcloud compute networks create $VPC_NM \
--project=$PROJECT_ID \
--subnet-mode=custom \
--mtu=1460 \
--bgp-routing-mode=regional 

# Create subnet
gcloud compute networks subnets create $SUBNET_NM_CATCHALL \
 --network $VPC_NM \
 --range $SUBNET_CIDR_CATCHALL  \
 --region $LOCATION \
 --enable-private-ip-google-access \
 --project $PROJECT_ID 

# Pypi access
gcloud compute firewall-rules create allow-pypi-access \
    --network=$VPC_NM \
    --action=ALLOW \
    --direction=EGRESS \
    --target-tags=notebook-allow-pypi \
    --destination-ranges=0.0.0.0/0 \
    --rules=tcp:80,tcp:443 \
    --priority=1000

# Public internet egress
gcloud compute firewall-rules create allow-all-egress-for-all \
    --network=$VPC_NM \
    --direction=EGRESS \
    --priority=1000 \
    --action=ALLOW \
    --rules=all \
    --destination-ranges=0.0.0.0/0

# Create peeering range
gcloud compute addresses create $PEERING_RANGE_NAME \
  --global \
  --prefix-length=16 \
  --description="Peering range for Google service" \
  --network=$VPC_NM \
  --purpose=VPC_PEERING 

# Create the VPC peering
gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --network=$VPC_NM \
  --ranges=$PEERING_RANGE_NAME \
  --project=$PROJECT_ID 
```


## 7. Clone the repo if you have not already
```
git clone https://github.com/GoogleCloudPlatform/retail-data-to-ai-workshop.git
```

## 8. Create a bucket to load data to

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
LOCATION="us-central1"
DATA_BUCKET="capstone_stage_$PROJECT_NBR"

gcloud storage buckets create gs://$DATA_BUCKET --location=$LOCATION 
```


## 9. Prepare the data for upload to the bucket

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
rm -rf 
```

## 10. Upload to the data bucket

Again, navigate on cloud shell to retail-data-to-ai-workshop

```
gsutil -m cp -r 01-data-assets/capstone_data gs://$DATA_BUCKET/
```

## 8. Quick review of the scoped assets for this capstone

```
.
├── 01-data-assets
│   └── capstone_data
│       ├── fridge_tabular_data
│       ├── fridge_userguides
│       └── metadata
│           └── captone_database_metadata_grounding.md
├── 02-code-assets
│   ├── capstone-retail-solution <-- Custom agent code
│   └── Module_20_Capstone_Setup.ipynb <-- Setup notebook
├── 03-lab-manuals
│   ├── Module_20_Capstone_Setup.md
│   ├── Module_21_ADK_Primer_Data_Analyst_Agent.md
│   ├── Module_22_Demand_Planner_Agent.md
│   ├── Module_23_Inventory_Manager_Agent.md
│   ├── Module_24_Procurement_Manager_Agent.md
│   ├── Module_25_Logistics_Manager_Agent.md
│   └── ..
...
```


## 11. Run the setup notebook in BigQuery to complete all else

Upload the `Module_20_Capstone_Setup.md` notebook to BQ and run it.<br>
Expect this to take 30 minutes to complete.


<hr>

## 9. About the data 


<hr>

## 10. About the BigQuery objects created in the nitebook






<hr>

## 11. About the Data Insights scan results



## 12. About the BQ metadata persisted to GCS for agentic grounding


<hr>

We have completed the data foundations for the capstone, proceed to the next module.
