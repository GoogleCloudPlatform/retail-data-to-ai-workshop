import os, dotenv
from vertexai.generative_models import GenerationConfig,SafetySetting, HarmCategory


dotenv.load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'project_not_set')
LOCATION = os.getenv('LOCATION', 'us-central1')
DEPLOYMENT_USER_MANAGED_SERVICE_ACCOUNT_FQN = os.getenv('DEPLOYMENT_USER_MANAGED_SERVICE_ACCOUNT_FQN', 'deployment_user_managed_service_account_fqn_not_set')
DATA_ANALYST_USER_MANAGED_SERVICE_ACCOUNT_FQN = os.getenv('DATA_ANALYST_USER_MANAGED_SERVICE_ACCOUNT_FQN','agent_user_managed_service_account_fqn_not_set')

BQ_DATASET_IN_SCOPE = os.getenv('BQ_DATASET_IN_SCOPE', 'bq_dataset_in_scope_not_set')
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

AGENT_ACTIVITY_LOG_SQL = "select * from capstone_ds.agent_activity_log order by execution_date desc"
AVAILABLE_TO_PROMISE_REPORT_SQL = "WITH RankedStock AS (SELECT sml.location_id, lm.location_name, sml.omni_item_id, sml.quantity_on_hand, sml.stock_date, ROW_NUMBER() OVER(PARTITION BY sml.location_id, sml.omni_item_id ORDER BY sml.stock_date DESC) as rn FROM `capstone_ds.stock_master_location` AS sml JOIN `capstone_ds.location_master` AS lm ON sml.location_id = lm.location_id WHERE LOWER(lm.location_type) = 'warehouse' ) SELECT location_name, omni_item_id, quantity_on_hand, stock_date FROM RankedStock WHERE rn = 1 ORDER BY location_name, omni_item_id"
AVERAGE_RATE_OF_SALE_REPORT_SQL = "select * from capstone_ds.vw_avg_rate_of_sale"
DEMAND_FORECAST_SQL = "select * from capstone_ds.demand_forecast order by forecast_datetime"
DEMAND_SIGNAL_LOG_SQL = "select * from capstone_ds.demand_signal_log order by signal_datetime desc"
FILL_RATE_REPORT_SQL = "SELECT * FROM capstone_ds.vw_supplier_fill_rate"
FLEET_ITEMS_DELIVERY_SUMMARY_REPORT_SQL = "select * from capstone_ds.vw_fleet_items"
FLEET_USAGE_SUMMARY_REPORT_SQL = "select * from capstone_ds.vw_fleet_usage"
INVENTORY_AGING_REPORT_SQL = "select * from capstone_ds.vw_inventory_aging"
INVENTORY_ALLOCATION_REPORT_SQL = "SELECT * FROM capstone_ds.stock_allocation_plan where is_current=true order by omni_item_id, location_id"
INVENTORY_RECONCILIATION_REPORT_SQL = "SELECT * FROM capstone_ds.vw_stock_reconciliation"
LOC_BASED_TRANSFER_VOLUME_SUMMARY_REPORT_SQL = "select * from capstone_ds.vw_transfer_volume"
LOW_STOCK_REPORT_SQL = "WITH RankedInventory AS (SELECT omni_item_id, quantity_on_hand, reorder_point, stock_date, ROW_NUMBER() OVER (PARTITION BY omni_item_id ORDER BY stock_date DESC) as rn FROM `capstone_ds.stock_master` ) SELECT omni_item_id, quantity_on_hand, reorder_point FROM RankedInventory WHERE rn = 1 AND quantity_on_hand < reorder_point ORDER BY omni_item_id"
ON_HAND_INVENTORY_REPORT_SQL = "select * from capstone_ds.vw_on_hand_stock"
ON_HAND_LOC_INVENTORY_REPORT_SQL = "select * from capstone_ds.vw_on_hand_loc_stock"
OUT_OF_STOCK_REPORT_SQL = "SELECT pm.omni_item_id, pm.description, lm.location_name, sml.quantity_on_hand FROM `capstone_ds.stock_master_location` AS sml JOIN `capstone_ds.product_master` AS pm ON sml.omni_item_id = pm.omni_item_id JOIN `capstone_ds.location_master` AS lm ON sml.location_id = lm.location_id WHERE sml.quantity_on_hand = 0"
PURCHASE_ORDER_STATUS_REPORT_SQL = "select * from capstone_ds.vw_stock_purchase_orders order by omni_item_id,order_date,order_status desc"
REORDER_POINT_REPORT_SQL = "SELECT distinct pm.item_number,pm.omni_item_id, pm.description, sm.quantity_on_hand, sm.reorder_point FROM `capstone_ds.stock_master` AS sm JOIN `capstone_ds.product_master` AS pm ON (sm.omni_item_id = pm.omni_item_id and sm.item_number = pm.item_number) WHERE sm.quantity_on_hand <= sm.reorder_point and sm.stock_date=(select max(stock_date) from capstone_ds.stock_master)"
STOCK_MOVEMENT_SUMMARY_REPORT_SQL = "select * from capstone_ds.vw_stock_movement_summary"
STOCK_TRANSFER_FULFILLMENT_REPORT_SQL = "select * from capstone_ds.vw_stock_transfer_fulfill"
SUGGESTED_REORDER_REPORT_SQL = "SELECT * FROM capstone_ds.vw_suggested_reorder"
UNDER_PERFORMING_INVENTORY_REPORT_SQL = "SELECT * FROM capstone_ds.vw_stock_reconciliation WHERE received_qty > 0 and pos_sold_qty = 0"
WEEKS_OF_SUPPLY_REPORT_SQL = "select * from capstone_ds.vw_weeks_of_supply"
WEIGHTED_LEAD_TIME_REPORT_SQL = "SELECT * FROM capstone_ds.vw_weighted_lead_time"

