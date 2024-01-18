import json

def get_json(path:str):
    with open(path) as file:
        return json.load(file)