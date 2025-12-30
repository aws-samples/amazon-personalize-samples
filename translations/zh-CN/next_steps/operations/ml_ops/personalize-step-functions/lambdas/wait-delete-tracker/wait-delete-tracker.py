from os import environ
from loader import Loader
import actions

LOADER = Loader()


def lambda_handler(event, context):
    # return event
    status = LOADER.personalize_cli.describe_event_tracker(
        eventTrackerArn=event['eventTrackerArn']
    )['eventTracker']

    actions.take_action_delete(status['status'])
    return status['status']