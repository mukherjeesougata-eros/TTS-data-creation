#!/usr/bin/env python3

import sys
import re
from pathlib import Path

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
TEXT_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset/Movie_2_w_txt_tkn")     # contains vocals_*_i_text.txt
TOKEN_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset/Movie_2_w_txt_tkn") # where vocals_*_i_tokens.txt will be written
ZIPVOICE_ROOT = Path("/mnt/data0/Sougata/TTS/ZipVoice")            # contains zipvoice/
# -------------------------------------------------


def extract_base(filename: str):
    """
    From vocals_*_i_text.txt → return vocals_*_i
    """
    match = re.match(r"(vocals_.+_\d+)_text\.txt$", filename)
    if not match:
        return None
    return match.group(1)


def main():
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)

    # Add ZipVoice to PYTHONPATH
    sys.path.insert(0, str(ZIPVOICE_ROOT))

    # Import tokenizer
    from zipvoice.tokenizer.tokenizer import SimpleTokenizer

    tokenizer = SimpleTokenizer(token_file="/mnt/data0/Sougata/TTS/ZipVoice_models/Zipvoice/4-epochs/zipvoice_custom/tokens.txt")

    txt_files = sorted(TEXT_DIR.glob("*.txt"))
    if not txt_files:
        raise RuntimeError(f"No .txt files found in {TEXT_DIR}")

    texts = []
    bases = []

    for txt_path in txt_files:
        base = extract_base(txt_path.name)
        if base is None:
            print(f"⚠️ Skipping non-matching file: {txt_path.name}")
            continue

        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        texts.append(text)
        bases.append(base)

    # Tokenize all texts together
    token_lists = tokenizer.texts_to_tokens(texts)
    
    # Write tokens to files
    for base, tokens in zip(bases, token_lists):
        out_path = TOKEN_DIR / f"{base}_tokens.txt"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(" ".join(map(str, tokens)) + "\n")

        print(f"✅ Written: {out_path.name}")    
    
    # 🔑 CHANGE IS HERE: use texts_to_token_ids
    token_ids = tokenizer.texts_to_token_ids(texts)

    # Write tokens_ids to files
    for base, tokens in zip(bases, token_ids):
        out_path = TOKEN_DIR / f"{base}_tokens_ids.txt"

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(" ".join(map(str, tokens)) + "\n")

        print(f"✅ Written: {out_path.name}")

    print(f"\n🎯 Total token files written: {len(token_lists)}")


if __name__ == "__main__":
    main()



