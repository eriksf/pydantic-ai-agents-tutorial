Learn Pydantic AI agents, step by step,

# 🤖 Pydantic AI Agents Tutorial

A step-by-step guide to building intelligent AI agents using Pydantic AI and local models and (Ollama or any OAI compatible). This tutorial demonstrates how to create structured, vision-capable, and tool-equipped AI agents.

## ✅ **Updated for Latest Pydantic-AI APIs**

**All examples have been updated to use the latest Pydantic-AI library APIs**, including:
- Modern `OpenAIModel` with `OpenAIProvider` structure
- Updated parameter names (`output_type`, `max_result_retries`)
- Latest multimodal/vision processing with `BinaryContent`
- Fixed deprecated API usage (`response.output` instead of `response.data`)
- Environment variable configuration for dynamic model setup

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
pip install -r requirements.txt
```

4. Configure your environment:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and uncomment/configure your preferred LLM provider
# The file includes examples for OpenAI, Ollama, vLLM, DeepSeek, and more
```

5. Set up Ollama and required models (choose any of those model)
```bash
# Best agents model for local run
ollama pull llama3.1:8b-instruct-q8_0
ollama pull qwen2.5:14b
ollama pull qwen2.5:32b

# vision models
ollama pull llama3.2-vision:latest
ollama pull minicpm-v
```

## (optional) setup vLLM for tool calling

If you prefer faster local inference you can use vLLM, here is 2 examples for preparing vLLM

### Running LLama3.1
```bash
# create vllm conda environment
conda create -n vllm python=3.12 pip -y
conda activate vllm
pip install vllm

# run vllm with LLama3.1 8B with flags that enables tool calling
# assuming you downloaded the GPTQ-Q8 version

vllm serve Meta-Llama-3.1-8B-Instruct-GPTQ-Q_8 \
           --port 5003 \
           --enforce-eager \
           --kv-cache-dtype fp8 \
           --enable-chunked-prefill  \
           --enable-auto-tool-choice \
           --tool-call-parser llama3_json \
           --guided-decoding-backend xgrammar \
           --chat-template ./tool_chat_template_llama3.1_json.jinja
```
you can download the jinja template from vllm github repo
[vLLM repo](https://github.com/vllm-project/vllm/)
**vllm/examples/tool_chat_template_llama3.1_json.jinja**

### Running Qwen2.5
based on offical documentation Qwen2.5 uses hermes tool calling and hermes jinja template
[Qwen2.5 function_call](https://qwen.readthedocs.io/en/latest/framework/function_call.html)

```bash
# Running Qwen2.5-32B with dual RTX cards.

vllm serve Qwen2.5-32B-Instruct-AWQ --port 5003 \
           --tensor-parallel-size 2  \
           --enforce-eager \
           --kv-cache-dtype fp8 \
           --enable-chunked-prefill  \
           --enable-auto-tool-choice \
           --tool-call-parser hermes \
           --guided-decoding-backend xgrammar \
           --chat-template ./tool_chat_template_hermes.jinja
```

```bash
# Running Qwen3-30B-A3B-GPTQ-Int4 with dual RTX cards.

vllm serve Qwen3-30B-A3B-GPTQ-Int4 \
        --disable-log-requests \
        --port 5003\
        --tensor-parallel-size 2 \
        --enable-prefix-caching \
        --enable-auto-tool-choice \
        --tool-call-parser hermes \
        --enable-reasoning \
        --reasoning-parser deepseek_r1  \
        --guided-decoding-backend xgrammar \
        --kv-cache-dtype fp8
```

### Configuring .env for vLLM

After starting your vLLM server, update your `.env` file to use it. For example, if you're running Qwen2.5-32B-Instruct-AWQ:

```bash
# Edit your .env file
MODEL_NAME=Qwen2.5-32B-Instruct-AWQ
BASE_URL=http://localhost:5003/v1
API_KEY=vllm
```

The examples will automatically use your vLLM server configuration. No code changes needed!



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
