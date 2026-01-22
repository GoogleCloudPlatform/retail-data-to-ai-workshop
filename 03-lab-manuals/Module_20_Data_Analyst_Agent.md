# Module 20: [ADK Primer] Create a Data Analyst Agent

## 1. Setup

### 1.1. Authenticate to Google Cloud from CLI


### 1.2. Ingest the refrigerator dataset from CLI


### 1.3. Run the notebook that executes the Data Insights documentation scans & persists metadata to GCS


### 1.4. Set up VS code or use any IDE on your machine


### 1.5. Clone this repo if you have not already done so


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

### 4.2. Create a user managed service account (UMSA) for the Data Analyst Agent

### 4.3. Grant the UMSA, requisite incremental IAM permissions 

### 4.4. Lock down the BigQuery datasets the Data Analyst Agent UMSA has access to

<hr>

## 5. Deploy the Data Analyst Agent to Agent Engine

### 5.1. Deploy the agent to Agent Engine

### 5.2. Capture the identifier of the agent deployed

### 5.3. Test the remote Data Analyst Agent on Agent Engine programmatically from your IDE

<hr>


## 6. Register the Data Analyst Agent with Agentspace on Gemini Enterprise



<hr>






