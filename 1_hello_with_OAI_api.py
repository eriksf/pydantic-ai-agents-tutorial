from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel

# example using tabbyAPI with exl2 models
model = OpenAIModel(
    'Replete-LLM-V2.5-Qwen-32b-Q5_K_S',
    base_url='http://localhost:11434/v1',
    api_key='your-super-secret-key',
)

agent1 = Agent(
    model=model,
    system_prompt="You are a helpful customer support agent. Be concise and friendly."
)

# Example usage of basic agent
response = agent1.run_sync("What is the capital of Egypt")
print(response.data)
