import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):

    create_dataset_group_response = personalize.create_dataset_group(
        name = event['input']
    )
    
    dataset_group_arn = create_dataset_group_response['datasetGroupArn']
    print(json.dumps(create_dataset_group_response, indent=2)) 

    return {
        'statusCode': 200,
        'datasetGroupArn':dataset_group_arn,
        'schemaArn': event['schemaArn']
        #'output': dataset_group_arn
        
    }
