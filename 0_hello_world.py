from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel

model = OllamaModel( model_name='llama3.1:8b-instruct-q8_0')

agent1 = Agent(
    model=model,
    system_prompt="You are a helpful customer support agent. Be concise and friendly."
)

# Example usage of basic agent
response = agent1.run_sync("What is the capital of Egypt")
print(response.data)
