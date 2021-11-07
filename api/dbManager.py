"""
Database manager.

This file keeps track of all functions that submits queries 
to a database.
"""

from api.db import engine

def fetch_combined_data():
    """
    This function submits a query that joins all tables
    contents together. 
    
        Returns:
            A list of joined table values
    """ 

    query = """
        SELECT feat_0.timestamp, feat_0.machine,
            feat_0.value AS val0, feat_1.value AS val1,
            feat_2.value as val2, feat_3.value as val3,
            install_date, model, room
        FROM feat_0 
        LEFT JOIN feat_1 
            ON (feat_0.timestamp, feat_0.machine)
                = (feat_1.timestamp, feat_1.machine)
        LEFT JOIN feat_2
            ON (feat_0.timestamp, feat_0.machine)
                = (feat_2.timestamp, feat_2.machine)
        LEFT JOIN feat_3
            ON (feat_0.timestamp, feat_0.machine)
                = (feat_3.timestamp, feat_3.machine)
        LEFT JOIN static_data
            ON feat_0.machine = machine_id;
        """
    try:
        data = engine.execute(query).fetchall()
        print("Joined data successfully retrieved from company database.")
        return data
    
    except:
        print("Something went wrong retrieving data from the database.")