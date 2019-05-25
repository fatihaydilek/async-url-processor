import logging
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')


def insert_item(table_name, data):
    try:
        table = dynamodb.Table(table_name)

        item = {
            'id': str(uuid.uuid1()),
            'text': data,
        }

        table.put_item(Item=item)
    except Exception as e:
        logging.error("Failed inserting item. Continuing. {}".format(e))
    else:
        logging.info("insert item successful")