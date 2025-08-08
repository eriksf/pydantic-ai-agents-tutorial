import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

# Load environment variables from .env file
load_dotenv()

# Retrieve the variables from the environment
model_name = os.getenv('MODEL_NAME')
base_url = os.getenv('BASE_URL')
api_key = os.getenv('API_KEY')

# Create an instance of OpenAIModel using the loaded variables
vision_model = GoogleModel(
    model_name,
    provider=GoogleProvider(api_key=api_key),
)

agent_vision = Agent(
    model=vision_model,
    output_retries=3,
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
