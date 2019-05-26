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


def handle_record(record):
    image = record['dynamodb']['NewImage']
    return {
        'id': image['id']['S'],
        'state': image['state']['S'],
        'url': image['url']['S'],
    }


def handler(event, context):
    try:
        for record in list(filter(lambda r: r['eventName'] == 'INSERT', event['Records'])):
            url_item = handle_record(record)
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
                    'id': url_item['id'],
                    'state': 'PROCESSED',
                    'title': title,
                    's3Url': "https://s3.amazonaws.com/" + os.environ['WebPageContentsBucket'] + "/" + build_s3_path(
                        url)
                })
                return {
                    "statusCode": 200,
                    "message": "url processing finished with id = {}".format(url_item['id'])
                }
            else:
                logging.error('page fetch failed!')
                return {'statusCode': 500,
                        'body': json.dumps({'error_message': 'page fetch failed!'})}
    except requests.ConnectionError:
        logging.error("failed to connect")
        return {'statusCode': 404,
                'body': json.dumps({'error_message': 'failed to connect'})}


