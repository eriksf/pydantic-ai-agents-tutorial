from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pathlib import Path
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the variables from the environment
model_name = os.getenv('MODEL_NAME')
base_url = os.getenv('BASE_URL')
api_key = os.getenv('API_KEY')

# Create an instance of OpenAIModel using the loaded variables
vision_model = OpenAIModel(
    model_name,
    provider=OpenAIProvider(base_url=base_url, api_key=api_key),
)

agent_vision = Agent(
    model=vision_model,
    result_retries=3,
    system_prompt="You are smart vision agent with text extract skills",
)

print("--------Testing with grocery bill image ---------")
# Read the PNG image file
image_path = Path("./11_vision_sample_data/grocery_test.png")
if image_path.exists():
    image_data = image_path.read_bytes()
    
    # Run agent with text and image
    result = agent_vision.run_sync([
        "how much should I pay for this bill?",
        BinaryContent(data=image_data, media_type='image/png')
    ])
    print(result.output)
else:
    print("Warning: grocery_test.png not found")


