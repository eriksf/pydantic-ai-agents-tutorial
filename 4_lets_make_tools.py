from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import subprocess
from dotenv import load_dotenv
import os

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

agent = Agent(
    model=model,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses and use suitble tools to fullfil user request"
    ),
    result_retries = 1
)


@agent.tool_plain
def get_current_ip_address() -> str:
    """
    Get public IP address using ifconfig.me website
    return: current ip address
    """
    command = ['curl','ifconfig.me']
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    return result.stdout
    
@agent.tool_plain
def get_ip_info_with_whois(ip_address_to_track:str ="0.0.0.0") -> str:
    """
    Get information about the IP address using Whois
    args:
     ip_address_to_track(str): the ip you want to track with whois request
    return: whois record for the requested IP
    """
    command = ['whois', ip_address_to_track]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    return result.stdout




data_list = []

response = agent.run_sync("using all tools you have access to, can you guess which city I live in now?")
print(response.output)
print(response.usage())
