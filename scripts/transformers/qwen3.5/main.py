from transformers import (
    AutoProcessor,
    AutoModelForImageTextToText,
    BitsAndBytesConfig,
    TextIteratorStreamer,
)
from threading import Thread
import re

quantization_config = BitsAndBytesConfig(load_in_8_bit=True)

checkpoint = "Qwen/Qwen3.5-0.8B"
processor = AutoProcessor.from_pretrained(checkpoint)
model = AutoModelForImageTextToText.from_pretrained(
    checkpoint,
    device_map="auto",
)
streamer = TextIteratorStreamer(tokenizer=processor, skip_prompt=True)
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "candy.jpg",
            },
            {"type": "text", "text": "What animal is on the candy?"},
        ],
    },
]

messages = []
while True:
    user_msg = input("User: ")

    match = re.search(r"image:(\S+)", user_msg)
    if match:
        image = match.group(1)
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": user_msg},
                ],
            }
        )
    else:
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_msg},
                ],
            }
        )

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    generation_arguments = inputs
    generation_arguments["max_new_tokens"] = 2048
    generation_arguments["streamer"] = streamer

    # outputs = model.generate(**inputs, max_new_tokens=1024, streamer=streamer)
    generation_thread = Thread(target=model.generate, kwargs=generation_arguments)
    generation_thread.start()
    # assistant_msg = processor.decode(outputs[0][inputs["input_ids"].shape[-1] :])
    assistant_msg = ""
    for t in streamer:
        print(t, end="", flush=True)
        assistant_msg += t
    # print(f"System: {assistant_msg}")
    messages.append(
        {"role": "assistant", "content": [{"type": "text", "text": assistant_msg}]}
    )