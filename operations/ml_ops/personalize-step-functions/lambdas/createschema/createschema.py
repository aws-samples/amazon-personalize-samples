from boto3 import client
import logging
import actions
import json

personalize = client('personalize')
ACCOUNTID = client('sts').get_caller_identity()['Account']
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ARN = 'arn:aws:personalize:us-east-1:{account}:schema/{name}'


def lambda_handler(event, context):
    
  status = None
  event['SchemaArn'] = ARN.format(account=ACCOUNTID, name=event['SchemaName'])
  event['AccountID'] = ACCOUNTID
  try:
    status = personalize.describe_schema(schemaArn=event['SchemaArn'])
  except personalize.exceptions.ResourceNotFoundException:
    logger.info('Schema not found! Will follow to create the schema.')


    schema = event['Schema']
    personalize.create_schema(
        name = event['SchemaName'],
        schema = json.dumps(schema)
    )
    status = personalize.describe_schema(schemaArn=event['SchemaArn'])
    print(status['schema']['schemaArn'])
  actions.takeSchemaAction(status['schema']['schemaArn'], event)
  return event
