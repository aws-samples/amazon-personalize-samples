import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    # TODO implement
    get_solution_metrics_response = personalize.get_solution_metrics(
        solutionVersionArn = event['solution_version_arn']
    )

    create_campaign_response = personalize.create_campaign(
        name = "stepfunction-campaign",
        solutionVersionArn = event['solution_version_arn'],
        minProvisionedTPS = 1
    )
    
    campaign_arn = create_campaign_response['campaignArn']
    print(json.dumps(create_campaign_response, indent=2))


    return {
        'campaign_arn': campaign_arn,
        'solution_version_arn': event['solution_version_arn']
        #'o': status,
        #'datasetGroupArn': datasetGroupArnVal
        
        #'body': json.dumps('Hello from Lambda!')
    }
