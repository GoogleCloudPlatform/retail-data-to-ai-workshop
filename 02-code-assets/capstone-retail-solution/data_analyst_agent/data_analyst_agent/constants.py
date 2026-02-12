import os, dotenv
from vertexai.generative_models import GenerationConfig,SafetySetting, HarmCategory


dotenv.load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'project_not_set')
LOCATION = os.getenv('LOCATION', 'us-central1')
DEPLOYMENT_USER_MANAGED_SERVICE_ACCOUNT_FQN = os.getenv('DEPLOYMENT_USER_MANAGED_SERVICE_ACCOUNT_FQN', 'deployment_user_managed_service_account_fqn_not_set')
DATA_ANALYST_USER_MANAGED_SERVICE_ACCOUNT_FQN = os.getenv('DATA_ANALYST_USER_MANAGED_SERVICE_ACCOUNT_FQN','agent_user_managed_service_account_fqn_not_set')

BQ_DATASET_IN_SCOPE = os.getenv('BQ_DATASET_IN_SCOPE', 'bq_datasets_in_scope_not_set')
BQ_METADATA_BUCKET = os.getenv('BQ_METADATA_BUCKET', 'bq_metadata_bucket_not_set')
BQ_METADATA_FILE = os.getenv('BQ_METADATA_FILE', 'bq_metadata_file_not_set')

AGENT_DEPLOYMENT_BUCKET = os.getenv('AGENT_DEPLOYMENT_BUCKET', 'agent_deployment_bucket_not_set')
DEPLOYED_AGENT_RESOURCE_URI = os.getenv('DEPLOYED_AGENT_RESOURCE_URI', 'deployed_agent_resource_uri_not_set')

GOOGLE_GENAI_USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'False')

MODEL = os.getenv('GEMINI_MODEL', 'gemini_model_not_set')
SAFETY_SETTINGS = [
    SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
    SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
    SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
    SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
]
GENERATION_CONFIGURATION_TEMPERATURE = 0.0
GENERATION_CONFIGURATION_TOP_P = 0.0
GENERATION_CONFIGURATION_TOP_K = 1
GENERATION_CONFIGURATION_MAX_OUTPUT_TOKENS = 65536
GENERATION_CONFIGURATION = GenerationConfig(
    temperature=GENERATION_CONFIGURATION_TEMPERATURE,
    top_p=GENERATION_CONFIGURATION_TOP_P,
    top_k=GENERATION_CONFIGURATION_TOP_K,
    max_output_tokens=GENERATION_CONFIGURATION_MAX_OUTPUT_TOKENS,
)