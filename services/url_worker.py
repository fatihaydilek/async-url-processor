import json
import requests
import logging
import validators
import bs4
import os
from datetime import datetime
from utility.s3_utility import upload_file_to_s3
from utility.dynamo_utility import get_item, update_item


def get_domain_from_url(url):
    return url.split("//")[-1].split("/")[0].split('?')[0]


def build_s3_path(url):
    timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    return get_domain_from_url(url) + "/" + timestamp + ".hmtl"


def handler(event, context):
    try:
        if 'identifier' in event:
            identifier = event['identifier']
            url_item = get_item(os.environ['DynamoTableName'], identifier)
            url = url_item['url']

        # check url validity
        if not validators.url(url):
            logging.error('Invalid Url')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'invalid url'})}

        response = requests.get(url)
        if response:
            logging.info('page fetch success!')
            title = bs4.BeautifulSoup(response.text, "html.parser").title.text
            # upload content to s3
            upload_file_to_s3(os.environ['WebPageContentsBucket'],
                              build_s3_path(url),
                              response.content)
            # update url item
            update_item(os.environ['DynamoTableName'], {
                'id': identifier,
                'state': '“PROCESSED”',
                's3Url': "https://s3.amazonaws.com/" + os.environ['WebPageContentsBucket'] + "/" + build_s3_path(url)
            })
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
            "objectUrl": "https://s3.amazonaws.com/" + os.environ['WebPageContentsBucket'] + "/" + build_s3_path(url)
        })
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
