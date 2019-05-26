import logging
import boto3


dynamodb = boto3.resource('dynamodb')


def insert_item(table_name, item):
    try:
        table = dynamodb.Table(table_name)
        table.put_item(Item=item)
    except Exception as e:
        logging.error("Failed inserting item. Continuing. {}".format(e))
    else:
        logging.info("insert item successful")


def get_item(table_name, id):
    try:
        table = dynamodb.Table(table_name)

        result = table.get_item(
            Key={
                'id': id
            }
        )
    except Exception as e:
        logging.error("Failed getting item. Continuing. {}".format(e))
        return None
    else:
        if 'Item' in result:
            return result['Item']


def update_item(table_name, item):
    table = dynamodb.Table(table_name)

    result = table.update_item(
        Key={
            'id': item['id']
        },
        UpdateExpression="set #st = :s, s3Url =:s3, title =:t",
        ExpressionAttributeValues={
            ':s': item['state'],
            ':s3': item['s3Url'],
            ':t': item['title']
        },
        ReturnValues='UPDATED_NEW',
        ExpressionAttributeNames={
            "#st": "state"
        }
    )

    return result['Attributes']
