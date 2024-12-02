from os import environ
import actions
from loader import Loader

ARN = 'arn:aws:personalize:{region}:{account}:dataset-group/{name}'
LOADER = Loader()


def lambda_handler(event, context):
    datasetGroupArn = ARN.format(
        account=LOADER.account_id,
        name=event['datasetGroup']['name'],
        region=environ['AWS_REGION']
    )
    try:
        status = LOADER.personalize_cli.describe_dataset_group(
            datasetGroupArn=datasetGroupArn
        )['datasetGroup']

    except LOADER.personalize_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Dataset Group not found! Will follow to create Dataset Group.'
        )
        LOADER.personalize_cli.create_dataset_group(**event['datasetGroup'])
        status = LOADER.personalize_cli.describe_dataset_group(
            datasetGroupArn=datasetGroupArn
        )['datasetGroup']

    actions.take_action(status['status'])
    return datasetGroupArn
