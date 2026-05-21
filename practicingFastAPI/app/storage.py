# 2 functions - one to read data from json file / one to write data to json file
# in production, we would use a database instead of json file like mysql, postgresql, mongodb etc.

from pathlib import Path 
import json

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "issues.json"


# read data
def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f: # r for read and f for file
            content = f.read()
            if content.strip():
                return json.load(content)
    return [] # if the file does not exist


# write data
def save_data(data):

    # create the directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f: 
        json.dump(data, f, indent=2)
