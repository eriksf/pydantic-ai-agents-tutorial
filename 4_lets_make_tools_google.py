import os
import subprocess

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

agent = Agent(
    model=model,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze the user request carefully and provide structured responses using suitable tools to fullfill the user request."
    ),
    output_retries=1
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

response = agent.run_sync("Using all the tools you have access to, can you guess which city I am in now?")
print(response.output)
print(response.usage())
