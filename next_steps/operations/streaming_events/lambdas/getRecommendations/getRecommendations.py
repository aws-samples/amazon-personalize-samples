from boto3 import client
personalize_cli = client('personalize-runtime')
import json
import os

def handler(event, context):
    print(f"Event = {event}")
    payload = json.loads(event['body'])
    try:
        response = personalize_cli.get_recommendations(
            campaignArn=os.environ['CAMPAIGN_ARN'],
            userId=payload['userId'],
            # numResults=123,
            # filterArn = 'string',
            context=payload['context'])
        print(f"RawRecommendations = {response['itemList']}")
        return {'statusCode': '200', 'body': json.dumps(response)}
    except personalize_cli.exceptions.ResourceNotFoundException as e:
        print(f"Personalize Error: {e}")
        return {'statusCode': '500', 'body': json.dumps("Campaign Not Found")}
    except personalize_cli.exceptions.InvalidInputException as e:
        print(f"Invalid Input Error: {e}")
        return {'statusCode': '400', 'body': json.dumps("Invalid Input")}
    except KeyError as e:
        print(f"Key Error: {e}")
        return {'statusCode': '400', 'body': json.dumps("Key Error")}
