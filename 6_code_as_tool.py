from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel

# import safe sandbox 
from llm_sandbox import SandboxSession


model = OllamaModel( model_name='Replete-LLM-V2.5-Qwen-32b-Q5_K_S')


agent = Agent(
    model=model,
    system_prompt=(
        "You are an intelligent research agent. "
        "Analyze user request carefully and provide structured responses"
        "you have access to multiple tools, use suitble tools to fullfil user request"
    ),
    result_retries = 3
)

@agent.tool_plain
def execute_python_code(code) -> str:
    """
    Send the python code as input string you can use it as well for math and print the results
    note: Don't use any library need to be installed with pip 
    args:
     code(str): The code to run. send it as string
    return: code execution results as text
    """

    with SandboxSession(image="python:3.14.0a3", lang="python", keep_template=True) as session:
        result = session.run(code)
        return(result.text)



request_msg = "tell me current date and time"
response = agent.run_sync(request_msg)
print(response.data)

#answer should be = 4.50906873475019
request_msg = "what is the area of square has length of 2.123456789 cm, use coding to calculate accuratly"
response = agent.run_sync(request_msg)
print(response.data)
