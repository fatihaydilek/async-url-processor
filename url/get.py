import json
import logging
import os
from utility.dynamo_utility import get_item
from utility.decimal_encoder import DecimalEncoder


def handler(event, context):
    try:
        if 'identifier' not in event['queryStringParameters']:
            logging.error('Bad query param')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'identifier not provided'})}

        identifier = event['queryStringParameters']['identifier']
        url_item = get_item(os.environ['DynamoTableName'], identifier)
        logging.info("item fetch success with identifier={}".format(identifier))
    except Exception as e:
        logging.error("Failed quering url item. Continuing. {}".format(e))
        return {'statusCode': 500,
                'body': json.dumps({'error_message': 'Failed quering url item'})}
    else:
        response = {
            "statusCode": 200,
            "body": json.dumps(url_item,
                               cls=DecimalEncoder)
        }

        return response
