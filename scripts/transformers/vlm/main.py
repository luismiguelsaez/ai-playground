from transformers import AutoProcessor, AutoModelForImageTextToText
from transformers.image_utils import load_image
from torch.cuda import is_available

# Set device
device = "cuda:0" if is_available() else "cpu"

# Load model and processor
model_id = "LiquidAI/LFM2-VL-1.6B"
model = AutoModelForImageTextToText.from_pretrained(
    model_id, device_map=device, dtype="bfloat16"
)
processor = AutoProcessor.from_pretrained(model_id)

# Load image and create conversation
image_path = "local_image.jpg"
image = load_image(image_path)
conversation = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": "Read the text from the image"},
        ],
    },
]

# Generate Answer
inputs = processor.apply_chat_template(
    conversation,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
    tokenize=True,
).to(model.device)
outputs = model.generate(**inputs, max_new_tokens=64)
outputs_decoded = processor.batch_decode(outputs, skip_special_tokens=True)[0]

print(outputs_decoded)
