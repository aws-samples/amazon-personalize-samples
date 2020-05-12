from boto3 import client
import logging
import actions
import os

personalize = client('personalize')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ARN = 'arn:aws:personalize:us-east-1:{account}:dataset-import-job/{ImportJobName}'


def lambda_handler(event, context):
  status = None
  event['DatasetImportJobArn'] = ARN.format(account=event['AccountID'],
                                            ImportJobName=event['ImportJobName'])
  try:
    status = personalize.describe_dataset_import_job(datasetImportJobArn=event['DatasetImportJobArn'])

  except personalize.exceptions.ResourceNotFoundException:
    logger.info('Dataset import job not found! Will follow to create new job.')

    personalize.create_dataset_import_job(
      jobName='{ImportJobName}'.format(ImportJobName=event['ImportJobName']),
      datasetArn=event['DatasetArn'],
      dataSource={
        'dataLocation': 's3://{Bucket}/{Key}'.format(Bucket=event['Bucket'], Key=event['Key'])
      },
      roleArn= os.environ['PERSONALIZE_ROLE']
    )
    status = personalize.describe_dataset_import_job(datasetImportJobArn=event['DatasetImportJobArn'])

  actions.takeAction(status['datasetImportJob']['status'])
  return event


