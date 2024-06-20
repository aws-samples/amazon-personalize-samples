from os import environ
import actions
from loader import Loader

LOADER = Loader()

def lambda_handler(event, context):
    listETResponse = LOADER.personalize_cli.list_event_trackers(
        datasetGroupArn=event['datasetGroupArn'])
    if(len(listETResponse['eventTrackers']) > 0):
        eventTrackerArn = listETResponse['eventTrackers'][0]['eventTrackerArn']
        status = LOADER.personalize_cli.describe_event_tracker(
            eventTrackerArn=eventTrackerArn
        )['eventTracker']
        status = LOADER.personalize_cli.describe_event_tracker(
            eventTrackerArn=eventTrackerArn
        )['eventTracker']
    else:
        LOADER.logger.info(
            'Event tracker not found!'
        )
        event['eventTracker']['datasetGroupArn'] = event['datasetGroupArn']
        createStatus = LOADER.personalize_cli.create_event_tracker(**event['eventTracker'])
        eventTrackerArn = createStatus['eventTrackerArn']
        status = LOADER.personalize_cli.describe_event_tracker(
            eventTrackerArn=eventTrackerArn
        )['eventTracker']
    
    actions.take_action(status['status'])
    return eventTrackerArn