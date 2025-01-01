# run throught the terminal with one of bellow exmaples 

from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel

# import safe sandbox
from typing import Optional, List
from llm_sandbox import SandboxSession

# lets get the input args
import sys

model = OllamaModel( model_name='Replete-LLM-V2.5-Qwen-32b-Q5_K_S')

# Lets mix 3 prompts, 1st one in the agents constructor
# 2nd prompt will be added through add_1st_command_to_the_prompt()
# 3rd prompt will be added through add_2nd_command_to_the_prompt()

agent = Agent(
    model=model,
    result_retries = 3,
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
    print("No all commands provided. please run the script as \n python3 8_lets_make_dynamic_prompts.py \"command details 1 \"  \"command details 2\"")
    exit(0)


response = agent.run_sync("You are an intelligent assistant.")
print(response.data)


