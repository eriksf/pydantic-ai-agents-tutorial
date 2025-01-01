from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
import subprocess

model = OllamaModel( model_name='Replete-LLM-V2.5-Qwen-32b-Q5_K_S')


class ResponseModel(BaseModel):
    """Automatic Structured response with metadata."""
    continent_location: str 
    country_location: str
    city_location: str
    internet_provider: str = Field(description="what is the name of internet service provider")
    ip_address_v4: str = Field(description="what is IP address (version 4) - IPv4")
    ip_address_v6: str = Field(description="what is IP address (version 6) - IPv6")


agent = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses and use suitble tools to fullfil user request"
    ),
    result_retries = 3
)

@agent.tool_plain
def get_current_ip_address() -> str:
    """Get public IP address using ifconfig.me website"""
    command = ['curl','ifconfig.me']
    result = subprocess.run(command, capture_output=True, text=True)
    #print(result.stdout)
    return result.stdout
    
@agent.tool_plain
def get_ip_info_with_whois(ip_to_track) -> str:
    """Get information about the IP address using Whoio"""
    command = ['whois', ip_to_track]
    result = subprocess.run(command, capture_output=True, text=True)
    #print(result.stdout)
    return result.stdout


data_list = []

response = agent.run_sync("can you guess where I am now?")
print(response.data.model_dump_json(indent=2))

# Uncomment to debug :)
print("--------------Debug----------------\n\n\n")
print(str(response.usage()))
# print(response.all_messages())