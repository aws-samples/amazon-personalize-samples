from os import environ
import actions
from loader import Loader

ARN = 'arn:aws:personalize:{region}:{account}:solution/{name}'
LOADER = Loader()


def create_solution(solutionArn, params):
    try:
        status = LOADER.personalize_cli.describe_solution(
            solutionArn=solutionArn
        )['solution']['status']

    except LOADER.personalize_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Solution not found! Will follow to create a new solution.'
        )
        LOADER.personalize_cli.create_solution(**params)
        status = LOADER.personalize_cli.describe_solution(
            solutionArn=solutionArn
        )['solution']['status']

    while status in {'CREATE PENDING', 'CREATE IN_PROGRESS'}:
        status = LOADER.personalize_cli.describe_solution(
            solutionVersion=solutionArn
        )['solution']['status']

    if status != 'ACTIVE':
        raise actions.ResourceFailed


def lambda_handler(event, context):
    solutionArn = ARN.format(
        region=environ['AWS_REGION'],
        account=LOADER.account_id,
        name=event['solution']['name']
    )

    event['solution']['datasetGroupArn'] = event['datasetGroupArn']
    create_solution(solutionArn, event['solution'])

    solutionVersionArn = LOADER.personalize_cli.create_solution_version(
        solutionArn=solutionArn,
        trainingMode='FULL'  # Assumed given we are creating a new model.
    )['solutionVersionArn']

    return solutionVersionArn
