from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
from pathlib import Path

#import os and base64 to open images and send them as string encoded in base64
import os
import base64


vision_model = OllamaModel( model_name='minicpm-v')


class ImageLoaderBase64:
    message_with_image = []

    def __init__(self, user_request:str, image_file_path: str):
        with open(image_file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
            prepare_image_inside_message = [
                    {
                        "type": "text",
                        "text": f"{user_request}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            self.encoded_message_with_image = prepare_image_inside_message

agent_vision = Agent(
    model=vision_model,
    result_retries = 3,
    system_prompt = "You are smart vision agent with text extract skills",
)

image_request_1 = ImageLoaderBase64(
    user_request="extract all text",
    image_file_path="./11_vision_sample_data/stv_jbs.png"
    )

result = agent_vision.run_sync(image_request_1.encoded_message_with_image)
print(result.data)


image_request_2 = ImageLoaderBase64(
    user_request="how much should I pay for this bill?",
    image_file_path="./11_vision_sample_data/grocery_test.png"
    )

result = agent_vision.run_sync(image_request_2.encoded_message_with_image)
print(result.data)


