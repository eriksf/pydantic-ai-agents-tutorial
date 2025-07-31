import os

from dotenv import load_dotenv
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

agent1 = Agent(
    model=model,
    system_prompt='You are a helpful customer support agent. Be concise and friendly.'
)
response = agent1.run_sync("Count from 1 to 50 separated by - and don't write anything else.")
print(response.output)
print(response.usage())
