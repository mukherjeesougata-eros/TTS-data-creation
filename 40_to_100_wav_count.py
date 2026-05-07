#!/usr/bin/env python3

from pathlib import Path

# ================= CONFIG =================
ROOT_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset")
MIN_WAVS = 40
MAX_WAVS = 100
# =========================================


def count_wavs(directory: Path) -> int:
    """Count all .wav files recursively inside a directory"""
    return sum(1 for _ in directory.rglob("*.wav"))


def main():
    matched_dirs = []

    # Find all *_processed directories
    processed_dirs = [
        d for d in ROOT_DIR.rglob("*_processed")
        if d.is_dir()
    ]

    if not processed_dirs:
        print("❌ No *_processed directories found.")
        return

    for processed_dir in processed_dirs:
        for subdir in processed_dir.iterdir():
            if not subdir.is_dir():
                continue

            wav_count = count_wavs(subdir)

            if MIN_WAVS <= wav_count <= MAX_WAVS:
                matched_dirs.append((subdir, wav_count, processed_dir))

    if not matched_dirs:
        print(
            f"❌ No directories found with WAV count "
            f"between {MIN_WAVS} and {MAX_WAVS}."
        )
        return

    print(
        f"\n📁 Directories inside *_processed with "
        f"{MIN_WAVS}–{MAX_WAVS} WAV files:\n"
    )

    for subdir, count, parent in matched_dirs:
        print(
            f"- {subdir}  →  {count} wav files "
            f"(inside {parent.name})"
        )


if __name__ == "__main__":
    main()

