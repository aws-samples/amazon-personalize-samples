class ResourcePending(Exception):
  pass

class ResourceFailed(Exception):
  pass

def takeAction(status):
  if status in {'CREATE_PENDING', 'CREATE_IN_PROGRESS', 'CREATE PENDING', 'CREATE IN_PROGRESS'}:
    raise ResourcePending
  elif status != 'ACTIVE':
    raise ResourceFailed
  else:
    return True

def takeSchemaAction(schemaArn, event):
  if schemaArn == event['SchemaArn']:
    return True
  else:
    raise ResourceFailed
    
    