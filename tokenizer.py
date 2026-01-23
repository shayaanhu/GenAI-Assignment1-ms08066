import argparse
import sys
import os

# Suppress transformers warnings about PyTorch/TensorFlow
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

import tiktoken

def interactive_mode():
    """Interactive mode - prompts user for input when no args provided."""
    print("\n=== LLM Token Counter ===\n")
    
    # Model selection
    print("Select a model:")
    print("  1. GPT-4 (cl100k_base)")
    print("  2. Llama (TinyLlama)")
    print("  3. DeepSeek (Coder 1.3B)")
    print("  4. Compare all models")
    
    try:
        while True:
            choice = input("\nEnter choice (1-4): ").strip()
            if choice == "1":
                model = "gpt4"
                compare_all = False
                break
            elif choice == "2":
                model = "llama"
                compare_all = False
                break
            elif choice == "3":
                model = "deepseek"
                compare_all = False
                break
            elif choice == "4":
                model = None
                compare_all = True
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
        
        # Text input
        text = input("\nEnter your text: ").strip()
        
        # Check for empty input
        if not text:
            print("Error: No text provided.", file=sys.stderr)
            sys.exit(1)
            
        return text, model, compare_all
        
    except (KeyboardInterrupt, EOFError):
        print("\n\nCancelled by user.")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="LLM Token Counter")
    parser.add_argument("text", nargs="?", help="Input text")
    parser.add_argument("--file", "-f", help="Read input from file")
    parser.add_argument("--model", "-m", choices=["gpt4", "llama", "deepseek"], default="gpt4", help="Select model")
    parser.add_argument("--all", action="store_true", help="Compare all models")
    
    args = parser.parse_args()

    input_text = ""
    compare_all = args.all
    selected_model = args.model
    
    if args.file:
        # Check if file exists
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        
        # Try to read the file
        try:
            with open(args.file, 'r', encoding="utf-8") as f:
                input_text = f.read()
        except PermissionError:
            print(f"Error: Permission denied to read '{args.file}'.", file=sys.stderr)
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: '{args.file}' appears to be a binary file. Only text files are supported.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        input_text = args.text
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
    else:
        # No args provided - run interactive mode
        input_text, selected_model, compare_all = interactive_mode()

    # Empty input check
    if not input_text.strip():
        print("Error: No text provided. Please provide some text to tokenize.", file=sys.stderr)
        sys.exit(1)

    models = ["gpt4", "llama", "deepseek"] if compare_all else [selected_model]
    results = []

    for model in models:
        res = {"model": model, "count": 0, "chars": len(input_text)}
        
        try:
            if model == "gpt4":
                enc = tiktoken.get_encoding("cl100k_base")
                tokens = enc.encode(input_text)
                res["count"] = len(tokens)

            elif model == "llama":
                try:
                    from transformers import AutoTokenizer
                except ImportError:
                    print("Error: transformers library missing", file=sys.stderr)
                    continue

                try:
                    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
                    tokenizer.deprecation_warnings = False
                    tokens = tokenizer.encode(input_text, add_special_tokens=False)
                    res["count"] = len(tokens)
                except Exception as e:
                    print(f"Llama Error: {e}", file=sys.stderr)
                    continue

            elif model == "deepseek":
                try:
                    from transformers import AutoTokenizer
                except ImportError:
                    print("Error: transformers library missing", file=sys.stderr)
                    continue
                
                try:
                    # Using DeepSeek Coder 1.3B (small footprint)
                    # Use trust_remote_code=True if needed for some deepseek models, but standard loaded should work for tokenizer
                    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-1.3b-base", trust_remote_code=True)
                    tokenizer.deprecation_warnings = False
                    tokens = tokenizer.encode(input_text, add_special_tokens=False)
                    res["count"] = len(tokens)
                except Exception as e:
                    print(f"DeepSeek Error: {e}", file=sys.stderr)
                    continue
            
            results.append(res)

        except Exception as e:
            print(f"Error ({model}): {e}", file=sys.stderr)

    for r in results:
        print(f"Model: {r['model']}")
        print(f"Tokens: {r['count']}")
        print(f"Chars: {r['chars']}")
        print("-" * 20)

if __name__ == "__main__":
    main()