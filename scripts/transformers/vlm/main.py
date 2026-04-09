from transformers import AutoProcessor, AutoModelForImageTextToText
from transformers.image_utils import load_image
from torch.cuda import is_available
import time
import argparse

# Set device
device = "cuda:0" if is_available() else "cpu"

# Parse command line arguments
parser = argparse.ArgumentParser(description="Image text extraction with LFM2.5-VL")
parser.add_argument("--image", type=str, required=True, help="Path to the input image file")
args = parser.parse_args()

# Time model loading
print("Starting model loading...")
start_time = time.time()
model_id = "LiquidAI/LFM2.5-VL-450M"
model = AutoModelForImageTextToText.from_pretrained(
    model_id, device_map=device, dtype="bfloat16"
)
processor = AutoProcessor.from_pretrained(model_id)
load_time = time.time() - start_time
print(f"Model loading completed in {load_time:.2f} seconds\n")

# Load image and create conversation
image = load_image(args.image)
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
print("Starting generation...")
start_time = time.time()
inputs = processor.apply_chat_template(
    conversation,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
    tokenize=True,
).to(model.device)
outputs = model.generate(**inputs, max_new_tokens=64)
outputs_decoded = processor.batch_decode(outputs, skip_special_tokens=True)[0]
generation_time = time.time() - start_time

print(f"\nGeneration completed in {generation_time:.2f} seconds")
print(f"\nOutput: {outputs_decoded}")
