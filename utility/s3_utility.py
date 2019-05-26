import boto3
import logging


def upload_file_to_s3(bucket_name, path, file):
    try:
        s3 = boto3.resource('s3')
        object = s3.Object(bucket_name, path)
        object.put(Body=file)
    except Exception as e:
        logging.error("Failed uploading file. Continuing. {}".format(e))
    else:
        logging.info("upload file successful")
