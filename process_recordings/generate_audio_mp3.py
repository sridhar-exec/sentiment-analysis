from gtts import gTTS
from pathlib import Path
from tqdm import tqdm

# Paths
input_file = "samples.txt"
output_folder = Path("/Users/apple/Library/Mobile Documents/com~apple~CloudDocs/Recordings/")
output_folder.mkdir(parents=True, exist_ok=True)

with open(input_file, "r") as f:
    content = f.read()

samples = content.strip().split("---")

for idx, sample in enumerate(tqdm(samples, desc="Generating MP3 files")):
    sample = sample.strip()
    if not sample:
        continue

    if sample.startswith("TYPE: DIALOGUE"):
        filename = f"dialogue_sample_{idx+1}.mp3"
        text = "\n".join(
            #line.split(":", 1)[-1].strip() for line in sample.split("\n")[1:] if ":" in line
            line.strip() for line in sample.split("\n")[1:] if line.strip()
        )
    elif sample.startswith("TYPE: MONOLOGUE"):
        filename = f"monologue_sample_{idx+1}.mp3"
        text = "\n".join(sample.split("\n")[1:]).strip()
    else:
        continue

    output_path = output_folder / filename
    tts = gTTS(text=text, lang='en')
    tts.save(str(output_path))

print(f"\nDone! MP3s saved to {output_folder}")