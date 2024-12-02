import json
import base64
import boto3


personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    # TODO implement

    dataset_type = "INTERACTIONS"
    datasetGroupArn = event['datasetGroupArn']
    create_dataset_response = personalize.create_dataset(
        name = "personalize-stepfunction-dataset",
        datasetType = dataset_type,
        datasetGroupArn = event['datasetGroupArn'],
        schemaArn = event['schemaArn']
    )
    
    dataset_arn = create_dataset_response['datasetArn']
    print(json.dumps(create_dataset_response, indent=2))




    return {
        'statusCode': 200,
        'dataset_arn': dataset_arn,
        'datasetGroupArn': datasetGroupArn 
        #'body': json.dumps('Hello from Lambda!')
    }
