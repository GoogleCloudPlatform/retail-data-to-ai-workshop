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

"""Defines agent """

from google.adk.agents.llm_agent import Agent
from . import constants, system_instructions, tools
from google.genai import types
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Inside the inventory manager agent")

root_agent = Agent(
    model=constants.MODEL,
    name="inventory_manager_agent",
    description="An agent that can answer inventory related questions, run inventory reports, run reconciliation, allocation adjustment processes and more.",
    instruction=system_instructions.INVENTORY_MANAGER_AGENT_SYSTEM_INSTRUCTIONS,
    tools=[
        tools.sql_generator,
        tools.sql_executor,
        tools.report_generator,
        tools.inventory_allocation_adjustor,
        tools.default_inventory_allocation_plan_generator,
        tools.stock_transfer_request_generator
    ],    
    generate_content_config=types.GenerateContentConfig(
        temperature=constants.GENERATION_CONFIGURATION_TEMPERATURE,
        safety_settings=constants.SAFETY_SETTINGS, 
        top_p=constants.GENERATION_CONFIGURATION_TOP_P,
        top_k=constants.GENERATION_CONFIGURATION_TOP_K,
        max_output_tokens=constants.GENERATION_CONFIGURATION_MAX_OUTPUT_TOKENS
    )
)
