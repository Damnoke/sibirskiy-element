import json
import os

def load_knowledge(filename, default_dict):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_dict
    return default_dict
