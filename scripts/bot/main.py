from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

checkpoint = "LiquidAI/LFM2.5-1.2B-Instruct"

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(
    checkpoint, device_map="cuda:3", quantization_config=quantization_config
)

messages = [
    {
        "role": "system",
        "content": "You are a general knowledge assistant, answering in a cheerful mood",
    }
]


def get_response(user_input, conversation_history):
    """Get response from LLM for given user input and conversation history."""
    logger.debug(f"Generating response for user input: {user_input}")
    conversation_history.append({"role": "user", "content": user_input})

    inputs = tokenizer.apply_chat_template(
        conversation_history,
        return_tensors="pt",
        return_dict=True,
        add_generation_prompt=True,
        tokenize=True,
    ).to(model.device)

    inputs_length = inputs["input_ids"].shape[1]
    logger.debug(f"Input tokens length: {inputs_length}")

    outputs = model.generate(**inputs, max_new_tokens=4096)
    logger.debug("LLM generation completed")

    decoded_outputs = tokenizer.decode(
        outputs[0][inputs_length:], skip_special_tokens=True
    )
    logger.debug(f"Generated response length: {len(decoded_outputs)}")

    conversation_history.append({"role": "assistant", "content": decoded_outputs})

    return decoded_outputs


if __name__ == "__main__":
    # Keep the original interactive loop for direct usage
    while True:
        user_input = input("- User: ")
        print()

        if user_input == "quit":
            break

        response = get_response(user_input, messages)
        print(f"- Assistant: {response}")
        print()
