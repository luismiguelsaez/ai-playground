from requests import get
from transformers import AutoModelForCausalLM, AutoTokenizer


def get_external_ip() -> str:
    """
    This is a tool that returns the system external IP, no arguments needed.
    """
    res = get(url="https://ifconfig.co")
    return res.text


tools = [get_external_ip]
checkpoint = "LiquidAI/LFM2.5-1.2B-Instruct"
model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="mps")
tokenizer = AutoTokenizer.from_pretrained(checkpoint)


messages = [
    {"role": "system", "content": "You are an agent which executes tools"},
    {"role": "user", "content": "Get the system external IP"},
]

input = tokenizer.apply_chat_template(
    messages, tokenize=False, tools=[get_external_ip], add_generation_prompt=True
)
print(input)

input_ids = tokenizer.encode(input, return_tensors="pt").to(model.device)
print(input_ids)

generation_args = dict(
    input_ids=input_ids,
    max_new_tokens=1024,
)


output = model.generate(**generation_args)
print(output)

output_text = tokenizer.decode(output[0], skip_special_tokens=False)
print(output_text)
