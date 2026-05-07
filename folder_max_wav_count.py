#!/usr/bin/env python3
#!/usr/bin/env python3

from pathlib import Path

# ================= CONFIG =================
ROOT_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset")
TOP_K = 5
# =========================================


def count_wavs(directory: Path) -> int:
    """Count all .wav files recursively inside a directory"""
    return sum(1 for _ in directory.rglob("*.wav"))


def main():
    results = []

    # Find all *_processed directories
    processed_dirs = [
        d for d in ROOT_DIR.rglob("*_processed")
        if d.is_dir()
    ]

    if not processed_dirs:
        print("❌ No *_processed directories found.")
        return

    for processed_dir in processed_dirs:
        # Only consider directories INSIDE *_processed
        for subdir in processed_dir.iterdir():
            if not subdir.is_dir():
                continue

            wav_count = count_wavs(subdir)
            if wav_count > 0:
                results.append((subdir, wav_count, processed_dir))

    if not results:
        print("❌ No .wav files found inside *_processed directories.")
        return

    # Sort by wav count (descending)
    results.sort(key=lambda x: x[1], reverse=True)

    print(f"\n🏆 Top {TOP_K} directories INSIDE *_processed by WAV count:\n")

    for i, (subdir, count, parent) in enumerate(results[:TOP_K], start=1):
        print(
            f"{i}. {subdir}  →  {count} wav files "
            f"(inside {parent.name})"
        )


if __name__ == "__main__":
    main()


