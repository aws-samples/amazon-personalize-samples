# Getting Started

This example showcases a key piece you can use to construct your API Layer to consume Amazon Personalize recommendations and produce real time events

As we can see below this is the architecture that you will be deploying from this project.

![Architecture Diagram](images/architecture.png)

**Note:** The Amazon Personalize Campaigns and Event trackers need to be deployed independently beforehand for you to complete this tutorial. You can deploy your Amazon Personalize Campaign by using the following automation example under the MLOps folder, or by leveraging the getting started folder.

## Prerequisites

### Installing AWS SAM

The AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings. With just a few lines per resource, you can define the application you want and model it using YAML. During deployment, SAM transforms and expands the SAM syntax into AWS CloudFormation syntax, enabling you to build serverless applications faster.

**Install** the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html). 
This will install the necessary tools to build, deploy, and locally test your project. In this particular example we will be using AWS SAM to build and deploy only. For additional information please visit our [documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).

### Create your Personalize Components 

**Create** an Amazon Personalize Campaign and attach an event tracker to it, after following our getting started [instructions](https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started).

You could also automate this part by leveraging this MLOps [example](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops)

## Build and Deploy

In order to deploy the project you will need to run the following commands:

1. Clone the Amazon Personalize Samples repo 
    - `git clone https://github.com/aws-samples/amazon-personalize-samples.git`
2. Navigate into the *next_steps/operations/streaming_events* directory
    - `cd amazon-personalize-samples/next_steps/operations/streaming_events` 
3. Build your SAM project. [Installation instructions](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
    - `sam build` 
4. Deploy your project. SAM offers a guided deployment option, note that you will need to provide your email address as a parameter to receive a notification.
    - `sam deploy --guided`
5. Enter the S3 bucket where you will like to store your events data, the Personalize Campaign ARN and EventTracker ID.

## Testing the endpoints

- Navigate to the Amazon CloudFormation [console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1)
- Select the stack deployed by SAM
- Navigate to the outputs sections where you will find 3 endpoints:
    1. Get Recommendations Endpoint
    2. Get History Endpoint
    3. Post Events Endopoint

**GET recommendations example:**

*Query Paramater:* userId=USERID

*Endpoint:* `https://XXXXXX.execute-api.us-east-1.amazonaws.com/se-personalize-dev/recommendations`

*Constructed Endpoint:*

`https://XXXXXX.execute-api.us-east-1.amazonaws.com/se-personalize-dev/recommendations?userId=USERID`

**GET history example:**

*Query Paramater:* userId=USERID

*Endpoint:* `https://XXXXXX.execute-api.us-east-1.amazonaws.com/se-personalize-dev/history`

*Constructed Endpoint:* 

`https://XXXXXX.execute-api.us-east-1.amazonaws.com/se-personalize-dev/history?userId=USERID`

**POST event example**

For the POST endpoint you need so send an event similar to the following in the *body* of the request:

*Enpoint:* `https://XXXXXX.execute-api.us-east-1.amazonaws.com/se-personalize-dev/history`

*Body:*
```
{
    "Event":{
        "itemId": "ITEMID",
        "eventValue": EVENT-VALUE,
        "CONTEXT": "VALUE" //optional
    },
    "SessionId": "SESSION-ID-IDENTIFIER",
    "EventType": "YOUR-EVENT-TYPE",
    "UserId": "USERID"
}
```

## Summary

Now that you have this architecture in your account, you can consume Amazon Personalize recommendations over the API Gateway GET endpoints and stream real time interactions data to the POST endpoint. 

There are two additional features to this architecture:

- A Dynamo DB table which includes your user's history. This table contains all the historical recommendations provided by Amazon Personalize to your user, as well as the events that user streamed to the Event Tracker.
- A S3 bucket containing your events persisted from your Kinesis Stream. You can run analysis on this bucket by using other AWS services such as Glue and Athena. For example you can follow this [blog](https://aws.amazon.com/blogs/big-data/build-and-automate-a-serverless-data-lake-using-an-aws-glue-trigger-for-the-data-catalog-and-etl-jobs/) on how to automate an ETL pipeline.



## Next Steps

Congratulations! You have successfully deployed and tested the API layer around your Amazon Personalize deployment.

For additional information on Getting Recommendations please visit our [documentation](https://docs.aws.amazon.com/personalize/latest/dg/getting-recommendations.html)
