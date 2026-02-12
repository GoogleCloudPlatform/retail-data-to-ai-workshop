# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines utils."""


from google.cloud import bigquery, storage
from google.api_core import exceptions
import google.auth
import itertools, json, logging
from . import constants
from typing import Optional


# Instantiate logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def read_file_in_gcs_into_string(bucket_name: str, file_path: str) -> str:
    """Reads file content in GCS and returns it as a string.

    Args:
      bucket_name: The name of the GCS bucket.
      file_path: The path to the file in the bucket.

    Returns:
      Returns the file content as a string
    """
    try:
        # 1. Initialize the Storage Client
        client = storage.Client()
        
        # 2. Get the bucket and the specific file (blob)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        
        # 3. Download the content as a UTF-8 string
        content = blob.download_as_text()
        
        return content

    except Exception as e:
        logger.critical(f"An unexpected error occurred while reading file in GCS: {e}")
        return f"An unexpected error occurred while reading file in GCS: {e}"


def get_bq_client() -> Optional[bigquery.Client]:
  """Initializes and returns a BigQuery client.

  Returns:
      Optional[bigquery.Client]: A BigQuery client instance, or None if
      initialization fails.
  """

  try:
    client = bigquery.Client(project=constants.PROJECT_ID)
    return client
  except google.auth.exceptions.DefaultCredentialsError as e:
    logger.critical(f"Authentication failed: {e}")
    logger.critical(
        "Please configure your GCP credentials."
        "See https://cloud.google.com/docs/authentication/provide-credentials-adc"
    )
    return None
  except Exception as e:
    logger.critical(f"An unexpected error occurred while creating BigQuery client: {e}")
    return None


def execute_bq_sql_query(
    sql_query: str
) -> Optional[bigquery.table.RowIterator]:
    """Executes a SQL query and returns the results.

    Args:
        bq_client: The BigQuery client.
        sql_query: The SQL query to execute.

    Returns:
        Optional[bigquery.table.RowIterator]: An iterator for the query
        results, or None if an error occurs.
    """

    try:
        bq_client = get_bq_client()

        if not bq_client:
            logger.critical("BigQuery client is not available.")
            return None
 
        rows = bq_client.query_and_wait(sql_query)  # Make an API request.
        return rows
    except exceptions.GoogleAPICallError as e:
        logger.critical(f"BigQuery API call failed: {e}")
        return None
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        return None

def generate_markdown_table_from_bq_rows(row_iterator: bigquery.table.RowIterator):
    """Generates a Markdown table from a BigQuery row iterator."""


    if not row_iterator:
        return "No results to display."
    try:
        headers = [field.name for field in row_iterator.schema]

        markdown_table = "|" + "|".join(headers) + "|\n"
        markdown_table += "|" + "|".join(["---"] * len(headers)) + "|\n"

        for row in row_iterator:
            row_values = [str(row[header]) for header in headers]
            markdown_table += "|" + "|".join(row_values) + "|\n"

        logger.info(f"Markdown Table: {markdown_table}")

        return markdown_table
    except Exception as e:
        logger.critical(f"Error generating markdown table: {e}")
        return "Error generating markdown table."

def get_query_results_markdown(sql_query: str) -> str:
    """Executes a SQL query and returns the results as a Markdown table."""

    rows = execute_bq_sql_query(sql_query)
    if rows is None:
        logger.info("Failed to execute query and retrieve results.")
        return "Failed to execute query and retrieve results."
    else:
        markdown_table = generate_markdown_table_from_bq_rows(rows)
        return markdown_table
    
def get_query_results(sql_query: str):
    """Executes a SQL query and returns the results as a list of dictionaries."""

    rows = execute_bq_sql_query(sql_query)
    if rows is None:
        logger.info("Failed to execute query and retrieve results.")
        return None
    else:
        return [dict(row) for row in rows]
    
def field_to_dict(field: bigquery.SchemaField) -> dict:
        """
        Recursively convert a SchemaField into a dict, including subfields if any.
        """
        field_dict = {"name": field.name, "description": field.description or ""}
        # If the field is a RECORD with nested fields, recurse
        if field.fields:
            field_dict["fields"] = [
                field_to_dict(subfield) for subfield in field.fields
            ]
        return field_dict

