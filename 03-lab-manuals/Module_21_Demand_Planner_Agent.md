# Module 21: [Capstone] Create a Demand Planner Agent 

In this tutorial we will create a demand planner agent, and deploy it to Agent Engine, then register it with Gemini Enterprise. As part of the agent developer continuum, we will test the agent with `adk web` locally, deploy and test on `agent engine` playground, and finally via the `gemini enterprise` UI. <br>

The demand planner agent can do the following:
1. Can run on-demand forecasting (TimesFM in BigQuery)
2. Can adjust forecasts based on demand signals for product (demand surge, slump)
3. Can do QnA on forecast data
4. Has limited access to view data, and to modify data

<hr>

## 1. Setup

### 1.1. Authenticate to Google Cloud from CLI & generate Application Default Credentials

Run each of these in cloud shell / terminal:
```
gcloud init
```

```
gcloud auth application-default login
```

<hr>

### 1.2. Create a user managed service account (UMSA) for the demand planner agent & grant it minimal permissions

#### 1.2.1. Run the below on cloud shell to create the UMSA:

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
LOCATION="us-central1"

DEMAND_PLANNER_UMSA="demand-planner-agent-sa"
DEMAND_PLANNER_UMSA_FQN="$DEMAND_PLANNER_UMSA@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $DEMAND_PLANNER_UMSA \
  --description="User Managed Service Account for Demand Planner Agent" \
  --display-name="Demand Planner Agent Service Account"
```

#### 1.2.2. Grant the UMSA requiste IAM permissions

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
  --role="roles/aiplatform.reasoningEngineServiceAgent"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
  --role="roles/iam.serviceAccountViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
--role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
--role="roles/iam.serviceAccountTokenCreator"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
  --role="roles/storage.objectCreator"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
--role="roles/discoveryengine.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
  --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
--role="roles/bigquery.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
--role="roles/bigquery.metadataViewer"

```

Lets ensure that our Demand Planner Agent has viewer access to the rscw_fridge_forecast_ds:
```
BQ_DATASET_IN_SCOPE_FOR_READS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_forecast_ds"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
--role="roles/bigquery.dataViewer" \
--condition="expression=resource.name.startsWith(\"$BQ_DATASET_IN_SCOPE_FOR_READS_RESOURCE_URI\"),title=ReadAccessToSpecificDataset"
```

Lets ensure we lock down write access for our Demand Planner Agent to just 3 tables:
```
BQ_DEMAND_FORECAST_TABLE_WRITE_ACCESS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_forecast_ds/tables/demand_forecast"
BQ_DEMAND_FORECAST_HISTORY_TABLE_WRITE_ACCESS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_forecast_ds/tables/demand_forecast_history"
BQ_PROCEDURE_ERROR_LOG_TABLE_WRITE_ACCESS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_forecast_ds/tables/procedure_error_log"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$DEMAND_PLANNER_UMSA_FQN" \
--role="roles/bigquery.dataEditor" \
--condition="expression=resource.name.startsWith(\"$BQ_DEMAND_FORECAST_TABLE_WRITE_ACCESS_RESOURCE_URI\") || resource.name.startsWith(\"$BQ_DEMAND_FORECAST_HISTORY_TABLE_WRITE_ACCESS_RESOURCE_URI\") || resource.name.startsWith(\"$BQ_PROCEDURE_ERROR_LOG_TABLE_WRITE_ACCESS_RESOURCE_URI\"),title=WriteAccessToSpecificTable"

```

####  1.2.3. Grant yourself permissions to impersonate the Data Analyst UMSA

Run the below in the terminal.
```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/iam.serviceAccountTokenCreator"

gcloud iam service-accounts add-iam-policy-binding \
    ${DEMAND_PLANNER_UMSA_FQN} \
    --member="user:${YOUR_UPN_FQN}" \
    --role="roles/iam.serviceAccountUser"
```
<hr>


## 2. Generate forecasts, and operationalize for agent use

### 2.1. Database setup, stored proecdure creation

## INSERT NOTEBOOK DETAILS HERE

### 2.2. Data Insights scan execution to generate dataset and table metadata for agentic grounding

## INSERT NOTEBOOK DETAILS HERE

<hr>

## 3. Review the Demand Planner Agent code 

### 3.1. Review the code layout in VS code/your IDE

Navigate to the `rscw-agent-solution` in vs code/your IDE <br>

Here is what the layout should look like if you navigate to the top level data_analyst_agent folder:
```
.
├── demand_planner_agent
│   ├── demand_planner_agent
│   │   ├── __init__.py
│   │   ├── agent.py -> core code
│   │   ├── constants.py -> configs
│   │   ├── system_instructions.py -> core code
│   │   ├── test.py -> agent engine deployment testing
│   │   ├── tools.py -> core code
│   │   └── utils.py -> core code
│   ├── miscellaneous
│   │   ├── enhancements.md
│   │   └── sample_prompts.md
│   └── requirements.txt

```

