from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
import os
import mlflow
from markitdown import MarkItDown
import pymupdf4llm

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

def extract_pdf_to_markdown(pdf_path):
    markdown_content = pymupdf4llm.to_markdown(pdf_path)
    print(markdown_content)
    return markdown_content

class certificationRecord(BaseModel):
    """Represents a record of an awarded certification."""
    certification_name: str = Field(description="Name of the certification")
    issuing_organization: str = Field(description="Organization that issued the certification")
    issue_date_year: int = Field(description="Year the certification was issued")
    issue_date_month: int = Field(description="Month the certification was issued")
    expiration_date_year: int = Field(description="Year the certification expires")
    expiration_date_month: int = Field(description="Month the certification expires")
    certification_id: str = Field(description="Unique identifier for the certification")
    description: str = Field(default="", description="Optional description of the certification")

class trainingRecord(BaseModel):
    """Represents a record of completed training."""
    training_name: str = Field(description="Name of the training program")
    training_provider: str = Field(description="Organization or entity that provided the training")
    completion_date_year: int = Field(description="Year the training was completed")
    completion_date_month: int = Field(description="Month the training was completed")
    duration_hours: float = Field(description="Duration of the training in hours")
    description: str = Field(default="", description="Optional description of the training")

class experinceRecord(BaseModel):
    company_name: str = Field(description="company name the employee worked for")
    start_date_of_employment_year: int = Field(description="which year the employee started to work for this specific company")
    start_date_of_employment_month: int = Field(description="which year the employee started to work for this specific company")
    work_summary: str = Field(description="extract all work describtion for this specifc company")
    tools_used: str = Field(description="list of tools used while employee worked in this company, write it as comma seperated, example: managing linux server, testing, problem solving")
    skills: str = Field(description="list of skills used while employee worked in this company, write it as comma seperated, example: managing linux server, testing, problem solving")


class employeeModel(BaseModel):
    """Automatic Structured response with metadata."""
    employee_name: str = Field(description="full name of employee")
    age: int 
    location_address: str = Field(description="Address if exsist")
    location_city: str = Field(description="City")
    location_country: str = Field(description="country")
    phone_number1: str = Field(description="phone number")
    phone_number2: str = Field(description="optinal second phone number")
    email_address: str = Field(description="email address")
    personal_website: str = Field(description="personal website or blog")
    linkedin_account: str = Field(description="linkedin account url")
    github_account: str = Field(description="github account url")
    experinceRecords: list[experinceRecord]
    certificationsRecords: list[certificationRecord]
    trainingRecords: list[trainingRecord]


agent = Agent(
    model=model,
    output_type=employeeModel,
    system_prompt=(
        "You are an intelligent resume & CV analysis agent. Extract all needed information, Be consice"
        "Analyze CV data and extract all keypoints such as working history, skill list"
        "DON'T SUMMARIZE ANY CONTENT, WRITE DATA IN JSON ENTRY AS IN ORIGINAL CONTENT"
        "DON'T FAKE ANY DATA, IF YOU CAN'T FIND SOME DATA, WRITE _NONE_"
        # "You are an intelligent and accurate resume & CV analysis agent. Extract all needed information"
        # "IF YOU CAN'T FIND the field/entry DATA, WRITE _NONE_ or 0"
        # "always use context provided only, Don't write any information not included in the context"
    ),
    max_result_retries=3
)



# load CV with pyMuPDF
cv_markdown = extract_pdf_to_markdown('resources/abdallah.pdf')

response = agent.run_sync(f"extract all information from attached CV data {cv_markdown}")

print(response.output.model_dump_json(indent=2))
print("-------------------usage ----------------------\n\n")
print(response.usage())
