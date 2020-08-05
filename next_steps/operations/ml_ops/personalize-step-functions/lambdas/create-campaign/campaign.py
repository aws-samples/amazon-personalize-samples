from os import environ
import actions
from loader import Loader

ARN = 'arn:aws:personalize:{region}:{account}:campaign/{name}'
LOADER = Loader()


def lambda_handler(event, context):
    campaignArn = ARN.format(
        region=environ['AWS_REGION'],
        account=LOADER.account_id,
        name=event['campaign']['name']
    )
    try:
        status = LOADER.personalize_cli.describe_campaign(
            campaignArn=campaignArn
        )['campaign']

    except LOADER.personalize_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Campaign not found! Will follow to create a new campaign.'
        )
        LOADER.personalize_cli.create_campaign(
            name=event['campaign']['name'],
            solutionVersionArn=event['solutionVersionArn'],
            minProvisionedTPS=event['campaign']['minProvisionedTPS']
        )
        status = LOADER.personalize_cli.describe_campaign(
            campaignArn=campaignArn
        )['campaign']

    actions.take_action(status['status'])
    return campaignArn
