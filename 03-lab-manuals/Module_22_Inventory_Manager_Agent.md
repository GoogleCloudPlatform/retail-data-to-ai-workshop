# Module 22: [Capstone] Create an Inventory Manager Agent 

You are already familiar with agent development from the previous modules. This module is identical, we are merely creating a different persona. The drill is the same - as part of the agent developer continuum, we will test the agent with `adk web` locally, deploy and test on `agent engine` playground. We will skip Gemini Enterprise registration as the focus is merely a functionally adequate UI for our agents, and ADK and Agent Engine playground are sufficient.<br>

The inventory manager agent can do the following:
1. Generate the default inventory allocation plan
2. Adjust inventory allocation across stores and warehouse
3. Answer any adhoc questions (best effort)
4. Generate a variety of canned reports:<br>
a) Inventory Reconciliation Report<br>
b) On Hand Inventory Report<br>
c) Available to Promise Report<br>
d) Low Stock Report<br>
e) Stock Movement Summary Report<br>
f) Out of Stock Report<br>
g) Reorder Point Report<br>
h) Inventory Aging Report<br>
i) Inventory Allocation Report<br>
j) Under-performing Inventory Report<br>

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

Make sure you set the GCP project-
```
gcloud config set project <YOUR_PROJECT_ID>
```

<hr>

### 1.2. Create a user managed service account (UMSA) for the agent & grant it minimal permissions

#### 1.2.1. Run the below on cloud shell to create the UMSA:

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
LOCATION="us-central1"

AGENT_UMSA="inventory-manager-agent-sa"
AGENT_UMSA_FQN="$AGENT_UMSA@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $AGENT_UMSA \
  --description="User Managed Service Account for Inventory Manager Agent" \
  --display-name="Inventory Manager Agent Service Account"
```

#### 1.2.2. Grant the UMSA requiste IAM permissions

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AGENT_UMSA_FQN" \
  --role="roles/aiplatform.reasoningEngineServiceAgent"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AGENT_UMSA_FQN" \
  --role="roles/iam.serviceAccountViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AGENT_UMSA_FQN" \
--role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AGENT_UMSA_FQN" \
--role="roles/iam.serviceAccountTokenCreator"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AGENT_UMSA_FQN" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AGENT_UMSA_FQN" \
  --role="roles/storage.objectCreator"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$AGENT_UMSA_FQN" \
  --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AGENT_UMSA_FQN" \
--role="roles/bigquery.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AGENT_UMSA_FQN" \
--role="roles/bigquery.metadataViewer"

```

Lets ensure that our Demand Planner Agent has viewer access to the rscw_fridge_forecast_ds:
```
BQ_DATASET_1_IN_SCOPE_FOR_READS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_forecast_ds"
BQ_DATASET_2_IN_SCOPE_FOR_READS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_ds"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AGENT_UMSA_FQN" \
--role="roles/bigquery.dataViewer" \
--condition="expression=resource.name.startsWith(\"$BQ_DATASET_1_IN_SCOPE_FOR_READS_RESOURCE_URI\") && resource.name.startsWith(\"$BQ_DATASET_2_IN_SCOPE_FOR_READS_RESOURCE_URI\"),title=ReadAccessToSpecificDatasets"
```

Lets ensure we lock down write access for our agent to just a few tables:
```
BQ_STOCK_ALLOC_TABLE_WRITE_ACCESS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_ds/tables/inventory_allocation"
BQ_PROCEDURE_ERROR_LOG_TABLE_WRITE_ACCESS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_ds/tables/procedure_error_log"
BQ_ACTIVITY_LOG_TABLE_WRITE_ACCESS_RESOURCE_URI="projects/$PROJECT_ID/datasets/rscw_fridge_ds/tables/activity_log"

gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:$AGENT_UMSA_FQN" \
--role="roles/bigquery.dataEditor" \
--condition="expression=resource.name.startsWith(\"$BQ_STOCK_ALLOC_TABLE_WRITE_ACCESS_RESOURCE_URI\") || resource.name.startsWith(\"$BQ_PROCEDURE_ERROR_LOG_TABLE_WRITE_ACCESS_RESOURCE_URI\") || resource.name.startsWith(\"$BQ_ACTIVITY_LOG_TABLE_WRITE_ACCESS_RESOURCE_URI\" ),title=WriteAccessToSpecificTables"

```

