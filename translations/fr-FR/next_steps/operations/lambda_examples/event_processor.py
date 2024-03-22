import boto3
import json
import numpy as np
import pandas as pd
import time
import uuid
import os
import urllib.parse

print('Loading function')

personalize = boto3.client('personalize')

s3 = boto3.client('s3')

def push_event_to_Personalize(event):
    """
    Here an event is a file object
    """
    trackingId = os.environ['trackingId']
    print(event[0]['userId'])
    
    personalize.put_events(
        trackingId = trackingId,
        userId = event[0]['userId'],
        sessionId = event[0]['sessionId'],
        eventList = [event[1]]
    )

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response['Body']
        push_event_to_Personalize(event=body.read())
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e