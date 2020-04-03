from boto3 import client
from time import sleep
from json import dumps
import os

SNS = client('sns')
def lambda_handler(event, context):
    if os.environ['SNS_TOPIC_ARN'] != 'empty':
        message = 'Congratulations!! \n Your campaign has completed training please use the following CampaignARN to get recommendations: \n\n {campaignARN}  \n\n The following information contains the result of your step function execution \n{eventJSON} '
        
        SNS.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=message.format(campaignARN=event['CampaignARN'],
                                    eventJSON=dumps(event, indent=4))
        )
        return event
    return event