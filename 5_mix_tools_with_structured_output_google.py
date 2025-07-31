import os
import subprocess

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
    continent_location: str 
    country_location: str
    city_location: str
    internet_provider: str = Field(description="What is the name of internet service provider?")
    ip_address_v4: str = Field(description="What is the IP address (version 4) - IPv4?")
    ip_address_v6: str = Field(description="what is the IP address (version 6) - IPv6?")


agent = Agent(
    model=model,
    output_type=ResponseModel,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze the user request carefully and provide structured responses using suitable tools to fullfill the user request."
    ),
    output_retries=5
)

@agent.tool_plain
def get_current_ip_address() -> str:
    """Get public IP address using ifconfig.me website"""
    command = ['curl','ifconfig.me']
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    return result.stdout
    
@agent.tool_plain
def get_ip_info_with_whois(ip_to_track:str) -> str:
    """Get information about the IP address using Whois"""
    command = ['whois', ip_to_track]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    return result.stdout


data_list = []

response = agent.run_sync("Can you guess which city I am in now?")
print(response.output.model_dump_json(indent=1))
print(response.usage())