####  1.2.3. Grant yourself permissions to impersonate the UMSA

Run the below in the terminal.
```
YOUR_UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$YOUR_UPN_FQN" \
  --role="roles/iam.serviceAccountTokenCreator"

gcloud iam service-accounts add-iam-policy-binding \
    ${AGENT_UMSA_FQN} \
    --member="user:${YOUR_UPN_FQN}" \
    --role="roles/iam.serviceAccountUser"
```
<hr>


## 2. Incremental database object creation, and operationalizing for agent use

We will use a to complete this section. It is imperative that you complete this section carefully to ensure the agent has the appropriate grounding and tooling in place.

### 2.1. Database setup, stored procedure creation

1. Run the notebook `Module_22_Inventory_Manager_Utils_Prework.ipynb` in BigQuery
2. Visit the Cloud Console and browse the objects created  

<hr>

## 3. Review the Inventory Manager Agent code 

### 3.1. Review the code layout in VS code/your IDE

Navigate to the `rscw-agent-solution` in vs code/your IDE <br>

Here is what the layout should look like if you navigate to the top level inventory_manager_agent folder:
```
.
├── inventory_manager_agent
│   ├── inventory_manager_agent
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

<br><br>

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

Navigate to the Inventory_Manager_Agent folder that has the requirements.txt and run the install from VS code terminal-
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

BQ_DATASETS_IN_SCOPE=["rscw_fridge_ds","rscw_fridge_forecast_ds"]
BQ_METADATA_BUCKET="rscw-workshop-fridge-stage-<YOUR_PROJECT_NUMBER>"
BQ_METADATA_FILE_FOR_CORE_DATASET="fridge-metadata-for-agent-grounding.md"
BQ_METADATA_FILE_FOR_FORECAST_DATASET="fridge-forecast-metadata-for-agent-grounding.md"

INVENTORY_MANAGER_SERVICE_ACCOUNT_FQN="inventory-manager-agent-sa@<YOUR_PROJECT_ID>.iam.gserviceaccount.com"

AGENT_DEPLOYMENT_BUCKET="agent-deployment-bucket-<YOUR_PROJECT_NUMBER>"
DEPLOYED_AGENT_RESOURCE_URI="projects/<YOUR_PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<THIS_WILL_COME_LATER>"
```


<br><br>


### 4.4. Launch a terminal in VS Code/your IDE and authenticate

Follow instructions in section 1.

### 4.5. Run adk web

In the terminal navigate to the top level inventory_manager_agent directory and run the command below.<br>
(e.g. from author - `/Users/akhanolkar/github/rscw-agent-solution/inventory_manager_agent`)

```
adk web
```



### 4.6. Try out a few prompts

The code base includes sample prompts, you can grab a few and try out. The code base includes several tried and tested prompts under the miscellaneous directory, in the "sample_prompts" file.


<hr>

## 5. Deploy & test the Inventory Manager Agent on Agent Engine

### 5.1. Deploy the agent to Agent Engine

Run this from within the top level inventory_manager_agent folder, from CLI. This will automatically read in any configs in agent_engine_config.json
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
AGENT_ENGINE_LOCATION="us-central1"

adk deploy agent_engine \
--project=$PROJECT_ID   \
--region=$AGENT_ENGINE_LOCATION   \
--display_name="Inventory Manager"   \
--description="An agent that can generate inventory allocation plan, adjust allocation, runa number of canned reports and answer adhoc natural language questions about inventory data in the BQ dataset rscw_fridge_ds" \
--staging_bucket=gs://agent-deployment-bucket-$PROJECT_NBR   \
--env_file="./inventory_manager_agent/.env"   \
--trace_to_cloud   \
./inventory_manager_agent
```


### 5.2. Review the deployment on the Cloud Console

![README](../04-images/M22_5_2.png)   
<br><br>

### 5.3. Test the agent deployed to Agent Engine from the playground tab

We will need to ensure the agent engine deployment works right, run a few prompts.


![README](../04-images/M22_5_3.png)   
<br><br>

<hr>

This concludes the module. Please proceed to the next module.





