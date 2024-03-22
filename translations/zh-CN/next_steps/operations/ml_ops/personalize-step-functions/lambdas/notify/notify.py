import os
from boto3 import client
SNS = client('sns')

def get_message(event):
    if 'statesError' in event.keys():
        return 'Internal error: {}'.format(event['statesError'])
    if 'serviceError' in event.keys():
        return 'Service error: {}'.format(event['statesError'])
    return 'Your Personalize Endpoint is ready!'

def lambda_handler(event, context):
    return SNS.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'], Message=get_message(event)
    )