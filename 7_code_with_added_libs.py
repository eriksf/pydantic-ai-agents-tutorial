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

class FormatedTime(BaseModel):
    year: str
    month: str = Field(description="Write month with 3 letters only, example: Jan, Feb, Mar ...etc")
    day_numeric: str = Field(description="Write day as numeric value")
    day_name: str = Field(description="Write day as name, example: Sunday, Monday, Tuesday...etc")
    time: str = Field(description="Write time in following format hours:minutes:PM/AM")
    timezone: str = Field(description="timezone refrenced to GMT, exmaple GMT+1, GMT-2")
    


agent = Agent(
    model=model,
    output_type=FormatedTime,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses"
        "you have access to multiple tools, use suitble tools to fullfil user request"
    ),
    max_result_retries = 3
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


# asking for timezone will make the llm try to install some libraries 

request_msg = "get the current date, time, day name and local timezone of your environment"
response = agent.run_sync(request_msg)
print(response.output.model_dump_json(indent=1))
print(response.usage())
