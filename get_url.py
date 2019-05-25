import json
import requests
import logging
import validators
import bs4
import boto3
import os
from datetime import datetime


def upload_file_to_s3(bucket_name, path, file):
    try:
        s3 = boto3.resource('s3')
        object = s3.Object(bucket_name, path)
        object.put(Body=file)
    except Exception as e:
        logging.error("Failed uploading file. Continuing. {}".format(e))
    else:
        logging.info("upload file successful")


def get_domain_from_url(url):
    return url.split("//")[-1].split("/")[0].split('?')[0]


def build_s3_path(url):
    timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    return get_domain_from_url(url) + "/" + timestamp + ".hmtl"


def handler(event, context):
    try:
        # check queryParams
        if 'url' not in event['queryStringParameters']:
            logging.error('Bad query param')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'url not provided'})}

        # check url validity
        url = event['queryStringParameters']['url']
        if not validators.url(url):
            logging.error('Invalid Url')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'invalid url'})}

        response = requests.get(url)
        if response:
            logging.info('page fetch success!')
            title = bs4.BeautifulSoup(response.text, "html.parser").title.text
            upload_file_to_s3(os.environ['WebPageContentsBucket'],
                              build_s3_path(url),
                              response.content)
        else:
            logging.error('page fetch failed!')
            return {'statusCode': 500,
                    'body': json.dumps({'error_message': 'page fetch failed!'})}


    except requests.ConnectionError:
        logging.error("failed to connect")
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'failed to connect'})}

    body = {
        "message": "title fetch successful",
        "title": json.dumps({
            "title": title,
            "objectUrl": "https://s3.amazonaws.com/" + build_s3_path(url)
        })
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
