import json
import os

def save_json(data, filename):
    os.makedirs("output", exist_ok=True)

    with open(os.path.join("output", filename), "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Output saved successfully")