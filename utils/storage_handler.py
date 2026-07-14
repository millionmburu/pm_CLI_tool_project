
import json
import os

STORAGE_FILE = "data/storage.json" #define the storage of the database file .json

def load_data() -> dict:
    #Loads the application structure of the json file or an empty structure incase it is missing

    if not os.path.exists(STORAGE_FILE):
        # creates an empty directory of the STORAGE FILE incase it doesnt exist
        os.makedirs(os.path.dirname(STORAGE_FILE),exist_ok= True)
        return {"users": {}, "projects": {}}

    try: #Attempts to read the file 
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except(json.JSONDecodeError, IOError):
        #Handles the missing or corrupted files
        print("Database is missing or corrupted, Initialize a fresh database")
        return {"users": {}, "projects": {}}

def save_data(data: dict):
    # saves the python dictionary data in the .json file

    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=4) #conversion into an index text

    except(IOError) as e:
        print(f"[Error] failed to load data to disk: {e}")

