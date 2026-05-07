#!/usr/bin/env python3

# import json
# import shutil
# from pathlib import Path
# import re

# # ================= CONFIG =================
# PARENT_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset")   # contains *_processed directories
# OUTPUT_ROOT = Path("/mnt/data0/Sougata/Dataset/Voice-dataset/Hindi_processeed_w_text")
# # =========================================


# def extract_index(wav_path: Path) -> int:
#     """
#     Extract trailing index from vocals_*_m.wav
#     """
#     match = re.search(r"_([0-9]+)\.wav$", wav_path.name)
#     if not match:
#         raise ValueError(f"Cannot extract index from {wav_path.name}")
#     return int(match.group(1))


# def process_processed_dir(processed_dir: Path):
#     """
#     Process one *_processed directory
#     """
#     for src_dir in sorted(processed_dir.iterdir()):
#         if not src_dir.is_dir():
#             continue

#         # Find JSON file
#         json_files = list(src_dir.glob("vocals_*.json"))
#         if len(json_files) != 1:
#             print(f"⚠️ Skipping {src_dir} (expected 1 JSON, found {len(json_files)})")
#             continue

#         json_path = json_files[0]

#         with open(json_path, "r", encoding="utf-8") as f:
#             data = json.load(f)

#         if not isinstance(data, list):
#             print(f"❌ Invalid JSON format in {json_path}")
#             continue

#         # Find wav files
#         wav_files = sorted(
#             src_dir.glob("vocals_*_*.wav"),
#             key=extract_index
#         )

#         if len(wav_files) != len(data):
#             print(
#                 f"❌ Count mismatch in {src_dir}: "
#                 f"{len(wav_files)} wavs vs {len(data)} json entries"
#             )
#             continue

#         for wav_path in wav_files:
#             idx = extract_index(wav_path)

#             try:
#                 text = data[idx]["text"]
#             except (IndexError, KeyError):
#                 print(f"❌ Missing text for index {idx} in {json_path}")
#                 continue

#             out_wav = OUTPUT_ROOT / wav_path.name
#             out_txt = OUTPUT_ROOT / (wav_path.stem + ".txt")

#             # Write text
#             with open(out_txt, "w", encoding="utf-8") as f:
#                 f.write(text.strip() + "\n")

#             # Copy wav
#             shutil.copy2(wav_path, out_wav)

#         print(f"✅ Processed: {processed_dir.name}/{src_dir.name}")


# def main():
#     OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

#     processed_dirs = sorted(
#         d for d in PARENT_DIR.iterdir()
#         if d.is_dir() and "_processed" in d.name
#     )

#     if not processed_dirs:
#         print("❌ No *_processed directories found")
#         return

#     for processed_dir in processed_dirs:
#         process_processed_dir(processed_dir)


# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3

import json
import shutil
from pathlib import Path
import re
import csv

# ================= CONFIG =================
PARENT_DIR = Path("/mnt/data0/Sougata/Dataset/Voice-dataset")   # contains *_processed dirs
OUTPUT_ROOT = Path("/mnt/data0/Sougata/Dataset/Voice-dataset/Hindi_processeed_w_text")
REPORT_CSV = OUTPUT_ROOT / "missing_text_report.csv"
EMPTY_TEXT = ""  # or "[MISSING TEXT]"
# =========================================


def extract_index(wav_path: Path) -> int | None:
    match = re.search(r"_([0-9]+)\.wav$", wav_path.name)
    return int(match.group(1)) if match else None


def process_processed_dir(processed_dir: Path, report_rows: list):
    for src_dir in processed_dir.iterdir():
        if not src_dir.is_dir():
            continue

        json_files = list(src_dir.glob("vocals_*.json"))
        json_path = json_files[0] if json_files else None
        data = []

        if json_path:
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, list):
                        data = loaded
            except Exception:
                pass  # malformed JSON

        wav_files = list(src_dir.glob("vocals_*_*.wav"))

        for wav_path in wav_files:
            idx = extract_index(wav_path)
            text = EMPTY_TEXT
            missing_reason = None

            if idx is None:
                missing_reason = "index_parse_failed"

            elif not data:
                missing_reason = "json_missing_or_invalid"

            elif idx >= len(data):
                missing_reason = "index_out_of_range"

            elif not isinstance(data[idx], dict):
                missing_reason = "entry_not_dict"

            else:
                text = data[idx].get("text", "")
                if not isinstance(text, str) or not text.strip():
                    missing_reason = "text_empty_or_missing"

            # Always copy wav
            out_wav = OUTPUT_ROOT / wav_path.name
            shutil.copy2(wav_path, out_wav)

            # Always write txt
            out_txt = OUTPUT_ROOT / (wav_path.stem + ".txt")
            with open(out_txt, "w", encoding="utf-8") as f:
                f.write(text.strip() + "\n")

            # Log missing text cases
            if missing_reason:
                report_rows.append({
                    "processed_dir": processed_dir.name,
                    "source_dir": src_dir.name,
                    "json_file": json_path.name if json_path else "NONE",
                    "dict_index": idx,
                    "wav_file": wav_path.name,
                    "reason": missing_reason
                })

        print(f"✅ Processed: {processed_dir.name}/{src_dir.name}")


def main():
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    processed_dirs = [
        d for d in PARENT_DIR.iterdir()
        if d.is_dir() and "_processed" in d.name
    ]

    report_rows = []
    total_wavs = 0

    for processed_dir in processed_dirs:
        wavs = list(processed_dir.glob("*/*.wav"))
        total_wavs += len(wavs)
        process_processed_dir(processed_dir, report_rows)

    # Write CSV report
    if report_rows:
        with open(REPORT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "processed_dir",
                    "source_dir",
                    "json_file",
                    "dict_index",
                    "wav_file",
                    "reason",
                ],
            )
            writer.writeheader()
            writer.writerows(report_rows)

    print("\n📊 SUMMARY")
    print(f"Total WAVs expected : {total_wavs}")
    print(f"Total WAVs written  : {len(list(OUTPUT_ROOT.glob('*.wav')))}")
    print(f"Missing text cases  : {len(report_rows)}")

    if report_rows:
        print(f"📝 Report written to: {REPORT_CSV}")


if __name__ == "__main__":
    main()


