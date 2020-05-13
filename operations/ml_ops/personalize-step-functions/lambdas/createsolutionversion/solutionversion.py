from boto3 import client
import logging
import actions
import os

personalize = client('personalize')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
  status = None
  try:
    status = personalize.describe_solution_version(solutionVersionArn=event['SolutionVersionARN'])
  except (personalize.exceptions.ResourceNotFoundException, KeyError, IndexError):
    create_solution_version_response = personalize.create_solution_version(
      solutionArn=event['SolutionArn']
      )
    event['SolutionVersionARN'] = create_solution_version_response['solutionVersionArn']
    status = personalize.describe_solution_version(solutionVersionArn=event['SolutionVersionARN'])
  actions.takeAction(status['solutionVersion']['status'])
  return event