def fetch_all_tables_metadata_json() -> str:
    """
    Retrieves detailed info about each table in the specified datasets and
    returns it as a JSON string. For each table, it includes:
      - table_name (full path in 'project.dataset.table')
      - description
      - columns (list of columns with name, description)
        * handles nested fields (RECORD type) recursively
    """

    table_iterators = []
    project_id = constants.PROJECT_ID

    try:
        bq_client = bigquery.Client(project=project_id)
        bq_dataset_list = constants.SOURCE_BQ_DATASETS_IN_SCOPE
 
        for ds_id in bq_dataset_list:
             
            try:
                table_iterators.append(bq_client.list_tables(f"{project_id}.{ds_id}"))
            except exceptions.NotFound:
                logger.info(f"Dataset not found, skipping: {project_id}.{ds_id}")
    except google.auth.exceptions.DefaultCredentialsError as e:
        logger.critical(f"Authentication failed: {e}")
        return json.dumps({"error": f"Authentication failed: {e}"})
    except Exception as e:
        logger.critical(f"An unexpected error occurred during client setup: {e}")   
        return json.dumps(
            {"error": f"An unexpected error occurred during client setup: {e}"}
        )

    all_tables_info = []
    for table_item in itertools.chain.from_iterable(table_iterators):
        full_table_id = ""  # Initialize here for the except block
        try:
            full_table_id = (
                f"{table_item.project}.{table_item.dataset_id}.{table_item.table_id}"
            )

            table_obj = bq_client.get_table(full_table_id)
            table_info = {
                "table_name": full_table_id,
                "description": table_obj.description or "",
                "columns": [field_to_dict(f) for f in table_obj.schema],
            }
            all_tables_info.append(table_info)
        except exceptions.NotFound:
            logger.info(f"Table not found, skipping: {full_table_id}")
            continue
        except Exception as e:
            logger.info(f"Could not process table {full_table_id}: {e}")
            continue

    # Convert the list of table dictionaries to a JSON string
    return json.dumps(all_tables_info, indent=2)

def fetch_bq_table_schema(table_fq_resource_uri: str) -> str:
    """
    Retrieves the BQ table metadata
    """

    try:
        bq_client = bigquery.Client(project=constants.PROJECT_ID)
        table_resource_uri_parts = table_fq_resource_uri.split("/")
        full_table_id=table_resource_uri_parts[6] + "." + table_resource_uri_parts[8].rstrip('"')
        try:
            table_obj = bq_client.get_table(full_table_id.strip())


            serializable_schema = []
            for field in table_obj.schema:
                field_dict = {
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description,
                }
                if field.fields:  # Handle nested fields for RECORD types
                    field_dict["fields"] = [
                        {
                            "name": nested_field.name,
                            "type": nested_field.field_type,
                            "mode": nested_field.mode,
                            "description": nested_field.description,
                        }
                        for nested_field in field.fields
                    ]
                serializable_schema.append(field_dict)

            return json.dumps(serializable_schema, indent=2)
        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}")
            return json.dumps({"error": f"An unexpected error occurred: {e}"}
        )

    except google.auth.exceptions.DefaultCredentialsError as e:
        logger.critical(f"Authentication failed: {e}")
        return json.dumps({"error": f"Authentication failed: {e}"})
    except exceptions.NotFound:
        logger.critical(f"Resource not found: {table_fq_resource_uri}") 
        return json.dumps(
            {"error": "Resource not found"}
        )
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        return json.dumps(
            {"error": f"An unexpected error occurred: {e}"}
        )
    
def update_table_schema(project_id: str, dataset_id: str, table_id: str, new_schema: list[bigquery.SchemaField]):
    """
    Updates the schema of a BigQuery table.

    Args:
        project_id: The project ID.
        dataset_id: The dataset ID.
        table_id: The table ID.
        new_schema: A list of bigquery.SchemaField objects for the new schema.
    """

    # Instantiates a BQ connection
    try:
        bq_client = bigquery.Client(project=project_id)
        logger.info("BigQuery client initialized successfully.")
    except Exception as e:
        logger.critical(f"Error initializing BigQuery client: {e}")
        logger.info("Please ensure you have authenticated with 'gcloud auth application-default login'")
        logger.info("and that your PROJECT_ID is correct.")
        return

    table_ref = bq_client.dataset(dataset_id).table(table_id)

    try:
        table = bq_client.get_table(table_ref)
        logger.info(f"Fetched table: {table.project}.{table.dataset_id}.{table.table_id}")
    except NotFound:
        logger.critical(f"Error: Table {dataset_id}.{table_id} not found.")
        return
    except Exception as e:
        logger.critical(f"An error occurred while fetching the table: {e}")
        return

    # Set the table's schema to the newly constructed schema.
    table.schema = new_schema

    # Make the API call to update the table's schema.
    # The second argument to update_table() specifies which properties to update.
    try:
        table = bq_client.update_table(table, ["schema"])  # API request
        logger.info(f"\nSuccessfully updated the table schema for {table.table_id}.")

        #for field in table.schema:
        #    print(f" - {field.name} ({field.field_type}): {field.description}")       
    except Exception as e:
        logger.critical(f"\nAn error occurred while updating the table schema: {e}")


