"""
File with functions that manage AWS S3 uploads
"""

from api.upload import client

def upload_to_aws_s3(file):
    """
    Uploads specified file input to Amazon S3 bucket

        Arguments:
            - file: a string represents file path to upload

    """
    try: 
        print("Attempting to upload " + file + " to AWS S3.")

        upload_file_bucket = "tagup-challenge-bucket"   
        client.upload_file(file, upload_file_bucket, file)

        print("Upload successful.")

    except:
        print("Something went wrong with the uploading process.",
              "Perhaps the 'secret' file was not configured.")   