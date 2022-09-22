from os import environ
from loader import Loader
import actions

LOADER = Loader()


def lambda_handler(event, context):
    # return event
    status = LOADER.personalize_cli.describe_dataset_group(
        datasetGroupArn=event['datasetGroupArn']
    )['datasetGroup']

    actions.take_action_delete(status['status'])
    return status['status']
