"""
Main script for ML pipeline for ExampleCo, Inc
"""

from sqlalchemy.sql.expression import false
from api import setup, dbManager, transform, uploadManager

# Set to true to upload to AWS
# Note: will not work without secret keys
UPLOAD = False

def main():
    # 0) Initial setup and settings
    settings = setup.settings

    # 1) Retrieved joined company data
    joined_data = dbManager.fetch_combined_data()

    # 2) Transform to pandas DataFrame and clean data
    df = transform.clean_data(joined_data, settings)

    # 3) Convert DataFrame to xarray Dataset
    ds = transform.to_xarray(df, settings)

    # 4) Write out Dataset to disk
    write_path = settings["company_name"] + "_data.nc"
    print("Writing data to disk.")
    ds.to_netcdf(write_path)
    print("Data successfully written to disk.")

    # 5) Optinal: Upload to AWS S3
    if UPLOAD:
        uploadManager.upload_to_aws_s3(write_path)
    
if __name__ == '__main__':
    main()