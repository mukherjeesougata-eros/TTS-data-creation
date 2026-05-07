#!/usr/bin/env python3

import json
from pathlib import Path
import re

# ================= CONFIG =================
VOCALS_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset/hindi-all-wav-set3_processed/vocals_671d99b1fde21050cff44d87")
TXT_OUTPUT_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset/Movie_2_w_txt_tkn")
# =========================================


def main():
    TXT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find JSON file
    json_files = list(VOCALS_DIR.glob("vocals_*.json"))
    if len(json_files) != 1:
        raise RuntimeError(
            f"Expected exactly one vocals_*.json in {VOCALS_DIR}, "
            f"found {len(json_files)}"
        )

    json_path = json_files[0]

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise RuntimeError("JSON file must contain a list")

    # Extract base name from directory (vocals_*)
    base_name = VOCALS_DIR.name

    # Iterate STRICTLY by index
    for i, entry in enumerate(data):
        text = ""
        if isinstance(entry, dict):
            text = entry.get("text", "")

        txt_filename = f"{base_name}_{i}_text.txt"
        txt_path = TXT_OUTPUT_DIR / txt_filename

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text.strip() + "\n")

        print(f"✅ Written: {txt_path.name}")

    print(f"\n🎯 Total text files written: {len(data)}")


if __name__ == "__main__":
    main()


