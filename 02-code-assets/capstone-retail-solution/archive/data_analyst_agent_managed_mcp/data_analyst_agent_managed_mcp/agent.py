# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import tools, constants
from google.adk.agents import LlmAgent

bigquery_mcp_toolset = tools.get_bigquery_mcp_toolset()

root_agent = LlmAgent(
    #model='gemini-3-pro-preview
    model='gemini-2.5-pro',
    name='Data_Analyst_Agent',
    instruction=f"""
                You are an expert data analyst that can author BigQuery SQL queries and fetch data based on natual 
                language questions asked. 
                Tools at your disposal:
                    **BigQuery MCP toolset:** This allows you to access data in BigQuery.
                Project scope:
                    Run all queries against the GCP project {constants.PROJECT_ID}
                BigQuery dataset scope:
                    Run all queries against the BigQuery datasets in scope: {constants.BQ_DATASETS_IN_SCOPE}
                Greeting:
                    On start - greet the user with - 
                    'Hello, I am a data analyst agent. \n
                    You can ask me questions and I will make a best effort to answer accurately.\n 
                    1. You can ask questions about data; My data access scope is limited to the BigQuery dataset capstone_ds.
                    2. You can ask me questions about the BigQuery resources I have access to such as 
                    dataset metadata, table metadata, table relationships, stored procedures and such.'
                
            """,
    tools=[bigquery_mcp_toolset]
)
