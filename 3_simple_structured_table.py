from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel

# example using tabbyAPI with exl2 models
model = OpenAIModel(
    'llama3.1:8b-instruct-q8_0',
    base_url='http://localhost:11434/v1',
    api_key='tabbyAPI',
)

class ResponseModel(BaseModel):
    """Automatic Structured response with metadata."""
    continent_name: str
    country_name: str
    capital_name: str
    has_river: bool
    has_sea: bool
    weather: str = Field(description="Weather over the year")


agent = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses."
    ),
    result_retries = 3
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
data_list.append(response.data.model_dump_json(indent=2))

response = agent.run_sync("tell me about France")
data_list.append(response.data.model_dump_json(indent=2))

response = agent.run_sync("tell me about China")
data_list.append(response.data.model_dump_json(indent=2))

response = agent.run_sync("tell me about Australia")
data_list.append(response.data.model_dump_json(indent=2))

response_MDtable = agent2.run_sync(str(data_list))
print(response_MDtable.data)