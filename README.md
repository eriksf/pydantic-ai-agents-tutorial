Learn Pydantic AI agents, step by step,

# 🤖 Pydantic AI Agents Tutorial

A step-by-step guide to building intelligent AI agents using Pydantic AI and local models and (Ollama or any OAI compatible). This tutorial demonstrates how to create structured, vision-capable, and tool-equipped AI agents.

## 🌟 Features

- 📝 Structured output
- 🔧 Custom tool integration
- 👁️ Using Vision models (llama3.2 vision / minicpm-v)
- 🤝 Simple Multi-agent systems
- 📁 File handling
- 🔄 Dynamic prompting

## 🚀 Getting Started

1. Clone the repository
2. Create conda evironment

```bash
conda create -n pydantic python=3.12 pip -y
``` 

3. Install dependencies:

```bash
pip install pydantic-ai llm-sandbox
```
4. Set up Ollama and required models (chosee any of those model)
```bash
# Best agents model for local run
ollama pull llama3.1:8b-instruct-q8_0
ollama pull qwen2.5:14b
ollama pull qwen2.5:32b

# vision models
ollama pull llama3.2-vision:latest
ollama pull minicpm-v
```
## 📚 Tutorial Structure

The repository contains progressive examples:

### Basic Concepts
- `0_hello_world.py` - Basic agent setup
- `1_hello_with_OAI_api.py` - OpenAI compatible API integration
- `2_simple_structured.py` - Structured outputs
- `3_simple_structured_table.py` - Table formatting + Structured outputs

### Advanced Features
- `4_lets_make_tools.py` - Custom tool creation
- `5_mix_tools_with_structured_output.py` - Combining tools and structure
- `6_code_as_tool.py` - Code execution capabilities
- `7_code_with_added_libs.py` - External library integration

### Special Features
- `8_lets_make_dynamic_prompt.py` - Dynamic prompt generation
- `9_mix_multiple_prompts.py` - Multiple prompt handling
- `10_lets_open_files.py` - File operations
- `11_hello_vision.py` - Basic vision capabilities
- `12_running_2_mixed_agents_with_vision.py` - Advanced vision and multi-agent systems

## 📝 License

Licensed under the Apache License, Version 2.0. See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.