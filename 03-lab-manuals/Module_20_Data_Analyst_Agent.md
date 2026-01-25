# Module 20: [ADK Primer] Create a Data Analyst Agent with the BigQuery Managed MCP Server

In this tutorial we will create an agent for data QnA with ADK, and deploy it to Agent Engine, then register it with Gemini Enterprise. As part of the agent developer continuum, we will test the agent with `adk web` locally, deploy and test on `agent engine` playground, and finally via the `gemini enterprise` UI. 

Note:
1. The managed MCP server for BigQuery is a new feature at the time of authoring and can be brittle/can fail at times
2. The system instructions are bare and the goal is to see how far we can get without detailed instructions
3. The integration is brittle, exercise caution to proceed with the instructions exactly as detailed
4. Gemini throttling can affect the performance - be mindful of issues / outages
5. Enhance the instructions to improve the accuracy as a challenge
6. Attempt configuring with the agent identity construct, or end user credentials for further challenge
7. Finally, skip the MCP server and author custpm tool for BQ access for the greatest control and flexibility
8. Layer in the MCP toolbox for databases for the benefits it offers
   

## 1. Setup

### 1.1. Authenticate to Google Cloud from CLI & generate Application Default Credentials

Run each of these in cloud shell / terminal:
```
gcloud init
```

```
gcloud auth application-default login
```

### 1.2. Ingest the refrigerator dataset from CLI

# INSERT INSTRUCTIONS

### 1.3. Run the notebook that executes the Data Insights documentation scans & persists metadata to GCS

# INSERT INSTRUCTIONS

### 1.4. Create a user managed service account for provisioning services

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

### 1.6. Grant yourself permissions to impersonate the provisioning UMSA

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


### 1.7. Create a bucket for agent deployment

From your terminal, run the below:
```
AGENT_DEPLOYMENT_BUCKET="agent-deployment-bucket-$PROJECT_NBR"
gcloud storage buckets create "gs://$AGENT_DEPLOYMENT_BUCKET" --location=$LOCATION  --impersonate-service-account=$DEPLOYMENT_UMSA_FQN

```

### 1.8. Enable APIs

Only incremental APIs are listed below-
```
gcloud services enable telemetry.googleapis.com
gcloud services enable logging.googleapis.com
```


### 1.9. Set up VS code or use any IDE on your machine

Install VS code from https://code.visualstudio.com/download and configure it for Python and Google Cloud.



### 1.8. Clone the repo

You should have cloned the repo at the onset of this workshop, pull the latest code.

<hr>


## 2. Review the Data Analyst Agent code 

### 2.1. Review the code layout in VS code/your IDE

Navigate to the `rscw-agent-solution` in vs code/your IDE <br>

Here is what the layout should look like:
```
.
└── data_analyst_agent
    ├── data_analyst_agent
    │   ├── __init__.py
    │   ├── agent.py
    │   ├── constants.py
    │   └── tools.py
    ├── requirements.txt
    └── sample_prompts.md
```

### 2.2. Study these specific code/config files

Open each of the files and review the code.

<hr>

## 3. Run the agent locally

### 3.1. Set up a Python virtual environment in VS code / your IDE's terminal

Run the below in your terminal-
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

![README](../04-images/M20-10.png)   
<br><br>


### 3.3. Launch a terminal in VS Code/your IDE and authenticate

Follow instructions in section 1.

### 3.4. Run adk web

In the terminal navigate to the top level data_analyst_agent directory and run the command below.<br>
(e.g. from author - `/Users/akhanolkar/github/rscw-agent-solution/data_analyst_agent`)

```
adk web
```


### 3.4. Try out a few prompts

The code base includes sample prompts, you can grab a few and try out like below.

![README](../04-images/M20-11.png)   
<br><br>

![README](../04-images/M20-12.png)   
<br><br>

We now know our agent is able to access data from BigQuery via the managed MCP server for BigQuery and we did no need to create any custom tools.

<hr>

## 4. Preparing for deployment to Agent Engine

Our goal is to deploy the agent to agent engine to run as custom service account. Per the documentation this is supported. If it does not work, we will grant the Agent Engine default Service Agent the permissions needed for access. This is however not a best practice. 

### 4.1. Requisite API enabling

Run the below in the terminal.
```
gcloud services enable discoveryengine.googleapis.com
```

This should ideally create the P4SA  - the agent engine default service agent account that has the following construct- `service-YOUR_PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com`



### 4.2. Create a user managed service account (UMSA) for the Data Analyst Agent

We will first try to create a custom service account which we will refer to as Data Analyst Agent UMSA from this point on and try to provision the Agent on Agent Engine with this service account. Run the below in the terminal.

```
DATA_ANALYST_UMSA="data-analyst-agent"
DATA_ANALYST_UMSA_FQN="$DATA_ANALYST_UMSA@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $DATA_ANALYST_UMSA \
  --description="User Managed Service Account" \
  --display-name="Data Analyst Agent Service Account"
```

### 4.3. Grant the UMSA, requisite IAM permissions 

We will need to grant the requisite UMSA IAM permissions. Run the below in the terminal.
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

Run the below in the terminal.
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

### 4.5. Grant the Agent Engine Default Service Agent permissions [as the IAM permissionsto the Data Analyst UMSA did not work from the author's trials]

The custom / user managed service account did not consistently work in terms of data access. So, lets grant the Agent Engine Default Service Agent permissions for data access. For product workloads, follow principle of least privilege. Run the below in the terminal.

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

## 5. Deploy & test the Data Analyst Agent on Agent Engine


