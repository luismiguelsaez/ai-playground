import os
import json
import re
from transformers import AutoModelForCausalLM, AutoTokenizer


def list_files_tool(path: str) -> str:
    """List files in the given directory path."""
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist"
    if not os.path.isdir(path):
        return f"Error: '{path}' is not a directory"

    try:
        entries = os.listdir(path)
        result = []
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                result.append(f"{entry}/")
            else:
                result.append(entry)
        return "\n".join(result) if result else "Empty directory"
    except PermissionError:
        return f"Error: Permission denied for path '{path}'"


def read_files_tool(path: str) -> str:
    """Read the contents of a file."""
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist"
    if not os.path.isfile(path):
        return f"Error: '{path}' is not a file"

    try:
        with open(path, "r") as f:
            content = f.read()
        return content
    except PermissionError:
        return f"Error: Permission denied for path '{path}'"
    except Exception as e:
        return f"Error reading file: {str(e)}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a given directory path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list files from.",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_files",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The file path to read.",
                    }
                },
                "required": ["path"],
            },
        },
    },
]

tool_functions = {"list_files": list_files_tool, "read_files": read_files_tool}


def load_model():
    print("Loading model and tokenizer...")
    model_name = "LiquidAI/LFM2.5-1.2B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype="auto", device_map="auto"
    )
    return model, tokenizer


def parse_tool_calls(response_text: str, parser=None):
    tool_calls = []

    lfm_pattern = r"<\|tool_call_start\|>\[(\w+)\(([^)]*)\)\]<\|tool_call_end\|>"
    lfm_matches = re.findall(lfm_pattern, response_text)
    for func_name, args_str in lfm_matches:
        try:
            args = {}
            arg_parts = re.findall(r'(\w+)="([^"]*)"', args_str)
            for key, value in arg_parts:
                args[key] = value
            tool_calls.append(
                {"type": "function", "function": {"name": func_name, "arguments": args}}
            )
        except Exception:
            pass

    json_match = re.search(r"\[.*?\]", response_text, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group())
            if isinstance(parsed, list):
                for item in parsed:
                    if "name" in item and "arguments" in item:
                        tool_calls.append(
                            {
                                "type": "function",
                                "function": {
                                    "name": item["name"],
                                    "arguments": item["arguments"],
                                },
                            }
                        )
        except json.JSONDecodeError:
            pass

    tool_call_pattern = r"<tool_call>(.*?)</tool_call>"
    tc_matches = re.findall(tool_call_pattern, response_text, re.DOTALL)
    for tc_match in tc_matches:
        name_match = re.search(r"name:\s*(\w+)", tc_match)
        args_match = re.search(r"arguments:\s*(\{.*?\})", tc_match, re.DOTALL)
        if name_match and args_match:
            try:
                args = json.loads(args_match.group(1))
                tool_calls.append(
                    {
                        "type": "function",
                        "function": {"name": name_match.group(1), "arguments": args},
                    }
                )
            except json.JSONDecodeError:
                pass

    return tool_calls


def process_tool_calls(tool_calls: list) -> list:
    results = []
    for tool_call in tool_calls:
        func_name = tool_call["function"]["name"]
        args = tool_call["function"]["arguments"]

        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = {"raw": args}

        if func_name in tool_functions:
            result = tool_functions[func_name](**args)
            results.append((func_name, result))
        else:
            results.append((func_name, f"Error: Unknown function '{func_name}'"))

    return results


def chat_loop(model, tokenizer):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to tools. When the user asks you to perform a task that requires a tool, you MUST use the available tools by outputting a JSON tool call. Available tools: list_files - use this to list files in a directory, read_files - use this to read the contents of a file.",
        }
    ]

    print("\nStarting chat loop. Type 'quit' or 'exit' to stop.")
    print("Available tools: list_files, read_files")
    print()

    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            try:
                inputs = tokenizer.apply_chat_template(
                    messages,
                    tools=tools,
                    add_generation_prompt=True,
                    return_dict=True,
                    return_tensors="pt",
                ).to(model.device)

                outputs = model.generate(
                    **inputs, max_new_tokens=512, temperature=0.7, do_sample=True
                )

                response = tokenizer.decode(
                    outputs[0][inputs.input_ids.shape[1] :], skip_special_tokens=True
                )

                tool_calls = parse_tool_calls(response)

                if not tool_calls:
                    messages.append({"role": "assistant", "content": response})
                    print(f"Assistant: {response}\n")
                    break

                print(f"[Tool call detected: {tool_calls}]")
                messages.append(
                    {"role": "assistant", "content": response, "tool_calls": tool_calls}
                )

                tool_results = process_tool_calls(tool_calls)

                for func_name, result in tool_results:
                    print(
                        f"[Tool result ({func_name}): {result[:100]}...]"
                        if len(str(result)) > 100
                        else f"[Tool result ({func_name}): {result}]"
                    )
                    messages.append(
                        {"role": "tool", "name": func_name, "content": str(result)}
                    )

            except Exception as e:
                print(f"Error: {e}")
                import traceback

                traceback.print_exc()
                break


if __name__ == "__main__":
    model, tokenizer = load_model()
    chat_loop(model, tokenizer)
