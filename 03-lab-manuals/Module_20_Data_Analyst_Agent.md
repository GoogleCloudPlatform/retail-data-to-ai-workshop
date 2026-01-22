# Module 20: [ADK Primer] Create a Data Analyst Agent

## 1. Setup

### 1.1. Authenticate to Google Cloud from CLI

### 1.2. Ingest the refrigerator dataset from CLI


### 1.3. Run the notebook that executes the Data Insights documentation scans & persists metadata to GCS


### 1.4. Create a user managed service account for deployments

From your terminal, run the below:
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
LOCATION="us-central1"
DEPLOYMENT_UMSA="rscw-devops-umsa"
DEPLOYMENT_UMSA_FQN="rscw-devops-umsa@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $DEPLOYMENT_UMSA \
  --description="User Managed Service Account" \
  --display-name="RSCW DevOps UMSA"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEPLOYMENT_UMSA_FQN" \
  --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEPLOYMENT_UMSA_FQN" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEPLOYMENT_UMSA_FQN" \
  --role="roles/storage.objectCreator"
```

### 1.6. Grant yourself permissions to impersonate the deployment UMSA

```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/iam.serviceAccountTokenCreator"

gcloud iam service-accounts add-iam-policy-binding \
    ${DEPLOYMENT_UMSA_FQN} \
    --member="user:${YOUR_UPN_FQN}" \
    --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts add-iam-policy-binding \
    ${DEPLOYMENT_UMSA_FQN} \
    --member="user:${YOUR_UPN_FQN}" \
    --role="roles/iam.serviceAccountTokenCreator"
```


### 1.5. Create a bucket for agent deployment

From your terminal, run the below:
```
AGENT_DEPLOYMENT_BUCKET="agent-deployment-bucket-$PROJECT_NBR"
gcloud storage buckets create "gs://$AGENT_DEPLOYMENT_BUCKET" --location=$LOCATION  --impersonate-service-account=$DEPLOYMENT_UMSA_FQN

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEPLOYMENT_UMSA_FQN" \
  --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEPLOYMENT_UMSA_FQN" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEPLOYMENT_UMSA_FQN" \
  --role="roles/storage.objectCreator"



```


### 1.5. Set up VS code or use any IDE on your machine


### 1.6. Clone this repo if you have not already done so


<hr>


## 2. Review the Data Analyst Agent code 

### 2.1. Review the code layout in VS code


### 2.2. Study these specific code/config files

<hr>

## 3. Run the agent locally

### 3.1. Set up a Python virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

### 3.2. Install the Python dependencies

Navigate to the Data_Analytics_Agent folder that has the requirements.txt and run the install from VS code terminal-
`pip install -r requirements.txt`

### 3.2. Update the env file 

Modify the env file to reflect your GCP project ID


### 3.3. Lauch a terminal in VS Code/your IDE and authenticate

### 3.4. Run adk web


### 3.4. Try out a few prompts

<hr>

## 4. Preparing for deployment to Agent Engine

### 4.1. Requisite API enabling

```
gcloud services enable discoveryengine.googleapis.com
```

### 4.2. Create a user managed service account (UMSA) for the Data Analyst Agent

```
DATA_ANALYST_UMSA="data-analyst-umsa"
DATA_ANALYST_UMSA_FQN="$DATA_ANALYST_UMSA@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $DATA_ANALYST_UMSA \
  --description="User Managed Service Account" \
  --display-name="Data Analyst Service Account"
```

### 4.3. Grant the UMSA, requisite IAM permissions 

```


```

### 4.4. Lock down the BigQuery datasets the Data Analyst Agent UMSA has access to

<hr>

## 5. Deploy the Data Analyst Agent to Agent Engine

### 5.1. Deploy the agent to Agent Engine

### 5.2. Capture the identifier of the agent deployed

### 5.3. Test the remote Data Analyst Agent on Agent Engine programmatically from your IDE

<hr>


## 6. Register the Data Analyst Agent with Agentspace on Gemini Enterprise



<hr>






