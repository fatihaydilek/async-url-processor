import json
import requests
import logging
import validators
import bs4


def handler(event, context):
    try:
        if 'url' not in event['queryStringParameters']:
            logging.error('Bad query param')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'url not provided'})}

        url = event['queryStringParameters']['url']
        if not validators.url(url):
            logging.error('Invalid Url')
            return {'statusCode': 400,
                    'body': json.dumps({'error_message': 'invalid url'})}

        response = requests.get(url)
        if response:
            logging.info('page fetch success!')
            title = bs4.BeautifulSoup(response.text).title.text
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
        "title": title
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
