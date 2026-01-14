from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

checkpoint = "LiquidAI/LFM2.5-1.2B-Instruct"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"
model = AutoModelForCausalLM.from_pretrained(
    checkpoint, device_map="cuda:3", quantization_config=quantization_config
)

messages = [
    {
        "role": "system",
        "content": "You are an image generation assistant, providing natural language prompts emphasizing artistic style and fine details",
    }
]

while True:
    user_input = input("- User: ")
    print()

    if user_input == "quit":
        break

    messages.append({"role": "user", "content": user_input})

    try:
        inputs = tokenizer.apply_chat_template(
            messages,
            return_tensors="pt",
            return_dict=True,
            add_generation_prompt=True,
            tokenize=True,
        ).to(model.device)

        inputs_length = inputs["input_ids"].shape[1]

        outputs = model.generate(
            **inputs,
            max_new_tokens=4096,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

        decoded_outputs = tokenizer.decode(
            outputs[0][inputs_length:], skip_special_tokens=True
        )
    except Exception as e:
        print(f"Error during generation: {e}")
        decoded_outputs = "Sorry, I encountered an error processing your request."

    print(f"- Assistant: {decoded_outputs}")
    print()

    messages.append({"role": "assistant", "content": decoded_outputs})

    del inputs, outputs
    torch.cuda.empty_cache()

    print(f"- Assistant: {decoded_outputs}")
    print()
