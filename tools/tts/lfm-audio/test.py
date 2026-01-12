import torch
import torchaudio
from liquid_audio import LFM2AudioModel, LFM2AudioProcessor, ChatState, LFMModality

# Load models
HF_REPO = "LiquidAI/LFM2.5-Audio-1.5B"

processor = LFM2AudioProcessor.from_pretrained(HF_REPO).eval()
model = LFM2AudioModel.from_pretrained(HF_REPO).eval()

# Set up inputs for the model
chat = ChatState(processor)

chat.new_turn("system")
chat.add_text("Respond with interleaved text and audio.")
chat.end_turn()

chat.new_turn("user")
wav, sampling_rate = torchaudio.load("assets/question.wav")
chat.add_audio(wav, sampling_rate)
chat.end_turn()

chat.new_turn("assistant")

# Generate text and audio tokens.
text_out: list[torch.Tensor] = []
audio_out: list[torch.Tensor] = []
modality_out: list[LFMModality] = []
for t in model.generate_interleaved(
    **chat, max_new_tokens=512, audio_temperature=1.0, audio_top_k=4
):
    if t.numel() == 1:
        print(processor.text.decode(t), end="", flush=True)
        text_out.append(t)
        modality_out.append(LFMModality.TEXT)
    else:
        audio_out.append(t)
        modality_out.append(LFMModality.AUDIO_OUT)

# output: Sure! How about "Handcrafted Woodworking, Precision Made for You"? Another option could be "Quality Woodworking, Quality Results." If you want something more personal, you might try "Your Woodworking Needs, Our Expertise."

# Detokenize audio, removing the last "end-of-audio" codes
# Mimi returns audio at 24kHz
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
torchaudio.save("answer1.wav", waveform.cpu(), 24_000)

# Append newly generated tokens to chat history
chat.append(
    text=torch.stack(text_out, 1),
    audio_out=torch.stack(audio_out, 1),
    modality_flag=torch.tensor(modality_out),
)
chat.end_turn()

# Start new turn
chat.new_turn("user")
chat.add_text(
    "My business specialized in chairs, can you give me something related to that?"
)
chat.end_turn()

chat.new_turn("assistant")

# Generate second turn text and audio tokens.
audio_out: list[torch.Tensor] = []
for t in model.generate_interleaved(
    **chat, max_new_tokens=512, audio_temperature=1.0, audio_top_k=4
):
    if t.numel() == 1:
        print(processor.text.decode(t), end="", flush=True)
    else:
        audio_out.append(t)

# output: Sure thing! How about “Comfortable Chairs, Crafted with Care” or “Elegant Seats, Handcrafted for You”? Let me know if you’d like a few more options.

# Detokenize second turn audio, removing the last "end-of-audio" codes
audio_codes = torch.stack(audio_out[:-1], 1).unsqueeze(0)
waveform = processor.decode(audio_codes)
torchaudio.save("answer2.wav", waveform.cpu(), 24_000)