def fetch_list_of_tables_in_dataset(dataset_id: str) :
    """Fetches a list of table IDs in a given BigQuery dataset.

    Args:
        dataset_id: The ID of the dataset.

    Returns:
        A list of table IDs, or an empty list if an error occurs.
    """
    client = get_bq_client()
    if not client:
        logger.critical("Failed to initialize BigQuery client.")
        return ["Failed to initialize BigQuery client."]

    try:
        bq_tables_list = client.list_tables(dataset_id)  # Make an API request.
        return [table.table_id for table in bq_tables_list]
    except exceptions.NotFound:
        logger.critical(f"Dataset not found: {dataset_id}")
        return ["Dataset not found."]
        
    except Exception as e:
        logger.critical(f"An unexpected error occurred while listing tables: {e}")
        return ["An unexpected error occurred while listing tables."]


def generate_default_inventory_allocation_plan()-> str:
    """
    Calls the BQ stored procedure to generate the default inventory allocation plan
                        
    Returns:
        A success message or an error description.
    """
    logger.info(f"Utils.py: generate_inventory_allocation_plan")

    # Initialize the BigQuery Client
    client = bigquery.Client()
    
    # 1. Define the SQL CALL statement
    sql = f"CALL `capstone_ds.generate_inventory_allocation_plan`('INVENTORY_MANAGER_AGENT')"

    try:
        # 2. Execute the query
        query_job = client.query(sql)
        
        # 3. Wait for the procedure to finish
        query_job.result() 
        logger.info(f"Successfully ran generate_inventory_allocation_plan")
        return f"Successfully ran generate_inventory_allocation_plan"

    except Exception as e:
        logger.error(f"Error calling BQ procedure: {e}")
        return f"Failed to adjust allocation. Error: {str(e)}"


def generate_stock_transfer_order(omni_item_id: str)-> Optional[bigquery.table.RowIterator]:
    """
    Calls the BQ stored procedure to generate a stock transfer request

    Args:
        omni_item_id (str): ID of a specific product 
                        
    Returns:
        A recordset showing transfer order details
    """
    logger.info(f"Utils.py: generate_stock_transfer_order for item: {omni_item_id}")

    # Initialize the BigQuery Client
    client = bigquery.Client()
    
    # 1. Define the SQL CALL statement
    sql = f"CALL `capstone_ds.generate_stock_transfer_order`('{omni_item_id}','INVENTORY_MANAGER_AGENT')"

    try:
        # 2. Execute the query
        query_job = client.query(sql)
        
        # 3. Wait for the procedure to finish
        rows = query_job.result() 
        logger.info(f"Successfully generated stock transfer order for : {omni_item_id}")
        return rows

    except Exception as e:
        logger.error(f"Error calling BQ procedure: {e}")
        return f"Failed to adjust allocation. Error: {str(e)}"
  

def adjust_inventory_allocation(omni_item_id: str, at_store_allocation: int, at_warehouse_allocation: int)-> str:
    """
    Calls the BQ stored procedure to adjust the allocation

    Args:
        omni_item_id (str): ID of a specific product to update
        at_store_allocation (int): quantity of product to stock at store
        at_warehouse_allocation (int): quantity of product to stock at warehouse
                        
    Returns:
        A success message or an error description.
    """
    logger.info(f"Utils.py: adjust_inventory_allocation for item: {omni_item_id}, with store allocation: {at_store_allocation}, and warehouse allocation: {at_warehouse_allocation}")

    # Initialize the BigQuery Client
    client = bigquery.Client()
    
    # 1. Define the SQL CALL statement
    sql = f"CALL `capstone_ds.adjust_inventory_allocation`('{omni_item_id}',{at_store_allocation},{at_warehouse_allocation},'INVENTORY_MANAGER_AGENT')"

    try:
        # 2. Execute the query
        query_job = client.query(sql)
        
        # 3. Wait for the procedure to finish
        query_job.result() 
        logger.info(f"Successfully adjusted allocation for : {omni_item_id}")
        return f"Successfully adjusted allocation for : {omni_item_id}"

    except Exception as e:
        logger.error(f"Error calling BQ procedure: {e}")
        return f"Failed to adjust allocation. Error: {str(e)}"
    
    
