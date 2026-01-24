# GenAI-Assignment1-ms08066

## Token Counter

CLI tool for counting tokens across different LLMs (GPT-4, Llama, DeepSeek).

## Setup

```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode
Simply run without arguments to get prompted for model selection and text input:
```bash
python tokenizer.py
```

### Command Line Mode
```bash
# Basic count
python tokenizer.py "Input text here"

# Select model (default: gpt4)
python tokenizer.py "Input text" --model llama

# Compare all models
python tokenizer.py "Input text" --all
```
### Models To Choose From
- `gpt4` - GPT-4 tokenizer (cl100k_base)
- `llama` - TinyLlama-1.1B tokenizer
- `deepseek` - DeepSeek Coder 1.3B tokenizer

## Example Output
```
=== LLM Token Counter ===

Select a model:
  1. GPT-4 (cl100k_base)
  2. Llama (TinyLlama)
  3. DeepSeek (Coder 1.3B)
  4. Compare all models

Enter choice (1-4): 1 

Enter your text: Hello World!
Model: gpt4
Token Count: 3
Char Count: 12
Tokens: ['Hello', ' World', '!']
----------------------------------------
```
