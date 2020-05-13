from boto3 import client
import logging
import actions
import os

personalize = client('personalize')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
CampaignARN = 'arn:aws:personalize:us-east-1:{account}:campaign/{CampaignName}_{recipie}'
CampaignName = '{CampaignName}_{recipie}'
def lambda_handler(event, context):
  status = None
  event['CampaignARN'] = CampaignARN.format(CampaignName=event['CampaignName'], 
                                        account=event['AccountID'],
                                        recipie=event['RecipieName'])
  event['CampaignName'] = CampaignName.format(CampaignName=event['CampaignName'],
                                        recipie=event['RecipieName'])
  try:
    status = personalize.describe_campaign(campaignArn=event['CampaignARN'])
  except personalize.exceptions.ResourceNotFoundException:
    logger.info('Campaign not found! Will follow to create new Campaign.')
    personalize.create_campaign(
      name = event['CampaignName'],
      solutionVersionArn = event['SolutionVersionARN'],
      minProvisionedTPS = event['MinProvisionedTPS']
    )
    status = personalize.describe_campaign(campaignArn=event['CampaignARN'])
  actions.takeAction(status['campaign']['status'])
  return event
