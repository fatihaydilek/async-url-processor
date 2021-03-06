import json
import logging
import uuid
import validators
import os
from utility.dynamo_utility import insert_item


def handler(event, context):
    try:
        # check queryParams
        if 'queryStringParameters' not in event or 'url' not in event['queryStringParameters']:
            logging.error('Bad query param')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'url not provided'})}

        # check url validity
        url = event['queryStringParameters']['url']
        if not validators.url(url):
            logging.error('Invalid Url')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'invalid url'})}

        # generate request identifier
        identifier = str(uuid.uuid1())
        item = {
            'id': identifier,
            'url': url,
            'state': 'PENDING'
        }
        insert_item(os.environ['DynamoTableName'], item)

    except Exception as e:
        logging.error("Error while getting url request. {}".format(e))
        return {'statusCode': 500,
                'body': json.dumps({'error_message': 'Error while getting url request'})}
    else:
        body = {
            "message": "Request received successfully",
            "identifier": identifier
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response
