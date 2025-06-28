# NOTE: If you encounter scipy runtime errors, install this specific version:
# pip install scipy==1.14.1

from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import sys
from transformers.agents import PythonInterpreterTool
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
    max_result_retries = 3,
)


@agent.tool_plain
def execute_python_code(code_string:str, libs:list[str] = ["odf", "pathlib", "datetime"]):
    """
    Send the python code as input string you can use it as well for math and print the results
    note: Don't use any library need to be installed with pip 
    args:
     code(str): The code to run. send it as string
     libs(List[str]): list of libraries needed to be used for exmaple ["odf", "pathlib", "datetime"]
    return: code execution results as text
    """
    python_interpreter = PythonInterpreterTool(authorized_imports=libs)

    try:
        result = python_interpreter.forward(code_string)
        print(f"code run reult = {result}")
        return result
    except Exception as e:
        return f"Python code is wrong, send valid code, error code : {str(e)}"

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
print(response.output)
