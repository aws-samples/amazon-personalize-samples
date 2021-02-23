from os import environ
import actions
from loader import Loader

LOADER = Loader()


def create_filter(args):
    
    filterARN = 'arn:aws:personalize:{region}:{account}:filter/{args.name}'
    try:
        status = LOADER.personalize_cli.describe_filter(
            filterArn=filterARN
        )['filter']['status']

    except LOADER.personalize_cli.exceptions.ResourceNotFoundException:
        LOADER.logger.info(
            'Filter not found! Will follow to create a new filter.'
        )
        LOADER.personalize_cli.create_filter(**args)
        status = LOADER.personalize_cli.describe_filter(
            filterArn=filterARN
        )['filter']['status']

    while status in {'CREATE PENDING', 'CREATE IN_PROGRESS'}:
        status = LOADER.personalize_cli.describe_filter(
            filterArn=filterARN
        )['filter']['status']

    if status != 'ACTIVE':
        raise actions.ResourceFailed
    
    return filterARN

def lambda_handler(event, context):
    meta_filter_arns = []
    for filter in event['filters']:
        meta_filter_arns.append(create_filter(filter))
    return meta_filter_arns