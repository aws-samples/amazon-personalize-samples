import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    describe_solution_version_response = personalize.describe_solution_version(
        solutionVersionArn = event['solution_version_arn']
    )
    status = describe_solution_version_response["solutionVersion"]["status"]
    #print("SolutionVersion: {}".format(status))

    return {
        'status': status,
        'solution_version_arn': event['solution_version_arn'] 
        #'DatasetGroup': status,
        #'datasetGroupArn': datasetGroupArnVal
        
        #'body': json.dumps('Hello from Lambda!')
    }