def generate_report(reportType: str) -> Optional[bigquery.table.RowIterator]:
    """
    Generate report                     
    Returns:
        Optional[bigquery.table.RowIterator]: An iterator for the query
        results, or None if an error occurs.
    """
    logger.info(f"Inside tool generate_report, with reportType: {reportType}")
    
    reportSQL = ""
    if(reportType == 'AGENT_ACTIVITY_LOG_REPORT'):
        reportSQL = str(constants.AGENT_ACTIVITY_LOG_SQL)
    elif(reportType == 'AVAILABLE_TO_PROMISE_REPORT'):
        reportSQL = str(constants.AVAILABLE_TO_PROMISE_REPORT_SQL)
    elif(reportType == 'AVERAGE_RATE_OF_SALE_REPORT'):
        reportSQL = str(constants.AVERAGE_RATE_OF_SALE_REPORT_SQL)
    elif(reportType == 'DEMAND_FORECAST_REPORT'):
        reportSQL = str(constants.AVERAGE_RATE_OF_SALE_REPORT_SQL)
    elif(reportType == 'DEMAND_SIGNAL_LOG_REPORT'):
        reportSQL = str(constants.DEMAND_SIGNAL_LOG_SQL)
    elif(reportType == 'FILL_RATE_REPORT'):
        reportSQL = str(constants.FILL_RATE_REPORT_SQL)
    elif(reportType == 'FLEET_ITEMS_DELIVERY_SUMMARY_REPORT'):
        reportSQL = str(constants.FLEET_ITEMS_DELIVERY_SUMMARY_REPORT_SQL)
    elif(reportType == 'FLEET_USAGE_SUMMARY_REPORT'):
        reportSQL = str(constants.FLEET_USAGE_SUMMARY_REPORT_SQL)
    elif(reportType == 'INVENTORY_AGING_REPORT'):
        reportSQL = str(constants.INVENTORY_AGING_REPORT_SQL)
    elif(reportType == 'INVENTORY_ALLOCATION_REPORT'):
        reportSQL = str(constants.INVENTORY_ALLOCATION_REPORT_SQL)
    elif(reportType == 'INVENTORY_RECONCILIATION_REPORT'):
        reportSQL = str(constants.INVENTORY_RECONCILIATION_REPORT_SQL)
    elif(reportType == 'LOCATION_BASED_TRANSFER_VOLUME_SUMMARY_REPORT'):
        reportSQL = str(constants.LOC_BASED_TRANSFER_VOLUME_SUMMARY_REPORT_SQL)
    elif(reportType == 'LOW_STOCK_REPORT'):
        reportSQL = str(constants.LOW_STOCK_REPORT_SQL)
    elif(reportType == 'ON_HAND_INVENTORY_REPORT'):
        reportSQL = str(constants.ON_HAND_INVENTORY_REPORT_SQL)
    elif(reportType == 'ON_HAND_LOC_INVENTORY_REPORT'):
        reportSQL = str(constants.ON_HAND_LOC_INVENTORY_REPORT_SQL)
    elif(reportType == 'OUT_OF_STOCK_REPORT'):
        reportSQL = str(constants.OUT_OF_STOCK_REPORT_SQL)
    elif(reportType == 'PURCHASE_ORDER_STATUS_REPORT'):
        reportSQL = str(constants.PURCHASE_ORDER_STATUS_REPORT_SQL)
    elif(reportType == 'REORDER_POINT_REPORT'):
        reportSQL = str(constants.REORDER_POINT_REPORT_SQL)
    elif(reportType == 'STOCK_MOVEMENT_SUMMARY_REPORT'):
        reportSQL = str(constants.STOCK_MOVEMENT_SUMMARY_REPORT_SQL)
    elif(reportType == 'SUGGESTED_REORDER_REPORT'):
        reportSQL = str(constants.SUGGESTED_REORDER_REPORT_SQL)
    elif(reportType == 'STOCK_TRANSFER_FULFILLMENT_REPORT'):
        reportSQL = str(constants.STOCK_TRANSFER_FULFILLMENT_REPORT_SQL)
    elif(reportType == 'UNDER_PERFORMING_INVENTORY_REPORT'):
        reportSQL = str(constants.UNDER_PERFORMING_INVENTORY_REPORT_SQL)
    elif(reportType == 'WEEKS_OF_SUPPLY_REPORT'):
        reportSQL = str(constants.WEEKS_OF_SUPPLY_REPORT_SQL)
    elif(reportType == 'WEIGHTED_LEAD_TIME_REPORT'):
        reportSQL = str(constants.WEIGHTED_LEAD_TIME_REPORT_SQL)

    try:
        bq_client = get_bq_client()

        if not bq_client:
            logger.critical("BigQuery client is not available.")
            return None
 
        rows = bq_client.query_and_wait(reportSQL)  # Make an API request.
        return rows
    except exceptions.GoogleAPICallError as e:
        logger.critical(f"BigQuery API call failed: {e}")
        return None
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        return None
