import os, dotenv

dotenv.load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'project_not_set')
LOCATION = os.getenv('LOCATION', 'us-central1')
DEPLOYMENT_USER_MANAGED_SERVICE_ACCOUNT_FQN = os.getenv('DEPLOYMENT_USER_MANAGED_SERVICE_ACCOUNT_FQN', 'deployment_user_managed_service_account_fqn_not_set')
DATA_ANALYST_USER_MANAGED_SERVICE_ACCOUNT_FQN = os.getenv('DATA_ANALYST_USER_MANAGED_SERVICE_ACCOUNT_FQN','agent_user_managed_service_account_fqn_not_set')

BQ_DATASETS_IN_SCOPE = os.getenv('BQ_DATASETS_IN_SCOPE', 'bq_datasets_in_scope_not_set')
AGENT_DEPLOYMENT_BUCKET = os.getenv('AGENT_DEPLOYMENT_BUCKET', 'agent_deployment_bucket_not_set')
DEPLOYED_AGENT_RESOURCE_URI = os.getenv('DEPLOYED_AGENT_RESOURCE_URI', 'deployed_agent_resource_uri_not_set')

GOOGLE_GENAI_USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'False')