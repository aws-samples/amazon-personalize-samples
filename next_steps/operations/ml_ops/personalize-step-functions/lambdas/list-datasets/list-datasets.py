from os import environ
from loader import Loader
import actions
import json

LOADER = Loader()


def lambda_handler(event, context):
    try:
        response = LOADER.personalize_cli.list_datasets(
            datasetGroupArn=event['datasetGroupArn'],
            maxResults = 100
        )

        return json.loads(json.dumps(response['datasets'], default=str))
    except Exception as e:
        LOADER.logger.error(f'Error listing datasets {e}')
        raise e
