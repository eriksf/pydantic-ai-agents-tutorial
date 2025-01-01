from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
from pathlib import Path

model = OllamaModel( model_name='Replete-LLM-V2.5-Qwen-32b-Q5_K_S')


agent = Agent(
    model=model,
    result_retries = 3,
    system_prompt = "You are smart agent with analysis skills, you will analysis any file and extract as much info as possible",
)

@agent.tool_plain
def list_all_files(input_dir: str) -> list[str]:
    """
    List all files in the input directory

    Args:
        input_dir (str): The directory to list files from

    Returns:
        (list[str]): A list of all file paths in the input directory
    """
    print(f"Call list files with dir:{input_dir}")
    return [str(path) for path in Path(input_dir).glob("**/*")]


@agent.tool_plain
def list_files_matching_pattern(input_dir: str, pattern: str) -> list[str]:
    """
    List all files matching a specific pattern in the given directory.

    Args:
        directory (str): The directory to search for files.
        pattern (str): The pattern to match file names against.

    Returns:
        list[str]: A list of paths to files that match the specified pattern within the directory.
    """
    print(f"Call list files with pattern, dir:{input_dir}, pattern:{pattern}")
    return [str(path) for path in Path(input_dir).glob(pattern)]


@agent.tool_plain
def get_file_contents_as_str(file_path: str) -> str:
    """
    Read the contents of a file as a string

    Args:
        file_path (str): The path to the file to read
    Returns:
        (str): The contents of the file as a string
    """
    print(f"get files content called for file {file_path}")
    return Path(file_path).read_bytes().decode("utf-8")





response = agent.run_sync("Analysis the .bin file in directory '/home/abdallah/dev/test1/pydantic/src/sample_data' and tell me what is this file")
print(response.data)


response = agent.run_sync("Do you find andy common data between all files in '/home/abdallah/dev/test1/pydantic/src/sample_data'")
print(response.data)

