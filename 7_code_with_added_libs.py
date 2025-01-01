from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel

# import safe sandbox
from typing import Optional, List
from llm_sandbox import SandboxSession


model = OllamaModel( model_name='Replete-LLM-V2.5-Qwen-32b-Q5_K_S')


class FormatedTime(BaseModel):
    year: str
    month: str = Field(description="Write month with 3 letters only, example: Jan, Feb, Mar ...etc")
    day_numeric: str = Field(description="Write day as numeric value")
    day_name: str = Field(description="Write day as name, example: Sunday, Monday, Tuesday...etc")
    time: str = Field(description="Write time in following format hours:minutes:PM/AM")
    timezone: str = Field(description="timezone refrenced to GMT, exmaple GMT+1, GMT-2")
    


agent = Agent(
    model=model,
    result_type=FormatedTime,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses"
        "you have access to multiple tools, use suitble tools to fullfil user request"
    ),
    result_retries = 3
)

@agent.tool_plain
def run_python_code(code: str, libraries: Optional[List] = None) -> str:
    """
    Run python code in a sandboxed environment.
    args:
     code(str): The code to run. send it as string
     libraries(list of str): The libraries to use, it will be installed with pip. send list of strings to represnet needed libraries
    return: The output of the code. don't forget to add print to your code to print the final result
    """
    with SandboxSession(image="python:3.14.0a3", lang="python", keep_template=True, verbose=True) as session:
        result = session.run(code, libraries)
        return result.text


# asking for timezone will make the llm try to install some libraries 

request_msg = "get the current date, time, day name and local timezone of your environment"
response = agent.run_sync(request_msg)
print(response.data.model_dump_json(indent=2))
