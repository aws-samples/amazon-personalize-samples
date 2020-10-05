import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):

    create_dataset_import_job_response = personalize.create_dataset_import_job(
        jobName = event['datasetimportjob'],
        datasetArn = event['dataset_arn'],
        bucket = event['bucket_name'],
        filename = event['file_name'],
        role_arn = event['role_arn'],
        
        dataSource = {
            "dataLocation": "s3://{}/{}".format(bucket, filename)
        },
        roleArn = role_arn
    )
    
    dataset_import_job_arn = create_dataset_import_job_response['datasetImportJobArn']
    print(json.dumps(create_dataset_import_job_response, indent=2))
    return {
        'statusCode': 200,
        'dataset_import_job_arn':dataset_import_job_arn,
        'output': dataset_import_job_arn
    }

