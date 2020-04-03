from boto3 import client
import logging
import actions

personalize = client('personalize')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ARN = 'arn:aws:personalize:us-east-1:{account}:dataset-group/{name}'


def lambda_handler(event, context):
  status = None
  event['DatasetGroupArn'] = ARN.format(account=event['AccountID'],
                                        name=event['DatasetGroupName'])
  try:
    status = personalize.describe_dataset_group(datasetGroupArn=event['DatasetGroupArn'])

  except personalize.exceptions.ResourceNotFoundException:
    logger.info('Dataset Group not found! Will follow to create Dataset Group.')

    personalize.create_dataset_group(
      name=event['DatasetGroupName']
    )
    status = personalize.describe_dataset_group(datasetGroupArn=event['DatasetGroupArn'])
    print(status)
  actions.takeAction(status['datasetGroup']['status'])
  return event