### 5.1. Grant the deployer (yourself), incremental IAM permissions

```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/discoveryengine.admin"

```

### 5.2. Deploy the agent to Agent Engine

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

![README](../04-images/M20-13.png)   
<br><br>




### 5.3. Retrieve the Data Analyst Agent ID from the Agent Engine deployment

We will need to register with Gemini Enterprise.
```
AGENT_ENGINE_LOCATION="us-central1"
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
DATA_ANALYST_AGENT_ID=`curl -X GET   -H "Authorization: Bearer $(gcloud auth print-access-token)"   "https://$AGENT_ENGINE_LOCATION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines" | grep -2 "Data Analyst Agent" | grep name | grep reasoningEngines | cut -d '/' -f2`
```


### 5.4. Test the  Data Analyst Agent on Agent Engine in the "Playground"


Navigate to the `Playground` tab and try out a few prompts.

![README](../04-images/M20-14.png)   
<br><br>

![README](../04-images/M20-15.png)   
<br><br>

![README](../04-images/M20-16.png)   
<br><br>

<hr>


## 6. Create the Agentspace App (Shoonya Retail Agentverse) on Gemini Enterprise

### 6.1. Create the application
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
AGENTSPACE_APP_ID="shoonya-agentverse"
AGENTSPACE_LOCATION="global"


curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-H "X-Goog-User-Project: $PROJECT_ID" \
"https://discoveryengine.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENTSPACE_LOCATION/collections/default_collection/engines?engineId=$AGENTSPACE_APP_ID" \
-d '{
  "displayName": "Shoonya Agentverse",
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

Visit the Gemini Enterprise UI on Cloud Shell and look at the app you just created.

![README](../04-images/M20-17.png)   
<br><br>


### 6.2. Check agents registered with the app you just created

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
AGENTSPACE_APP_ID="shoonya-agentverse"
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


![README](../04-images/M20-19.png)   
<br><br>


<hr>



## 7. Register the Data Analyst Agent with Agentspace on Gemini Enterprise


### 7.1. Register the agent on Agent Engine with Gemini Enterprise for the Agent UI experience

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
AGENTSPACE_APP_ID="shoonya-agentverse"
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
  "name": "projects/PROJECT_NBR/locations/global/collections/default_collection/engines/shoonya-agentverse/assistants/default_assistant/agents/16822893759314702269",
  "displayName": "Data Analyst Agent",
  "description": "An agent who can analyze data on your behalf with just natural language questions as input",
  "icon": {
    "uri": "ICON_URI"
  },
  "createTime": "2026-01-25T02:31:51.943848586Z",
  "adkAgentDefinition": {
    "provisionedReasoningEngine": {
      "reasoningEngine": "projects/PROJECT_ID/locations/us-central1/reasoningEngines/7130866169266831360"
    }
  },
  "state": "ENABLED"
}
```

Make note of the IDs here-
1. Agent ID on Gemini Enterprise is `16822893759314702269` in
`projects/606asdasdad20/locations/global/collections/default_collection/engines/shoonya-retail-agentverse/assistants/default_assistant/agents/16822893759314702269`
2. Agent name on Gemini Enterprise is `Data Analyst Agent`
3. Agent Engine (reasoning engine) ID is `7130866169266831360` from `projects/data-insights-quickstart/locations/us-central1/reasoningEngines/7130866169266831360`





### 7.2. Check agents registered with the app we created on Gemini enterprise

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
AGENTSPACE_APP_ID="shoonya-agentverse"
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
      "name": "projects/PROJECT_NBR/locations/global/collections/default_collection/engines/shoonya-agentverse/assistants/default_assistant/agents/16822893759314702269",
      "displayName": "Data Analyst Agent",
      "description": "An agent who can analyze data on your behalf with just natural language questions as input",
      "createTime": "2026-01-25T02:31:52.209085Z",
      "updateTime": "2026-01-25T02:34:38.901046763Z",
      "adkAgentDefinition": {
        "provisionedReasoningEngine": {
          "reasoningEngine": "projects/data-insights-quickstart/locations/us-central1/reasoningEngines/7130866169266831360"
        }
      },
      "state": "ENABLED"
    },
    {
      "name": "projects/PROJECT_NBR/locations/global/collections/default_collection/engines/shoonya-agentverse/assistants/default_assistant/agents/deep_research",
      "displayName": "Deep Research",
      "description": "This agent is a specialized agent that gathers, analyzes, and understands information from internal and external sources. It generates a plan, an in-depth report, and a summary.",
      "createTime": "2026-01-25T02:27:14.058043675Z",
      "updateTime": "2026-01-25T02:27:14.284137Z",
      "managedAgentDefinition": {},
      "state": "ENABLED",
      "sharingConfig": {
        "scope": "ALL_USERS"
      }
    }
  ]
}
```

Ensure the reasoning ending ID is the same as the value returned from running the below-
```
echo $DATA_ANALYST_AGENT_ID
```

![README](../04-images/M20-20.png)   
<br><br>

### 7.3. In case of discrepancies - update the Gemini Enterprise agent with the right Agent Engine agent ID ID 

Here is how you update the Agent Engine deployed Agent ID.<br>
SKIP THIS IF YOU HAVE THE RIGHT ID <br>
Documentation link: https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent#update_an_adk_agent

<hr>

## 8. Chat with the Data Analyst Agent in Gemini Enterprise

Launch the application as shown below.

![README](../04-images/M20-21.png)   
<br><br>

![README](../04-images/M20-22.png)   
<br><br>

![README](../04-images/M20-23.png)   
<br><br>

<hr>






