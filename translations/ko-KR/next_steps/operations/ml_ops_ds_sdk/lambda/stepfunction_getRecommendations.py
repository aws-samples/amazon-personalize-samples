import json
import boto3
import base64

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    
    userId = str(event['user_id'])
    itemId = str(event['item_id'])
    campaignArn = event['campaign_arn']
    
    
    
    print("userId, itemId",userId, itemId )
    
 
    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn=campaignArn,
        userId=userId,
        itemId=itemId

    )
    
    item_list = get_recommendations_response['itemList']

    return {
        'item_list': item_list
        #'body': json.dumps('Hello from Lambda!')
    }
