import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

# Load environment variables from .env file
load_dotenv()

# Retrieve the variables from the environment
model_name = os.getenv('MODEL_NAME')
base_url = os.getenv('BASE_URL')
api_key = os.getenv('API_KEY')

# Create an instance of OpenAIModel using the loaded variables
model = GoogleModel(
    model_name,
    provider=GoogleProvider(api_key=api_key),
)


class ResponseModel(BaseModel):
    """Automatic Structured response with metadata."""
    continent_name: str
    country_name: str
    capital_name: str
    has_river: bool
    has_sea: bool
    weather: str = Field(description="Weather over the year in 10 words only")


agent = Agent(
    model=model,
    output_type=ResponseModel,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses."
    ),
    output_retries=3
)

agent2 = Agent(
    model=model,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze input json list carefully and provide markdown table"
        "Be concise and don't write anything else except the markdown table"
        "use bold tags for headers"
    ),
)

data_list = []

response = agent.run_sync("tell me about Egypt")
data_list.append(response.output.model_dump_json(indent=2))

response = agent.run_sync("tell me about France")
data_list.append(response.output.model_dump_json(indent=2))

response = agent.run_sync("tell me about China")
data_list.append(response.output.model_dump_json(indent=2))

response = agent.run_sync("tell me about Australia")
data_list.append(response.output.model_dump_json(indent=2))

response_MDtable = agent2.run_sync(str(data_list))
print(response_MDtable.output)
print(response_MDtable.usage())
