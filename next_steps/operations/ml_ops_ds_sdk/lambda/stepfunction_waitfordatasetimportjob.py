import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    # TODO implement
    describe_dataset_import_job_response = personalize.describe_dataset_import_job(
        datasetImportJobArn = event['dataset_import_job_arn']
    )
    status = describe_dataset_import_job_response["datasetImportJob"]['status']
    print("DatasetImportJob: {}".format(status))

    return {
        'status': status,
        'dataset_import_job_arn': event['dataset_import_job_arn'],
        'datasetGroupArn': event['datasetGroupArn']
        
        #'o': status,
        #'datasetGroupArn': datasetGroupArnVal
        
        #'body': json.dumps('Hello from Lambda!')
    }
