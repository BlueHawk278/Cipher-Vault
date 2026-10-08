import json
import re
from pathlib import Path

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"

def remove_zero_dict(d: dict) -> dict:
    filtered_dict = {}
    for key, value in d.items():
        if value != 0:
            filtered_dict[key] = value
    return filtered_dict

def get_english_letter_frequency_dict():
    file_path = Path(__file__).resolve().parent / '../../data/statistics/english_letter_frequencies.json'
    with open(file_path, 'r') as file:
        data_dict = json.load(file)
        return data_dict

def convert_txt_to_json(txt_filepath, json_filepath):
    ngram_counts = {}

    with open(txt_filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                ngram = parts[0].upper()
                count = int(parts[1])
                ngram_counts[ngram] = count

    with open(json_filepath, 'w') as f:
        json.dump(ngram_counts, f, indent=4)

    print(f"Successfully converted {txt_filepath} -> {json_filepath}!")

def normalize(text: str) -> str:
    return re.sub(r'[^A-Z]', '', text.upper())
