# NOTE: If you encounter scipy runtime errors, install this specific version:
# pip install scipy==1.14.1

from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
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

python_interpreter = PythonInterpreterTool(authorized_imports=["odf", "pathlib", "datetime"])

agent = Agent(
    model=model,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses"
        "you have access to multiple tools, use suitble tools to fullfil user request"
    ),
    max_result_retries = 3
)

@agent.tool_plain
def execute_python_code(code_string:str):
    """
    Send the python code as input string you can use it as well for math and print the results
    note: Don't use any library need to be installed with pip 
    args:
     code(str): The code to run. send it as string
    return: code execution results as text
    """
    try:
        result = python_interpreter.forward(code_string)
        return result
    except Exception as e:
        return f"Python code is wrong, send valid code, error code : {str(e)}"

request_msg = "tell me current date and time"
response = agent.run_sync(request_msg)
print(response.output)
print(response.usage())

#answer should be = 4.50906873475019
request_msg = "what is the area of square has length of 2.123456789 cm, use python coding to calculate accuratly"
response = agent.run_sync(request_msg)
print(response.output)
print(response.usage())
