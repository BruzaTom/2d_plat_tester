import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load full sound file
full = AudioSegment.from_file("data/sfx/8_Bit_Effects.wav")

# Split based on silence
chunks = split_on_silence(
    full,
    min_silence_len=200,     # silence must be at least 200ms
    silence_thresh=-40       # silence threshold in dBFS
)

# Export each chunk

os.makedirs("data/sfx/split_effects/", exist_ok=True)

for i, chunk in enumerate(chunks):
    out_path = f"data/sfx/split_effects/{i}.wav"
    chunk.export(out_path, format="wav")

