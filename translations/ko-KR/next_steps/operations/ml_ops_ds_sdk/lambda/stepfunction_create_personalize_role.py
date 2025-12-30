import json
import boto3
import base64

def lambda_handler(event, context):
    # TODO implement


    #### Attach Policy to S3 Bucket
     
     s3 = boto3.client("s3")
    
    policy = {
        "Version": "2012-10-17",
        "Id": "PersonalizeS3BucketAccessPolicy",
        "Statement": [
            {
                "Sid": "PersonalizeS3BucketAccessPolicy",
                "Effect": "Allow",
                "Principal": {
                    "Service": "personalize.amazonaws.com"
                },
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::{}".format(event['bucket']),
                    "arn:aws:s3:::{}/*".format(event['bucket'])
                ]
            }
        ]
    }
    
    s3.put_bucket_policy(Bucket=event['bucket'], Policy=json.dumps(policy))
     
    #### Create Personalize Role 
 

    iam = boto3.client("iam")
    
    role_name = "PersonalizeRole"
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "Service": "personalize.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
            }
        ]
    }
    
    create_role_response = iam.create_role(
        RoleName = role_name,
        AssumeRolePolicyDocument = json.dumps(assume_role_policy_document)
    )
    
    # AmazonPersonalizeFullAccess provides access to any S3 bucket with a name that includes "personalize" or "Personalize" 
    # if you would like to use a bucket with a different name, please consider creating and attaching a new policy
    # that provides read access to your bucket or attaching the AmazonS3ReadOnlyAccess policy to the role
    
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonPersonalizeFullAccess"
    iam.attach_role_policy(
        RoleName = role_name,
        PolicyArn = policy_arn
    )
    
    time.sleep(60) # wait for a minute to allow IAM role policy attachment to propagate
    
    role_arn = create_role_response["Role"]["Arn"]
    print(role_arn) 
     
 
 
 
    return {
        'statusCode': 200,
        'role_arn':role_arn
        #'body': json.dumps('Hello from Lambda!')
    }
