import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    # TODO implement
    datasetGroupArnVal = event['input']
    describe_dataset_group_response = personalize.describe_dataset_group(
        datasetGroupArn = datasetGroupArnVal
        #datasetGroupArn = event['Payload']['datasetGroupArn']
        
    )
    #personalize.describe_dataset_group
    #print("DatasetGroup: {}".format(datasetGroupArn))
    return_status = False
    status = describe_dataset_group_response["datasetGroup"]["status"]
    print("DatasetGroup: {}".format(status))

    return {
        'status': status,
        'DatasetGroup': status,
        'datasetGroupArn': datasetGroupArnVal,
        'schemaArn': event['schemaArn']
        
        #'body': json.dumps('Hello from Lambda!')
    }
