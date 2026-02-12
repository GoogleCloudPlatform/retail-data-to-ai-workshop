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

"""Defines helper for data Q&A."""


from vertexai.generative_models import GenerativeModel
from . import utils, constants
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def sql_generator(prompt: str) -> str:
    """
    Takes a natural language prompt, generates a BigQuery SQL query using a
    generative model, executes the query, and returns the results in a
    markdown table.
    """
    logger.info("Inside sql_generator")

    try:
 
        model = GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(
            prompt, generation_config=constants.GENERATION_CONFIGURATION
        )
        sql_query = response.text
        logger.info(f"Gemini's SQL Response: {sql_query}")
        
        return sql_query

    except Exception as e:
        error_message = f"An error occurred: {e}"
        logger.critical(error_message)
        return error_message
    
def sql_executor(sql_query: str) -> str:
    """
    Takes the sql query, executes the query, and returns the results in a
    markdown table.
    """
    logger.info(f"Inside sql_executor & executing query: {sql_query}")

    try:
        sql_execution_results = utils.get_query_results_markdown(sql_query)
        #sql_execution_results = utils.get_query_results(sql_query)
        logger.info(f"sql_execution_results: {sql_execution_results}")
        return sql_execution_results

    except Exception as e:
        error_message = f"An error occurred: {e}"
        logger.critical(error_message)
        return error_message