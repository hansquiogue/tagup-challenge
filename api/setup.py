"""
Initial setup.

Retrieves configuration contents from a settings file.
"""

import json

try:
    # Load JSON filed with settings (such as company database file path)
    with open("settings.json") as f:
        settings = json.load(f)
    
    print("Settings have been successfully retrieved.")
    
except KeyError:
    print("JSON file structure is corrupted. File path cannot be found.")

except:
    print("Something went wrong with the initial setup. There is something wrong",
            "with the settings file.")