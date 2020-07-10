from boto3 import client
import logging
import actions
import os

personalize = client('personalize')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
recipieARN = "arn:aws:personalize:::recipe/{recipie}"
SolutionARN = 'arn:aws:personalize:us-east-1:{account}:solution/stepFunctions_{SolutionName}_{recipie}'
SolutionName = 'stepFunctions_{SolutionName}_{recipie}'

def lambda_handler(event, context):
  status = None
  event['SolutionArn'] = SolutionARN.format(SolutionName=event['SolutionName'], 
                                        account=event['AccountID'],
                                        recipie=event['RecipieName'])
  event['RecipieARN'] = recipieARN.format(recipie=event['RecipieName'])
  event['SolutionName'] = SolutionName.format(SolutionName=event['SolutionName'],
                                      recipie=event['RecipieName'])
  try:
    status = personalize.describe_solution(solutionArn=event['SolutionArn'])
    response = personalize.list_solution_versions(
        solutionArn = event['SolutionArn'],
        maxResults=100
    )
    if len(response['solutionVersions']) > 1: 
        x = [date['lastUpdatedDateTime'] for date in response['solutionVersions']]
        event['SolutionVersionARN'] = response['solutionVersions'][x.index(max(x))]["solutionVersionArn"]
    else:
        event['SolutionVersionARN'] = response['solutionVersions'][0]["solutionVersionArn"]
  except personalize.exceptions.ResourceNotFoundException:
    logger.info('Solution not found! Will follow to create new Solution.')
    personalize.create_solution(
      name = event['SolutionName'],
      datasetGroupArn = event['DatasetGroupArn'],
      recipeArn = event['RecipieARN']
    )
    create_solution_version_response = personalize.create_solution_version(
      solutionArn=event['SolutionArn']
      )
    event['SolutionVersionARN'] = create_solution_version_response['solutionVersionArn']
    status = personalize.describe_solution(solutionArn=event['SolutionArn'])
  actions.takeAction(status['solution']['status'])
  return event
