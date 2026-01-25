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

Our goal is to deploy the agent to agent engine to run as custom service account. Per the documentation this is supported. If it does not work, we will grant the Agent Engine default Service Agent the permissions needed for access. This is however not a best practice. 

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

### 4.5. Grant the Agent Engine Default Service Agent permissions [as the IAM permissions] to the Data Analyst UMSA did not work

The custom / user managed service account did not consistently work in terms of data access. So, lets grant the Agent Engine Default Service Agent permissions for data access. For product workloads, follow principle of least privilege.

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
AE_GMSA_FQN=service-$PROJECT_NBR@gcp-sa-aiplatform-re.iam.gserviceaccount.com


gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/mcp.toolUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/aiplatform.reasoningEngineServiceAgent"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/iam.oauthClientViewer"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/iam.serviceAccountViewer"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/oauthconfig.editor"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/aiplatform.user"

# Select 3 - None in the prompt
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/storage.objectCreator"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AE_GMSA_FQN" \
  --role="roles/bigquery.jobUser" 

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AE_GMSA_FQN" \
--role="roles/bigquery.dataViewer" \
--condition="expression=resource.name.startsWith(\"$BQ_DATASET_IN_SCOPE_RESOURCE_URI\"),title=AccessToSpecificDataset"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AE_GMSA_FQN" \
--role="roles/bigquery.user" 
```


<hr>

## 5. Deploy & test the Data Analyst Agent to Agent Engine

### 5.1. Create the agent_engine_config.json

# INSERT SCREENSHOT HERE


### 5.2. Grant the deployer (yourself), incremental IAM permissions

```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/discoveryengine.admin"

```

### 5.3. Deploy the agent to Agent Engine

Run this from within the top level data_analyst_agent folder, from CLI. This will automatically read in any configs in agent_engine_config.json
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

### 5.4. Retrieve the Data Analyst Agent ID from the Agent Engine deployment

```
AGENT_ENGINE_LOCATION="us-central1"
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
DATA_ANALYST_AGENT_ID=`curl -X GET   -H "Authorization: Bearer $(gcloud auth print-access-token)"   "https://$AGENT_ENGINE_LOCATION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines" | grep -2 "Data Analyst Agent" | grep name | grep reasoningEngines | cut -d '/' -f2`

```


### 5.5. Test the  Data Analyst Agent on Agent Engine in the "Playground"


# INSERT SCREENSHOT HERE

<hr>



## 6. Create the Agentspace App (Shoonya Retail Agentverse) on Gemini Enterprise

### 6.1. Create the application
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
  "name": "projects/606asdasd5020/locations/global/collections/default_collection/operations/create-engine-192268asdasdas42799",
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.cloud.discoveryengine.v1.Engine",
    "name": "projects/60asdasd0/locations/global/collections/default_collection/engines/shoonya-retail-agentverse",
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

### 6.2. Check agents registered with the app you just created

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
AGENTSPACE_APP_ID="shoonya-retail-agentverse"
AGENTSPACE_LOCATION="global"

curl -X GET \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
"https://$AGENTSPACE_LOCATION-discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_ID/locations/$AGENTSPACE_LOCATION/collections/default_collection/engines/$AGENTSPACE_APP_ID/assistants/default_assistant/agents"
```

You should see the "Deep Research" agent automatically registered:
```
{
  "agents": [
    {
      "name": "projects/sdads/locations/global/collections/default_collection/engines/shoonya-retail-agentverse/assistants/default_assistant/agents/deep_research",
      "displayName": "Deep Research",
      "description": "This agent is a specialized agent that gathers, analyzes, and understands information from internal and external sources. It generates a plan, an in-depth report, and a summary.",
      "createTime": "2026-01-24T22:59:28.608545129Z",
      "updateTime": "2026-01-24T22:59:28.754573Z",
      "managedAgentDefinition": {},
      "state": "ENABLED",
      "sharingConfig": {
        "scope": "ALL_USERS"
      }
    }
  ]
}
```

<hr>



## 7. Register the Data Analyst Agent with Agentspace on Gemini Enterprise


### 7.1. Register the agent on Agent Engine with Gemini Enterprise for the Agent UI experience

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
  "name": "projects/606asdasdad20/locations/global/collections/default_collection/engines/shoonya-retail-agentverse/assistants/default_assistant/agents/3653339957651564590",
  "displayName": "Data Analyst Agent",
  "description": "An agent who can analyze data on your behalf with just natural language questions as input",
  "icon": {
    "uri": "ICON_URI"
  },
  "createTime": "2026-01-24T23:06:00.197769472Z",
  "adkAgentDefinition": {
    "provisionedReasoningEngine": {
      "reasoningEngine": "projects/data-insights-quickstart/locations/us-central1/reasoningEngines/606804615020"
    }
  },
  "state": "ENABLED"
}
```

Make note of the IDs here-
1. Agent ID on Gemini Enterprise is `3653339957651564590` in
`projects/606asdasdad20/locations/global/collections/default_collection/engines/shoonya-retail-agentverse/assistants/default_assistant/agents/3653339957651564590`
2. Agent name on Gemini Enterprise is `Data Analyst Agent`
3. Agent Engine (reasoning engine) ID is `606804615020` from `projects/data-insights-quickstart/locations/us-central1/reasoningEngines/60680461502`


### 7.2. Check agents registered with the app we created on Gemini enterprise

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
AGENTSPACE_APP_ID="shoonya-retail-agentverse"
AGENTSPACE_LOCATION="global"

curl -X GET \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
"https://$AGENTSPACE_LOCATION-discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_ID/locations/$AGENTSPACE_LOCATION/collections/default_collection/engines/$AGENTSPACE_APP_ID/assistants/default_assistant/agents"
```
Here is what the author got back:
```
THIS IS INFORMATIONAL

{
  "agents": [
    {
      "name": "projects/606sdfsdfg20/locations/global/collections/default_collection/engines/shoonya-retail-agentverse/assistants/default_assistant/agents/3653339957651564590",
      "displayName": "Data Analyst Agent",
      ..
     ...
      "adkAgentDefinition": {
        "provisionedReasoningEngine": {
          "reasoningEngine": "projects/data-insights-quickstart/locations/us-central1/reasoningEngines/606804615020"
        }
      },
      "state": "ENABLED"
    },
    {
      "name": "projects/60sdfsdfg020/locations/global/collections/default_collection/engines/shoonya-retail-agentverse/assistants/default_assistant/agents/deep_research",
      "displayName": "Deep Research",
     ...
      }
    }
  ]
}
```

Ensure the reasoning ending ID is the same as the value returned from running the below-
```
echo $DATA_ANALYST_AGENT_ID
```



### 7.3. In case of discrepancies - update the Gemini Enterprise agent with the right Agent Engine agent ID ID 

Here is how you update the Agent Engine deployed Agent ID.<br>
SKIP THIS IF YOU HAVE THE RIGHT ID <br>
Documentation link: https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent#update_an_adk_agent



```


<hr>






