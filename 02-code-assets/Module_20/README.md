# Installation instructions - Gemini CLI and Managed MCP server for BigQuery

## 1. Gemini CLI setup on Mac

### 1.1. Configure your GCP project if not already

```
gcloud config set project "data-insights-quickstart"
```

### 1.2. Authenticate to Google Cloud

```
gcloud auth application-default login
```


### 1.3. Install nvm (Node Version Manager):

Open your terminal. Run the following command to install nvm:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

### 1.4. Install node

```
nvm install node

```

### 1.5. Verify

```
node -v
npm -v
```

### 1.6. Install Gemini CLI

```
npm install -g @google/gemini-cli
```

### 1.7. Grant yourself IAM permissions

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
PROJECT_NAME=`gcloud projects describe ${PROJECT_ID} | grep name | cut -d':' -f2 | xargs`
UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/mcp.toolUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/serviceusage.serviceUsageAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/iam.oauthClientViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/iam.serviceAccountViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/oauthconfig.editor"
```


### 1.8. Enable services

```
gcloud services enable bigquery.googleapis.com --project=${PROJECT_ID}
gcloud beta services mcp enable bigquery.googleapis.com --project=${PROJECT_ID}
```

### 1.9. Try Gemini

```
gemini
```

## 2. Using remote BigQuery managed MCP server from Gemini CLI

You need to configure BigQuery managed MCP server in your Gemini settings.

1. Create a directory structure
```
cd ~/.gemini
mkdir -p extensions/bq-managed-mcp
```

2. Create a file called gemini-extension.json inside this directory structure and paste the below. NOTE: Replace the project name with yours

```
{
  "name": "bq-managed-mcp",
  "version": "1.0.0",
  "mcpServers": {
    "bq-managed-mcp-server": {
      "httpUrl": "https://bigquery.googleapis.com/mcp",
      "authProviderType": "google_credentials",
      "oauth": {
        "scopes": ["https://www.googleapis.com/auth/bigquery"]
      },
      "timeout": 30000,
      "headers": {
        "x-goog-user-project": "data-insights-quickstart"
      }
    }
  }
}

```


3. Restart your terminal or run `source ~/.bashrc` or equivalent

4. Then start gemini CLI with `gemini` command and run `/mcp list` to list the MCP servers
5. And ask any database related questions










