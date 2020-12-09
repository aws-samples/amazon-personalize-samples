import os
from boto3 import client
SNS = client('sns')

def get_message(event):
    message = 'Resource Delete: '
    if 'statesError' in event.keys():
        message += f"Internal error: {event['statesError']}"
    if 'serviceError' in event.keys():
        message += f"Service error: {event['statesError']}"
    if 'datasetGroupArn' in event.keys():
        message += f"DatasetGroup deleted: {event['datasetGroupArn']}"
    if 'Error' in event.keys():
        message += f"State Machine failed: {event['Cause']}"
    return message


def lambda_handler(event, context):
    return SNS.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'], Message=get_message(event)
    )
