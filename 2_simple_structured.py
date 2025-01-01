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
    """Automatic Structured response with """
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
)

response = agent.run_sync("tell me about Egypt")
print(response.data.model_dump_json(indent=1))

response = agent.run_sync("tell me about France")
print(response.data.model_dump_json(indent=2))

response = agent.run_sync("tell me about China")
print(response.data.model_dump_json(indent=3))

response = agent.run_sync("tell me about Australia")
print(response.data.model_dump_json(indent=4))