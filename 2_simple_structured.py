import os

import mlflow
import mlflow.openai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

mlflow.set_tracking_uri(uri="http://localhost:8775")
mlflow.set_experiment("Ollama")
mlflow.openai.autolog()

# Load environment variables from .env file
load_dotenv()

# Retrieve the variables from the environment
model_name = os.getenv('MODEL_NAME')
base_url = os.getenv('BASE_URL')
api_key = os.getenv('API_KEY')

# Create an instance of OpenAIModel using the loaded variables
model = OpenAIModel(
    model_name,
    provider=OpenAIProvider(base_url=base_url, api_key=api_key),
)


class ResponseModel(BaseModel):
    continent_name: str
    country_name: str
    capital_name: str
    has_river: bool
    has_sea: bool
    weather: str = Field(description="Weather over the year, explain in 10 words only")


agent = Agent(
    model=model,
    output_type=ResponseModel,
    #system_prompt=(
    #    "You are an intelligent research agent. "
    #    "Analyze user request carefully and provide structured responses. "
    #    "You must use function call"
    #),
    output_retries=3,

)


response = agent.run_sync("tell me about Egypt")
print(response.output.model_dump_json(indent=1))
print(response.usage())

#response = agent.run_sync("tell me about France")
#print(response.output.model_dump_json(indent=2))
#print(response.usage())
#
#response = agent.run_sync("tell me about China")
#print(response.output.model_dump_json(indent=3))
#print(response.usage())
#
#response = agent.run_sync("tell me about Australia")
#print(response.output.model_dump_json(indent=4))
#print(response.usage())
#
#response = agent.run_sync("tell me about Moroco")
#print(response.output.model_dump_json(indent=4))
#print(response.usage())
#
#response = agent.run_sync("tell me about Saudi Arabia")
##print(response.output.model_dump_json(indent=4))
#print(response.usage())