### 3.2. Study these specific code/config files

Open each of the files and review the code files.

<hr>

## 4. Run the agent locally

### 4.1. Set up a Python virtual environment in VS code / your IDE's terminal

Run the below in your terminal-
```
python -m venv .venv
source .venv/bin/activate
```

### 4.2. Install the Python dependencies

Navigate to the Data_Analytics_Agent folder that has the requirements.txt and run the install from VS code terminal-
`pip install -r requirements.txt`

### 4.3. Update the env file 

Modify the env file to reflect your GCP project ID, project number and location by updating the following with your details and saving the file-

```
GOOGLE_CLOUD_PROJECT="<YOUR_PROJECT_ID>"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_CLOUD_PROJECT_NUMBER="<YOUR_PROJECT_NUMBER>"

GOOGLE_GENAI_USE_VERTEXAI="True"
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true

GEMINI_MODEL="gemini-2.5-pro"

BQ_DATASETS_IN_SCOPE="rscw_fridge_forecast_ds"
BQ_METADATA_BUCKET="rscw-workshop-fridge-stage-<YOUR_PROJECT_NUMBER>"
BQ_METADATA_FILE="frige-forecast-metadata-for-agent-grounding.md"

DATA_ANALYST_USER_MANAGED_SERVICE_ACCOUNT_FQN="demand-planner-agent-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com"

AGENT_DEPLOYMENT_BUCKET="agent-deployment-bucket-<YOUR_PROJECT_NUMBER>"
DEPLOYED_AGENT_RESOURCE_URI="projects/<YOUR_PROJECT_NUMBER>/locations/us-central1/reasoningEngines/1306920202704781312"
```

![README](../04-images/M20-10.png)   
<br><br>


### 4.4. Launch a terminal in VS Code/your IDE and authenticate

Follow instructions in section 1.

### 4.5. Run adk web

In the terminal navigate to the top level data_analyst_agent directory and run the command below.<br>
(e.g. from author - `/Users/akhanolkar/github/rscw-agent-solution/demand_planner_agent`)

```
adk web
```

![README](../04-images/M20-10b.png)   
<br><br>

![README](../04-images/M20-10c.png)   
<br><br>


### 4.6. Try out a few prompts

The code base includes sample prompts, you can grab a few and try out like below.

![README](../04-images/M20-11.png)   
<br><br>

![README](../04-images/M20-12.png)   
<br><br>

We now know our agent is able to access data from BigQuery.

Lets trying querying tables from a different dataset, the agent should state that it cannot.

![README](../04-images/M20-12b.png)   
<br><br>

Lets try to get the agent to delete all the data, the agent should state that it cannot.

![README](../04-images/M20-12c.png)   
<br><br>


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
AGENT_ENGINE_LOCATION="us-central1"

adk deploy agent_engine \
--project=$PROJECT_ID   \
--region=$AGENT_ENGINE_LOCATION   \
--display_name="Demand Planner"   \
--description="An agent that can generate demand forecasts, adjust forecasts and answer natural language questions about forecast data in the BQ dataset rscw_fridge_forecast_ds" \
--staging_bucket=gs://agent-deployment-bucket-$PROJECT_NBR   \
--env_file="./demand_planner_agent/.env"   \
--trace_to_cloud   \
./demand_planner_agent
```

![README](../04-images/M20-13a.png)   
<br><br>

![README](../04-images/M20-13d.png)   
<br><br>

![README](../04-images/M20-13e.png)   
<br><br>

![README](../04-images/M20-13b.png)   
<br><br>

![README](../04-images/M20-13c.png)   
<br><br>


### 5.3. Retrieve the Demand Planner Agent ID from the Agent Engine deployment

We will need to register with Gemini Enterprise.
```
AGENT_ENGINE_LOCATION="us-central1"
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
DEMAND_PLANNER_AGENT_ID=`curl -X GET   -H "Authorization: Bearer $(gcloud auth print-access-token)"   "https://$AGENT_ENGINE_LOCATION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines"  |  grep reasoningEngines | grep name | cut -d'/' -f6 | cut -d '"' -f1`
echo $DEMAND_PLANNER_AGENT_ID
```

### 5.4. Update the .env file with the agent engine ID

Here is the agent engine ID:

![README](../04-images/M20-13d.png)   
<br><br>

Update the .env to reflect the agent engine ID:


![README](../04-images/M20-13f.png)   
<br><br>


### 5.5. Test the  Demand Planner Agent on Agent Engine in the "Playground"

#### 5.5.1. Test via the UI

Navigate to the `Playground` tab and try out a few prompts.<br>

1. Lets check if it can access the metadata (grounding file) and retireve results without tool call <br>

![README](../04-images/M20-14.png)   
<br><br>

2. Lets run a query to fetch some data

![README](../04-images/M20-15.png)   
<br><br>

3. Lets try multi-turn

![README](../04-images/M20-16.png)   
<br><br>

![README](../04-images/M20-16b.png)   
<br><br>

![README](../04-images/M20-16c.png)   
<br><br>



#### 5.5.2. Test via Python script

1. Ensure you completed the .env update to reflect your deployed reasoningEngine agent ID from step 5.4

2. Ensure you are at the right location
```
# Navigate so that you are at the top level directory of demand_planner_agent
/Users/akhanolkar/Projects/github/rscw-agent-solution/demand_planner_agent <- HERE
```

3. Execute script

```
python test.py 
```

4. Browse the output streamed

![README](../04-images/M20-16d.png)   
<br><br>

![README](../04-images/M20-16e.png)   
<br><br>

![README](../04-images/M20-16f.png)   
<br><br>


<hr>


## 6. Revisit the Agentspace App (Shoonya Agentverse) on Gemini Enterprise


### 6.1. Check agents registered with the app you just created

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

```


