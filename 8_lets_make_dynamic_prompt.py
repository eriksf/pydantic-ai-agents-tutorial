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


agent = Agent(
    model=model,
    result_retries = 3,
)

@agent.tool_plain
def run_python_code(code: str, libraries: Optional[List] = None) -> str:
    """
    Run python code in a sandboxed environment.
    parameter code: The code to run. send it as string
    parameter libraries: The libraries to use, it will be installed with pip. send list of strings to represnet needed libraries
    return: The output of the code. don't forget to add print to your code to print the final result
    """
    with SandboxSession(image="python:3.14.0a3", lang="python", keep_template=True, verbose=True) as session:
        result = session.run(code, libraries)
        return result.text


@agent.system_prompt
def add_user_command() -> str:  
    return sys.argv[1]


# Check if any additional arguments were passed
# arg[0] is the application script itself
# arg[1] is the input prompt 
# exmaple: python3 8_lets_make_dynamic_prompt.py "calculate 1.11111*2.222222*3.33333/5.555555"
# exmaple: python3 8_lets_make_dynamic_prompt.py "find local ip address using code"
if len(sys.argv) == 2:
    print(sys.argv[1])
else:
    print("No command provided. please run the script as \n python3 8_lets_make_dynamic_prompts.py \"command details - insert your prompt here\"")
    exit(0)


response = agent.run_sync("You are an intelligent assistant.")
print(response.data)
