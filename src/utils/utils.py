import json

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"

def remove_zero_dict(d: dict) -> dict:
    dict = {}
    for key, value in d.items():
        if value != 0:
            dict[key] = value

def get_english_letter_frequency_dict():
    with open('../../data/english_letter_frequencies.json', 'r') as file:
        data_dict = json.load(file)
        return data_dict
