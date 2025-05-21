import json


def get_file_instructions(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip() != '' ]
    return lines


def get_json_data(file):
    with open(file, 'r') as f:
        return json.load(f)
