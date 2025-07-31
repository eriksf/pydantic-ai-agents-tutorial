# NOTE: If you encounter scipy runtime errors, install this specific version:
# pip install scipy==1.14.1

import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from smolagents import PythonInterpreterTool

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

python_interpreter = PythonInterpreterTool(authorized_imports=["odf", "pathlib", "datetime"])

agent = Agent(
    model=model,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze the user request carefully and provide structured responses "
        "using suitable tools to fullfill the request. "
        "You have access to multiple tools."
    ),
    output_retries=3
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

request_msg = "Tell me the current date and time"
response = agent.run_sync(request_msg)
print(response.output)
print(response.usage())

#answer should be = 4.50906873475019
request_msg = "What is the area of a square that has a length of 2.123456789 cm, use python coding to calculate accurately"
response = agent.run_sync(request_msg)
print(response.output)
print(response.usage())
