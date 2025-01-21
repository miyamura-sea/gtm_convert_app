import json

def file_open(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None