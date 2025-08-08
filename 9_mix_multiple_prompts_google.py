# run throught the terminal with one of bellow exmaples

import os

# lets get the input args
import sys

from dotenv import load_dotenv
from pydantic_ai import Agent

# from pydantic_ai.models.ollama import OllamaModel  # Not available in this version
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
# Lets mix 3 prompts, 1st one in the agents constructor
# 2nd prompt will be added through add_1st_command_to_the_prompt()
# 3rd prompt will be added through add_2nd_command_to_the_prompt()

agent = Agent(
    model=model,
    output_retries=3,
    system_prompt = "You are -Oro AI Agent- always start your reply with *I'm Oro, I will help you:*",
)


@agent.system_prompt
def add_1st_command_to_the_prompt() -> str:
    return sys.argv[1]

@agent.system_prompt
def add_2nd_command_to_the_prompt() -> str:
    return sys.argv[2]

# Check if any additional arguments were passed
# arg[0] is the application script itself
# arg[1] is the 1st input prompt
# arg[2] is the 2nd input prompt
# example1: python3 9_mix_multiple_prompts.py "hello I'm abdallah" "can you guess what language can i speak"
# example2: python3 9_mix_multiple_prompts.py "Can you guess where I'm if I'm inside that tallest building in the world" "provide json formated answer include country, city"

if len(sys.argv) == 3:
    print(sys.argv[1])
else:
    print("Not all commands provided. Please run the script as \n python 8_lets_make_dynamic_prompts.py \"command details 1 \"  \"command details 2\"")
    exit(1)


response = agent.run_sync("You are an intelligent assistant.")
print(response.output)


