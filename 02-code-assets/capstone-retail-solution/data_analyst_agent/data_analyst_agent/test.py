# Copyright 2026 Google LLC
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
# limitations under the License.§

"""Script to test the agent deployed at Agent Engine"""

import pprint
import logging
import sys
import vertexai
from vertexai import agent_engines
from google.api_core import exceptions as google_exceptions
from . import constants

# Setup logging for better visibility into errors
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def initialize_vertex():
    """Initializes Vertex AI with basic validation."""
    if constants.DEPLOYED_AGENT_RESOURCE_URI == 'deployed_agent_resource_uri_not_set':
        logger.error("DEPLOYED_AGENT_RESOURCE_URI is not set in constants.py")
        sys.exit(1)
        
    try:
        vertexai.init(project=constants.PROJECT_ID, location=constants.LOCATION)
    except Exception as e:
        logger.error(f"Failed to initialize Vertex AI: {e}")
        sys.exit(1)

def get_remote_app():
    """Fetches the agent with error handling for resource availability."""
    try:
        return agent_engines.get(constants.DEPLOYED_AGENT_RESOURCE_URI)
    except google_exceptions.NotFound:
        logger.error(f"Agent not found at URI: {constants.DEPLOYED_AGENT_RESOURCE_URI}")
    except google_exceptions.PermissionDenied:
        logger.error("Permission denied. Check your IAM roles (Vertex AI User).")
    except Exception as e:
        logger.error(f"Unexpected error retrieving agent: {e}")
    return None

def get_agent_response(remote_app, question, user_id, session):
    """Streams response with specific handling for network timeouts."""
    print(f"QUESTION: {question}\n" + "="*48)
    try:
        # We wrap the generator in a try block to catch streaming interruptions
        for event in remote_app.stream_query(
            user_id=user_id,
            session_id=session["id"],
            message=question,
        ):
            pprint.pp(event)
    except google_exceptions.DeadlineExceeded:
        logger.warning("The request timed out. Agent Engine took too long to respond.")
    except google_exceptions.ServiceUnavailable:
        logger.error("Agent Engine service is currently unavailable. Try again later.")
    except Exception as e:
        logger.error(f"An error occurred during streaming: {e}")
    print("="*48)

if __name__ == "__main__":
    initialize_vertex()
    
    user_id = "data-engineer"
    question_list = [
        "Show me the tables in BQ dataset capstone_ds",
        "Show me the inventory of product with omni_item_id of 'FRWW4543AS'"
    ]

    remote_app = get_remote_app()
    
    if remote_app:
        try:
            # Create session and handle potential auth/network issues
            session = remote_app.create_session(user_id=user_id)
            logger.info(f"Connected - Session ID: {session['id']}")

            for question in question_list:
                get_agent_response(remote_app, question, user_id, session)

        except Exception as e:
            logger.error(f"Failed to establish or maintain session: {e}")
    else:
        logger.error("Could not initialize remote app. Exiting.")

    