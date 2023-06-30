import os
import json
import logging
import boto3

def lambda_handler(event, context):
    global LOGGER
    LOGGER = logging.getLogger()
    LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())

    LOGGER.info(f"received_event: {event}")

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('demo-ccfn')

    response = table.get_item(Key={
    "id": "1"})

    return{
        "statusCode": 200,
        "body": json.dumps({
            "message": event,
            "data": "atul is good python developer & tableau",
            "env": "QA",
            "response": response
        })
    }
