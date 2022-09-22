from os import environ
import actions
from loader import Loader
from random import randint
from json import dumps

DATASET_ARN = 'arn:aws:personalize:{region}:{account}:dataset/{datasetGroupName}/{type}'
LOADER = Loader()


def create_schema(name, schema):
    schemaArn = 'arn:aws:personalize:{region}:{account}:schema/{name}'

    try:
        schemaResponse = LOADER.personalize_cli.describe_schema(
            schemaArn=schemaArn.format(
                name=name,
                account=LOADER.account_id,
                region=environ['AWS_REGION']
            )
        )

        if schemaResponse['schema']['schema'] != schema:
            LOADER.logger.info(
                '''{name} schema already exists with different schema!
                                    Will follow using different schema name.'''.
                format(name=name)
            )
            return create_schema(
                name='{name}-{rand}'.format(name=name, rand=randint(0, 100000)),
                schema=schema
            )
        return schemaResponse['schema']['schemaArn']

    except LOADER.personalize_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info('Schema not found! Will follow to create schema.')
        return LOADER.personalize_cli.create_schema(
            name=name, schema=dumps(schema)
        )['schemaArn']


def lambda_handler(event, context):
    # return event
    dataset = event['datasets'][event['datasetType']]
    datasetArn = DATASET_ARN.format(
        region=environ['AWS_REGION'],
        account=LOADER.account_id,
        datasetGroupName=event['datasetGroupName'],
        type=str.upper(event['datasetType'])
    )
    try:
        status = LOADER.personalize_cli.describe_dataset(datasetArn=datasetArn
                                                        )['dataset']

    except LOADER.personalize_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Dataset not found! Will follow to create schema and dataset.'
        )
        LOADER.personalize_cli.create_dataset(
            name=dataset['name'],
            schemaArn=create_schema(
                dataset['schema']['name'], dataset['schema']
            ),
            datasetGroupArn=event['datasetGroupArn'],
            datasetType=event['datasetType']
        )
        status = LOADER.personalize_cli.describe_dataset(datasetArn=datasetArn
                                                        )['dataset']

    actions.take_action(status['status'])
    return datasetArn
