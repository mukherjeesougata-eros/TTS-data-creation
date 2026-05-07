import os
import shutil

# Paths (EDIT THESE)
wav_dir = "/mnt/data0/Sougata/Dataset/Voice-dataset/hindi-all-wav-set5"
dir_dir = "/mnt/data0/Sougata/Dataset/Voice-dataset/hindi-all-wav-set5_processed"
output_dir = "/mnt/data0/Sougata/Dataset/Voice-dataset/hindi-all-wav-set6"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get set of directory names in dir_dir
existing_dirs = {
    name for name in os.listdir(dir_dir)
    if os.path.isdir(os.path.join(dir_dir, name))
}

# Loop through wav files
for file in os.listdir(wav_dir):
    if not file.lower().endswith(".wav"):
        continue

    wav_name = os.path.splitext(file)[0]  # remove .wav

    # If no matching directory exists, copy the wav
    if wav_name not in existing_dirs:
        src = os.path.join(wav_dir, file)
        dst = os.path.join(output_dir, file)
        shutil.copy2(src, dst)
        print(f"Copied: {file}")

print("✅ Done copying unmatched WAV files.")
