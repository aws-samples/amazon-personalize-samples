import json
import boto3
import base64


personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):

    datasetArn = event['dataset_arn']
    bucket = event['bucket_name']
    filename = event['file_name']
    roleArn = event['role_arn']
    
    create_dataset_import_job_response = personalize.create_dataset_import_job(
        jobName = "stepfunction-dataset-import-job",
        datasetArn = datasetArn,
        dataSource = {
            "dataLocation": "s3://{}/{}".format(bucket, filename)
        },
        roleArn = roleArn
    )
    
    dataset_import_job_arn = create_dataset_import_job_response['datasetImportJobArn']
    print(json.dumps(create_dataset_import_job_response, indent=2))




    # TODO implement
    return {
        'statusCode': 200,
        'dataset_import_job_arn': dataset_import_job_arn,
        'datasetGroupArn': event['datasetGroupArn']
        #'body': json.dumps('Hello from Lambda!')
    }
