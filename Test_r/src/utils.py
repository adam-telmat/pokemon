import os
import json

def load_json(filepath, default=None):
    """
    Load JSON data from a file.
    
    Parameters:
        filepath (str): Path to the JSON file.
        default: The value to return if the file does not exist or fails to load.
    
    Returns:
        The JSON data loaded from the file, or the default value.
    """
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

def save_json(filepath, data):
    """
    Save data as JSON to a file.
    
    Parameters:
        filepath (str): Path to the JSON file.
        data: The data to be saved.
    
    This function ensures that the directory exists before writing the file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
