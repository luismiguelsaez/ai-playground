"""Quantize LFM2.5-1.2B-Instruct using GPTQ (llmcompressor) - simplified version."""

from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "LiquidAI/LFM2.5-1.2B-Instruct"

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="cuda:0",
    torch_dtype="auto",
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

## CALIBRATION

from datasets import load_dataset

NUM_CALIBRATION_SAMPLES = 512
MAX_SEQUENCE_LENGTH = 2048

print("Loading calibration dataset...")
ds = load_dataset("HuggingFaceH4/ultrachat_200k", split="train_sft")
ds = ds.shuffle(seed=42).select(range(NUM_CALIBRATION_SAMPLES))


def preprocess(example):
    return {"text": tokenizer.apply_chat_template(example["messages"], tokenize=False, add_generation_prompt=True)}


ds = ds.map(preprocess)


def tokenize(sample):
    return tokenizer(
        sample["text"],
        padding=False,
        max_length=MAX_SEQUENCE_LENGTH,
        truncation=True,
        add_special_tokens=False,
    )


ds = ds.map(tokenize, remove_columns=ds.column_names)

## QUANTIZATION

from llmcompressor import oneshot
from llmcompressor.modifiers.quantization import GPTQModifier

# Simple quantization recipe
recipe = GPTQModifier(
    targets="Linear",
    scheme="W4A16",
    ignore=["lm_head"],
)

print("Applying GPTQ quantization...")
oneshot(
    model=model,
    dataset=ds,
    recipe=recipe,
    max_seq_length=MAX_SEQUENCE_LENGTH,
    num_calibration_samples=NUM_CALIBRATION_SAMPLES,
)

# Save the compressed model
SAVE_DIR = "LFM2.5-1.2B-Instruct-GPTQ4bit"
print(f"Saving quantized model to {SAVE_DIR}...")
model.save_pretrained(SAVE_DIR, save_compressed=True)
tokenizer.save_pretrained(SAVE_DIR)

print("Done!")

# Check file sizes
import os
print("\nSaved files:")
for f in sorted(os.listdir(SAVE_DIR)):
    size = os.path.getsize(os.path.join(SAVE_DIR, f)) / (1024 * 1024)
    print(f"  {f}: {size:.1f} MB")