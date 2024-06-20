from os import environ
import actions
from loader import Loader
from datetime import datetime

ARN = 'arn:aws:personalize:{region}:{account}:dataset-import-job/{type}_{date}'
LOADER = Loader()


def lambda_handler(event, context):
    # return event
    datasetImportJobArn = ARN.format(
        region=environ['AWS_REGION'],
        account=LOADER.account_id,
        date=event['date'],
        type=event['datasetType']
    )

    try:
        status = LOADER.personalize_cli.describe_dataset_import_job(
            datasetImportJobArn=datasetImportJobArn
        )['datasetImportJob']

    except LOADER.personalize_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Dataset import job not found! Will follow to create new job.'
        )
        LOADER.personalize_cli.create_dataset_import_job(
            jobName='{datasetType}_{date}'.format(**event),
            datasetArn=event['datasetArn'],
            dataSource={
                'dataLocation': 's3://{bucket}/{datasetType}/'.format(**event)
            },
            roleArn=environ['PERSONALIZE_ROLE']
        )
        status = LOADER.personalize_cli.describe_dataset_import_job(
            datasetImportJobArn=datasetImportJobArn
        )['datasetImportJob']

    actions.take_action(status['status'])
    return datasetImportJobArn
