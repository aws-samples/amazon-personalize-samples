import json
import boto3
import base64

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')


def lambda_handler(event, context):
    
    create_solution_version_response = personalize.create_solution_version(
        solutionArn = event['solution_arn']
    )
    
    solution_version_arn = create_solution_version_response['solutionVersionArn']
    #print(json.dumps(create_solution_version_response, indent=2))    
    
    # TODO implement
    return {
        'statusCode': 200,
        'solution_version_arn': solution_version_arn
        #'body': json.dumps('Hello from Lambda!')
    }
