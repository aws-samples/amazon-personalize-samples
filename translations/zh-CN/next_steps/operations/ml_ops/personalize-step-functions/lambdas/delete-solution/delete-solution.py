from os import environ
from loader import Loader
import actions

LOADER = Loader()


def lambda_handler(event, context):
    try:
        response = LOADER.personalize_cli.delete_solution(
            solutionArn=event['solutionArn']
        )
    except Exception as e:
        LOADER.logger.error(f'Error deleting solution: {e}')
        raise e
