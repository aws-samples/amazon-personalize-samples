import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    describe_campaign_response = personalize.describe_campaign(
        campaignArn = event['campaign_arn']
    )
    status = describe_campaign_response["campaign"]["status"]
    print("Campaign: {}".format(status))

    return {
        'status': status,
        'campaign_arn': event['campaign_arn']
        #'o': status,
        #'datasetGroupArn': datasetGroupArnVal
        
        #'body': json.dumps('Hello from Lambda!')
    }
