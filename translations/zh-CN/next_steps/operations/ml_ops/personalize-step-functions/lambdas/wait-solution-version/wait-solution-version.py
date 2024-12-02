from os import environ
from loader import Loader
import actions

LOADER = Loader()


def lambda_handler(event, context):
    # return event
    status = LOADER.personalize_cli.describe_solution_version(
        solutionVersionArn=event['solutionVersionArn']
    )['solutionVersion']

    actions.take_action(status['status'])
    return status['status']
