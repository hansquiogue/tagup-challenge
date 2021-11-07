"""
Upload arrays to Amazon S3.
"""

import boto3, json, os


try:
    # Load JSON filed with secret keys
    with open("secrets.json") as f:
        secrets = json.load(f)

    access_key = secrets["access_key"]
    secret_key = secrets["secret_key"]

except:
    print("Error loading in AWS credentials. Skipping upload process.")
    os.exit()

client = boto3.client("s3", aws_access_key_id = access_key, aws_secret_access_key = secret_key)