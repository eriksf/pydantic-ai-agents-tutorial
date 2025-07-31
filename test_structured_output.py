import os

import logfire
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()
model_name = os.getenv('MODEL_NAME')
base_url = os.getenv('BASE_URL')
api_key = os.getenv('API_KEY')

# 'if-token-present' means nothing will be sent (and the example will work) if you don't
# have logfire configured
logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()


class MyModel(BaseModel):
    city: str
    country: str


class ResponseModel(BaseModel):
    continent_name: str
    country_name: str
    capital_name: str
    has_river: bool
    has_sea: bool
    weather: str = Field(description="Weather over the year, explain in 10 words only")


#model = os.getenv("PYDANTIC_AI_MODEL", "openai:gpt-4o")
model = OpenAIModel(
    model_name,
    provider=OpenAIProvider(base_url=base_url, api_key=api_key)
)
print(f"Using model: {model}")
#agent = Agent(model, output_type=MyModel)
agent = Agent(model, output_type=ResponseModel)


if __name__ == "__main__":
    #result = agent.run_sync("The windy city in the US of A.")
    result = agent.run_sync("Tell me about Saudi Arabia")
    print(result.output)
    print(result.usage())
