from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
from pathlib import Path

#import os and base64 to open images and send them as string encoded in base64
import os
import base64

# Note for ollama both "minicpm-v" and "llama3.2-vision:latest" can't be used with pydantic tool calling, so we can't use it directly to call functions and format text
# therefor I will use 2 models, one for OCR and one for make structured data

# vision_model = OllamaModel( model_name='minicpm-v')
vision_model = OllamaModel( model_name='llama3.2-vision')
analysis_model = OllamaModel( model_name='Replete-LLM-V2.5-Qwen-32b-Q5_K_S')


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


class Item(BaseModel):
    item_name: str = Field(description="Item name")
    item_qu: str = Field(description="Quantity of item in the bill")
    item_price: str = Field(description="Price in $")

class BillSummary(BaseModel):
    items: list[Item] = Field(default_factory=list, description="List of items in the bill")
    subtotal: float = Field(description="Subtotal of the bill")
    tax: float = Field(description="taxes if applied bill")
    total: float = Field(description="total of the bill")
    bill_date: str = Field(description="bill issue date")
    bill_time: str = Field(description="bill issue time")

agent_vision = Agent(
    model=vision_model,
    result_retries = 3,
    system_prompt = "You are smart vision ai assistant, you will extract all text in any given image",
)

agent_analysis = Agent(
    model=analysis_model,
    result_type=BillSummary,
    result_retries = 3,
    system_prompt = "You are smart analysis agent, take the extracted OCR data, extract items and convert it to structured report",
)

image_request = ImageLoaderBase64(
    # user_request="list down in entries, start the entry with item name then create bullet points for quantity, price per item. add another entry for sub-total, tax value, total",
    user_request="for the following receipt, do step by step extract all text and describe it in details",
    image_file_path="./11_vision_sample_data/grocery_test.png"
    )

print("--------Running first Agent for OCR ---------")
result_ocr_text = agent_vision.run_sync(image_request.encoded_message_with_image)
print(result_ocr_text.data)


print("--------Running second Agent for summarizing the extracted data ---------")
result_structured = agent_analysis.run_sync(result_ocr_text.data)
print(result_structured.data.model_dump_json(indent=2))
