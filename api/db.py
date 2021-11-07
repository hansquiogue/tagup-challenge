"""
Loads a database's contents.
"""

from sqlalchemy import create_engine
from api.setup import settings

try:    
    # Test to see if JSON keys are found - specifically file path
    path = settings["data"]["path"]
    print("Data file path found. Proceeding to load data.")

    # Loading database
    engine = create_engine("sqlite:///" + path, echo = False)
    print("Database successfully loaded.")

except:
    print("Something went wrong with the database loading process.")