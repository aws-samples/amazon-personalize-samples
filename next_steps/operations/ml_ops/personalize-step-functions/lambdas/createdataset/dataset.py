from boto3 import client
import logging
import actions

personalize = client('personalize')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ARN = 'arn:aws:personalize:us-east-1:{account}:dataset/{name}/{datasetType}'


def lambda_handler(event, context):
  status = None
  event['DatasetArn'] = ARN.format(account=event['AccountID'], name=event['DatasetGroupName'], datasetType=event['DatasetType'])
  try:
    status = personalize.describe_dataset(datasetArn=event['DatasetArn'])
  except personalize.exceptions.ResourceNotFoundException:
    logger.info('Dataset not found! Will follow to create dataset.')

    personalize.create_dataset(
        name = event['DatasetName'],
        datasetType = event['DatasetType'],
        datasetGroupArn = event['DatasetGroupArn'],
        schemaArn = event['SchemaArn']
    )
    status = personalize.describe_dataset(datasetArn=event['DatasetArn'])
    print(status['dataset']['status'])
  actions.takeAction(status['dataset']['status'])
  return event
