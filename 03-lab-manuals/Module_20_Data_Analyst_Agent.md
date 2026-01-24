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

## 5. Deploy & test the Data Analyst Agent to Agent Engine

### 5.1. Create the agent_engine_config.json

# INSERT SCREENSHOT HERE



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

# INSERT SCREENSHOT HERE

### 5.2. Retrieve the Data Analyst Agent ID from the Agent Engine deployment

```
AGENT_ENGINE_LOCATION="us-central1"
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
DATA_ANALYST_AGENT_ID=`curl -X GET   -H "Authorization: Bearer $(gcloud auth print-access-token)"   "https://$AGENT_ENGINE_LOCATION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines" | grep -2 "Data Analyst Agent" | grep name | grep reasoningEngines | cut -d '/' -f2`
```

### 5.3. Grant the deployer (yourself), incremental IAM permissions

```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/discoveryengine.admin"

```

### 5.4. Test the  Data Analyst Agent on Agent Engine in the "Playground"


# INSERT SCREENSHOT HERE

<hr>


## 6. Create an oauth client from the Cloud Console for use in Gemini Enterprise

Docs: https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent <br>

Follow the steps as detailed in the screenshot below to create your oauth client.


# INSERT SCREENSHOT HERE



<hr>

## 7. Create the Agentspace App (Shoonya Retail Agentverse) on Gemini Enterprise

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
AGENTSPACE_APP_ID="shoonya-retail-agentverse"
AGENTSPACE_LOCATION="global"


curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-H "X-Goog-User-Project: $PROJECT_ID" \
"https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENTSPACE_LOCATION/collections/default_collection/engines?engineId=$AGENTSPACE_APP_ID" \
-d '{
  "displayName": "Shoonya Retail Agentverse",
  "dataStoreIds": [],
  "solutionType": "SOLUTION_TYPE_SEARCH",
  "industryVertical": "GENERIC",
  "appType": "APP_TYPE_INTRANET"
}'

```

Author's output:
```
THIS IS JUST FOR AWARENESS
{
  "name": "projects/606804615020/locations/global/collections/default_collection/operations/create-engine-8371403560808029638",
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.cloud.discoveryengine.v1.Engine",
    "name": "projects/606804615020/locations/global/collections/default_collection/engines/shoonya-retail-agentverse",
    "displayName": "Shoonya Retail Agentverse",
    "solutionType": "SOLUTION_TYPE_SEARCH",
    "searchEngineConfig": {
      "searchTier": "SEARCH_TIER_STANDARD"
    },
    "industryVertical": "GENERIC",
    "knowledgeGraphConfig": {
      "enablePrivateKnowledgeGraph": true,
      "featureConfig": {}
    },
    "appType": "APP_TYPE_INTRANET"
  }
}
```



## 8. Register an authorization resource with Gemini Enterprise

### 8.1. Variables

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
AGENTSPACE_APP_ID="shoonya-retail-agentverse"
AGENTSPACE_LOCATION="global"
```

### 8.2. Generate the curl command
  
Go to this URL and paste in your oauth details, grab the command and run it on the terminal...


# INSERT SCREENSHOT HERE


### 8.3. Run the curl command on your terminal


# INSERT SCREENSHOT HERE

```
THIS IS AUTHOR'S SAMPLE - THIS WONT WORK FOR YOU
curl -X POST \
   -H "Authorization: Bearer $(gcloud auth print-access-token)" \
   -H "Content-Type: application/json" \
   -H "X-Goog-User-Project: data-insights-quickstart" \
   "https://global-discoveryengine.googleapis.com/v1alpha/projects/data-insights-quickstart/locations/global/authorizations?authorizationId=shoonya_oauth_client" \
   -d '{
      "name": "projects/data-insights-quickstart/locations/global/authorizations/shoonya_oauth_client",
      "serverSideOauth2": {
         "clientId": "6068BLAHgrd.apps.googleusercontent.com",
         "clientSecret": "GBLAHrxsaqgG",
         "authorizationUri": "https://accounts.google.com/o/oauth2/auth",
         "tokenUri": "https://oauth2.googleapis.com/token"
      }
   }'
```

<hr>

## 9. Register the Data Analyst Agent with Agentspace on Gemini Enterprise


### 9.1. Register the agent

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
AGENTSPACE_APP_ID="shoonya-retail-agentverse"
AGENTSPACE_LOCATION="global"
AGENT_ENGINE_LOCATION="us-central1"
DATA_ANALYST_AGENT_ID=`curl -X GET   -H "Authorization: Bearer $(gcloud auth print-access-token)"   "https://$AGENT_ENGINE_LOCATION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines" | grep -2 "Data Analyst Agent" | grep name | grep reasoningEngines | cut -d '/' -f2`

PAYLOAD="{
     \"displayName\": \"Data Analyst Agent\",
     \"description\": \"An agent who can analyze data on your behalf with just natural language questions as input\",
     \"icon\": {
        \"uri\": \"ICON_URI\"
  },
  \"adk_agent_definition\": {
     \"provisioned_reasoning_engine\": {
        \"reasoning_engine\":
        \"projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines/$DATA_ANALYST_AGENT_ID\"
     }
  },
\"authorization_config\": {
\"tool_authorizations\": [
\"projects/$PROJECT_NBR/locations/global/authorizations/shoonya_oauth_client\"
]
}
}"

PAYLOAD="{
     \"displayName\": \"Data Analyst Agent\",
     \"description\": \"An agent who can analyze data on your behalf with just natural language questions as input\",
     \"icon\": {
        \"uri\": \"ICON_URI\"
  },
  \"adk_agent_definition\": {
     \"provisioned_reasoning_engine\": {
        \"reasoning_engine\":
        \"projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines/$DATA_ANALYST_AGENT_ID\"
     }
  }
}"

curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: $PROJECT_ID" \
  "https://$AGENTSPACE_LOCATION-discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_ID/locations/$AGENTSPACE_LOCATION/collections/default_collection/engines/$AGENTSPACE_APP_ID/assistants/default_assistant/agents" \
  -d "$PAYLOAD"
```


Author's output:
```
{
  "name": "projects/606804615020/locations/global/collections/default_collection/engines/shoonya-retail-agentverse/assistants/default_assistant/agents/8401779179432481891",
  "displayName": "Data Analyst Agent",
  "description": "An agent who can analyze data on your behalf with just natural language questions as input",
  "icon": {
    "uri": "ICON_URI"
  },
  "createTime": "2026-01-24T21:57:11.752273556Z",
  "adkAgentDefinition": {
    "provisionedReasoningEngine": {
      "reasoningEngine": "projects/data-insights-quickstart/locations/us-central1/reasoningEngines/606804615020"
    }
  },
  "state": "ENABLED"
}
```



<hr>






