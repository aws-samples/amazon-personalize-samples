from os import environ
from loader import Loader
import actions

LOADER = Loader()


def lambda_handler(event, context):
    status = LOADER.personalize_cli.delete_solution(
        solutionArn=event['solutionArn']
    )
