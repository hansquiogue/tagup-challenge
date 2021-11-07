"""
Data transformation process.

This file transforms and cleans retrieved company data.
"""

import pandas as pd
import xarray as xr

def create_data_frame(data):
    """
    This function creates a pandas DataFrame based on 
    data input.

        Arguments:
            - data: a list containing a company's data

        Returns:
            A pandas DataFrame based on the data input
    """
    # Hard-coded columns from company database
    # TODO: Generalize columns
    cols = ["time", "machine", "sensor0", 
            "sensor1", "sensor2", "sensor3", 
            "install_date", "model", "room"]

    return pd.DataFrame(data, columns = cols) 

def round_time(df, col, round_to = "H"):
    """
    Rounds a column to the nearest time

        Arguments:
            - df: a pandas DataFrame
            - col: a string column representing
            what needs to be rounded. This should be time
            related.
            - round_to: a character representing what to round
            the column to. For example, 'H' will round the time
            to the nearest hour, while 'D' will round the time
            to the nearest day.
    """
    df[col] = pd.to_datetime(df[col])
    df[col] = df[col].dt.round(round_to)

def fix_first_ten_digits(df, col, starting_name = "machine_0"):
    """
    Fixes company machine labeling

        Arguments:
            - col: a string column representing
            what digits need to be fixed.
            - starting_name: a string the represents
            the starting machine name.
    """
    # First ten digits
    first_ten_machines = df[col].unique()[0:10]
    
    # Add zero in front of first ten digits
    for name in first_ten_machines:
        curr_num = name[len(name) - 1]
        df[col] = df[col].replace([name], starting_name + curr_num) 

def fix_sensor_outliers(df, sensor_labels):
    """
    Fixes sensor value outliers. Note that this method is
    very specific to ExampleCo company and should not be used
    for any other company data.

        Arguments:
            - df: a pandas DataFrame
            - sensor_labels: a list of labels for sensor columns
    """
    # Replace numbers greater than 150 or less than 150 with 0
    # TODO: Account for other conditions
    for sensor in sensor_labels:
        condition = (df[sensor] < 150) & (df[sensor] > -150)
        df[sensor].where(condition, 0, inplace = True)

def clean_data(data, company_info):
    """
    Cleans company data

        Arguments:
            - data: company data
            - company_info: dictionary of company information

        Returns:
            Clean pandas DataFrame
    """
    try:
        print("Attempting to clean data.")
        df = create_data_frame(data)
        
        round_time(df, "time")
        fix_first_ten_digits(df, "machine")
        fix_sensor_outliers(df, company_info["sensors"])

        print("Data successfully cleaned.")
        return df
        
    except:
        print("Something went wrong cleaning the data.")    

def create_data_arrays_list(df, company_info, machine_col = "machine", time_col = "time"):
    """
    Create xarray DataArrays for each machine by time and sensor
    
        Arguments:
            - df: pandas DataFrame of company data
            - company_info: a dictionary of company information
            - machine_col: machine column label
            - time_col: time column label

        Returns:
            A list of DataArrays
    """
    # Creating individual arrays and appending them together into a list
    data_arrays = []
    sensor_labels = company_info["sensors"]
    
    # Goes through each machine (machine_00 -> machine_19)
    for m in df[machine_col].unique():
        filtered_machine = df[df["machine"] == m]
        
        new_arr = xr.DataArray(
            data = filtered_machine[sensor_labels],
            dims = ["time", "sensor"],
            coords = dict(
                time = df[time_col].unique(),
                sensor_labels = (["time", "sensor"], 
                                # Multiple sensor labels by row length 
                                # (To corresponding to sensor values)
                                [sensor_labels] * len(df[time_col].unique()))
            ),
            attrs = dict(
                company = company_info["company_name"],
                machine = m,
                model = filtered_machine["model"].tolist()[0],
                install_date = filtered_machine["install_date"].tolist()[0],
                room = filtered_machine["room"].tolist()[0]
            ),
            name = m
        )
    
        data_arrays.append(new_arr)

    return data_arrays
    
def to_xarray(df, company_info):
    """
    Converts pandas DataFrame with company data to xarray Dataset
    
        Arguments:
            - df: pandas DataFrame of company data
            - company_info: a dictionary of company information

        Returns:
            A list of DataArrays
    """
    try: 
        print("Converting data to multidimensional arrays.")
        
        da_list = create_data_arrays_list(df, company_info)
        combined_da = xr.combine_by_coords(da_list)

        print("Data successfully converted.")
        return combined_da
    
    except:
        print("Something went wrong with the xarray conversion process.")