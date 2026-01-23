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

```

### 1.6. Enable APIs

Only incremental APIs are listed below-
```
gcloud services enable telemetry.googleapis.com
gcloud services enable logging.googleapis.com
```


### 1.7. Set up VS code or use any IDE on your machine


### 1.8. Clone this repo if you have not already done so


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

Modify the env file to reflect your GCP project ID, project number and location by updating the following with your details and saving the file-

```
GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
GOOGLE_CLOUD_LOCATION="YOUR_GCP_LOCATION"
GOOGLE_CLOUD_PROJECT_NUMBER="YOUR_PROJECT_NUMBER"
```

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
DATA_ANALYST_UMSA="data-analyst-agent"
DATA_ANALYST_UMSA_FQN="$DATA_ANALYST_UMSA@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $DATA_ANALYST_UMSA \
  --description="User Managed Service Account" \
  --display-name="Data Analyst Agent Service Account"
```

### 4.3. Grant the UMSA, requisite IAM permissions 

```
BQ_DATASET_IN_SCOPE_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_ds"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/mcp.toolUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/aiplatform.reasoningEngineServiceAgent"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/iam.oauthClientViewer"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/iam.serviceAccountViewer"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/oauthconfig.editor"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/aiplatform.user"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/storage.objectCreator"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
  --role="roles/bigquery.jobUser" 

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
--role="roles/bigquery.dataViewer" \
--condition="expression=resource.name.startsWith(\"$BQ_DATASET_IN_SCOPE_RESOURCE_URI\"),title=AccessToSpecificDataset"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DATA_ANALYST_UMSA_FQN" \
--role="roles/bigquery.user" 

```

### 4.4. Grant yourself permissions to impersonate the Data Analyst UMSA

```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/iam.serviceAccountTokenCreator"

gcloud iam service-accounts add-iam-policy-binding \
    ${DATA_ANALYST_UMSA_FQN} \
    --member="user:${YOUR_UPN_FQN}" \
    --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts add-iam-policy-binding \
    ${DATA_ANALYST_UMSA_FQN} \
    --member="user:${YOUR_UPN_FQN}" \
    --role="roles/iam.serviceAccountTokenCreator"
```


<hr>

## 5. Deploy the Data Analyst Agent to Agent Engine

### 5.1. Create the agent_engine_config.json



### 5.1. Deploy the agent to Agent Engine

Run this from within the top level data_analyst_agent folder, from CLI
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
LOCATION="us-central1"

adk deploy agent_engine \
--project=$PROJECT_ID   \
--region=$LOCATION   \
--display_name="Data Analyst Agent"   \
--description="An agent that can answer natural language questions about data in the BQ dataset rscw_fridge_ds" \
--staging_bucket=gs://agent-deployment-bucket-$PROJECT_NBR   \
--env_file="./data_analyst_agent/.env"   \
--trace_to_cloud   \
./data_analyst_agent
```


### 5.2. Test the  Data Analyst Agent on Agent Engine in the "Playground"



<hr>


## 6. Register the Data Analyst Agent with Agentspace on Gemini Enterprise

### 6.1. Retrieve the Data Analyst Agent ID from the Agent Engine deployment

```
LOCATION=us-central1
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
DATA_ANALYST_AGENT_ID=`curl -X GET   -H "Authorization: Bearer $(gcloud auth print-access-token)"   "https://us-central1-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/reasoningEngines" | grep -2 "Data Analyst Agent" | grep name | grep reasoningEngines | cut -d '/' -f2`
```

### 6.2. Grant the deployer (yourself), incremental IAM permissions

```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/discoveryengine.admin"

```
<hr>






