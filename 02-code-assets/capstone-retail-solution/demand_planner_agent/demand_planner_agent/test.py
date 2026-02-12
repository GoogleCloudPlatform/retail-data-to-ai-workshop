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
import vertexai
from vertexai import agent_engines
import constants


vertexai.init(
    project=constants.PROJECT_ID,
    location=constants.LOCATION
)

if constants.DEPLOYED_AGENT_RESOURCE_URI == 'deployed_agent_resource_uri_not_set':
    print("DEPLOYED_AGENT_RESOURCE_URI is not set.")
    raise "DEPLOYED_AGENT_RESOURCE_URI is not set."


def get_remote_app():
    return agent_engines.get(constants.DEPLOYED_AGENT_RESOURCE_URI)

def get_agent_response(remote_app,question,user_id, session):
    for event in remote_app.stream_query(
        user_id=user_id,
        session_id=session["id"],
        message=question,
    ):
        pprint.pp(event)


if __name__ == "__main__":

    question_list = [
        "Can you show me the forecast for omni_item_id 'LRDCS2603S' for '2026-02-02' for location_id 'CHI-IL-ST'?",
        "I see a demand SURGE. Can you adjust the forecast for this omni_item_id 'LRDCS2603S', for a SURGE?",
        "Can you show me the forecast for omni_item_id 'LRDCS2603S' for '2026-02-02' for location_id 'CHI-IL-ST' again?" ]
    user_id = "demand-planner"
    remote_app = get_remote_app()
    session = remote_app.create_session(user_id=user_id)
    print(f"Connected to Agent Engine - URI: {constants.DEPLOYED_AGENT_RESOURCE_URI} as user {user_id} and session {session['id']}")

    for question in question_list:
       print(f"QUESTION: {question}")
       print(f"================================================")
       get_agent_response(remote_app,question,user_id,session) 
       print(f"================================================")

    