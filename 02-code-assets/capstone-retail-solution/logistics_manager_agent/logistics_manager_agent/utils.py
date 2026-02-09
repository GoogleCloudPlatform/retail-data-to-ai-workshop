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


def generate_stock_transfer_order(omni_item_id: str)-> Optional[bigquery.table.RowIterator]:
    """
    Calls the BQ stored procedure to generate a stock transfer order

    Args:
        omni_item_id: str - product unique identifier
              
    Returns:
        A recordset showing transfer order details
    """
    logger.info(f"Utils.py: generate_stock_transfer_order")

    # Initialize the BigQuery Client
    client = bigquery.Client()
    
    # 1. Define the SQL CALL statement
    sql = f"CALL `capstone_ds.generate_stock_transfer_order`('{omni_item_id}','LOGISTICS_MANAGER_AGENT')"

    try:
        # 2. Execute the query
        query_job = client.query(sql)
        
        # 3. Wait for the procedure to finish
        rows = query_job.result() 
        logger.info(f"Successfully generated stock transfer order")
        return rows

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