![README](../04-images/M20-19.png)   
<br><br>


<hr>



## 7. Register the Demand Planner Agent with Agentspace on Gemini Enterprise


### 7.1. Register the agent on Agent Engine with Gemini Enterprise for the Agent UI experience

```
AGENT_ENGINE_LOCATION="us-central1"
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
DEMAND_PLANNER_AGENT_ID=`curl -X GET   -H "Authorization: Bearer $(gcloud auth print-access-token)"   "https://$AGENT_ENGINE_LOCATION-aiplatform.googleapis.com/v1/projects/$PROJECT_ID/locations/$AGENT_ENGINE_LOCATION/reasoningEngines"  |  grep reasoningEngines | grep name | cut -d'/' -f6 | cut -d '"' -f1`
echo $DEMAND_PLANNER_AGENT_ID

PAYLOAD="{
     \"displayName\": \"Data Analyst\",
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
  "name": "projects/606804615020/locations/global/collections/default_collection/engines/shoonya-agentverse/assistants/default_assistant/agents/1624231307787687665",
  "displayName": "Data Analyst",
  "description": "An agent who can analyze data on your behalf with just natural language questions as input",
  "icon": {
    "uri": "ICON_URI"
  },
  "createTime": "2026-01-26T21:39:13.955130226Z",
  "adkAgentDefinition": {
    "provisionedReasoningEngine": {
      "reasoningEngine": "projects/data-insights-quickstart/locations/us-central1/reasoningEngines/1306920202704781312"
    }
  },
  "state": "ENABLED"
}
```

Make note of the IDs here-
1. Agent ID on Gemini Enterprise is `1624231307787687665` in
`projects/sdfsdfsdf/locations/global/collections/default_collection/engines/shoonya-agentverse/assistants/default_assistant/agents/1624231307787687665`
2. Agent name on Gemini Enterprise is `Data Analyst`
3. Agent Engine (reasoning engine) ID is `1306920202704781312` from `projects/data-insights-quickstart/locations/us-central1/reasoningEngines/1306920202704781312`
4. It is super important that the right reasoning engine is registered with Gemini Enterprise for things to work



### 7.2. Check agents registered with the app we created on Gemini enterprise

```
curl -X GET \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
"https://$AGENTSPACE_LOCATION-discoveryengine.googleapis.com/v1alpha/projects/$PROJECT_ID/locations/$AGENTSPACE_LOCATION/collections/default_collection/engines/$AGENTSPACE_APP_ID/assistants/default_assistant/agents"

```
Here is what the author got back:
```
THIS IS INFORMATIONAL


```


![README](../04-images/M20-20.png)   
<br><br>

### 7.3. In case of discrepancies - update the Gemini Enterprise agent with the right Agent Engine agent ID ID 

Here is how you update the Agent Engine deployed Agent ID.<br>
SKIP THIS IF YOU HAVE THE RIGHT ID <br>
Documentation link: https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-an-adk-agent#update_an_adk_agent

<hr>

## 8. Chat with the Demand Planner Agent in Gemini Enterprise

Launch the application as shown below.

![README](../04-images/M20-21.png)   
<br><br>

![README](../04-images/M20-22.png)   
<br><br>

![README](../04-images/M20-23.png)   
<br><br>

![README](../04-images/M20-24.png)   
<br><br>

![README](../04-images/M20-25.png)   
<br><br>

![README](../04-images/M20-26.png)   
<br><br>

![README](../04-images/M20-27.png)   
<br><br>


<hr>





