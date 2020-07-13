
# Getting Started

ML Ops is gaining a lot of popularity. This example showcases a key piece you can use to construct your automation pipeline. As we can see in the following architecture diagram, you will be deploying an AWS Step Funciton Workflow containing AWS Lambda functions that call Amazon S3, Amazon Personalize, and Amazon SNS APIs.

![Architecture Diagram](images/personalize-stepfunctions.png)


## Prerequisites

### Installing AWS SAM

The AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings. With just a few lines per resource, you can define the application you want and model it using YAML. During deployment, SAM transforms and expands the SAM syntax into AWS CloudFormation syntax, enabling you to build serverless applications faster.

**Install** the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html). 
This will install the necessary tools to build, deploy, and locally test your project. In this particular example we will be using AWS SAM to build and deploy only. For additional information please visit our [documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).

### Create a S3 Bucket

**Create** a S3 Bucket following these [instructions](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html), this bucket will host your training file.

### Training Files

You can find a sample testing file **movie-lens-100k.csv** in the **/test-data** directory of this repo. You can find a more detailed tutorial on how to transform your data and manually train your Amazon Personalize campaings in the following [Notebook](https://github.com/aws-samples/amazon-personalize-samples/blob/master/personalize_sample_notebook.ipynb)

**Upload** the *movie-lens-100k.csv* file to the previously created S3 bucket


## Build and Deploy

In order to deploy the project you will need to run the following commands:

1. Clone the Amazon Personalize Samples repo 
    - `git clone https://github.com/aws-samples/amazon-personalize-samples.git`
2. Navigate into the *operations/ml_ops/personalize-step-functions* directory
    - `cd operations/ml_ops/personalize-step-functions` 
3. Build your SAM project. [Installation instructions](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
    - `sam build` 
4. Deploy your project. SAM offers a guided deployment option, note that you will need to provide your email address as a parameter to receive a notification.
    - `sam deploy --guided`
5. Navigate to your email inbox and confirm your subscription to the SNS topic

## Using the Step Functions State Machine

AWS Step Functions lets you coordinate multiple AWS services into serverless workflows so you can build and update apps quickly. Using Step Functions, you can design and run workflows that stitch together services, such as AWS Lambda, AWS Fargate, and Amazon SageMaker, into feature-rich applications. Workflows are made up of a series of steps, with the output of one step acting as input into the next. 

Now that you have successfully deploy the project please navigate to [AWS Step Functions console](https://console.aws.amazon.com/states/home?region=us-east-1#/statemachines) to get started. Here you will see your newly create State Machine. Before we trigger our State Machine we need to prepare the input.

### Preparing your Step Machine Parameters

During this section we will be modifying the following JSON object 

```JSON
{
    "Bucket": "BUCKET_NAME",
    "Key": "movie-lens-100k.csv",
    "SchemaName": "SCHEMA_EXAMPLE",
    "Schema": {
        "type": "record",
        "name": "Interactions",
        "namespace": "com.amazonaws.personalize.schema",
        "fields": [
            {
                "name": "USER_ID",
                "type": "string"
            },
            {
                "name": "ITEM_ID",
                "type": "string"
            },
            {
                "name": "TIMESTAMP",
                "type": "long"
            }
        ],
        "version": "1.0"
    },
  	"DatasetGroupName": "DATA_SET_GROUP_EXAMPLE",
  	"DatasetName": "PERSONALIZE_LAUNCH_INTERACTIONS",
  	"DatasetType": "INTERACTIONS",
  	"ImportJobName": "IMPORT_JOB_EXAMPLE",
	"SolutionName": "SOLUTION_NAME",
  	"CampaignName": "CAMPAIGN_NAME",
  	"RecipieName": "aws-hrnn",
  	"MinProvisionedTPS": 1
}
```

If you are using the sample data provided in earlier steps, most of the values in this JSON object can stay the same. The most important values you need to modify are the **Bucket** and **Key** which point your State Machine to the location of your training data in your S3 location.

The rest of this section dives deeper into what each of the parameters mean for your Personalize training automation.

#### Training Data

* Modify the **Bucket** parameter with the name of your S3 Bucket that will host your data. 

If you are using the csv file from the prerequisites section you can keep the current **Key** parameter; assuming you uploaded the file in the parent directory. If you are using your own training data, please modify the **Key** parameter with the directory structure leading where you training csv file resides.

#### Schema

A core component of how Personalize understands your data comes from the Schema that is defined below. This configuration tells the service how to digest the data provided via your CSV file. Note the columns and types align to what was in the file you created above. 

* Enter a unique **SchemaName**, if you are using the test file from the prerequisites you can keep the **Schema** structure as define bellow.

#### Datasets

The largest grouping in Personalize is a Dataset Group, this will isolate your data, event trackers, solutions, and campaigns. Grouping things together that share a common collection of data. 

* Modify the **DatasetGroupName** name below if you'd like.

Amazon Personalize recognizes three types of historical datasets. Each type has an associated schema with a name key whose value matches the dataset type. The three types are: Users, Items, and Interactions. For more information about Datasets please visit the following [dataset documentation](https://docs.aws.amazon.com/personalize/latest/dg/how-it-works-dataset-schema.html).

* If you are utilizing the example file provided above you can keep the **DatasetType**. Feel free to modify the **DatasetName**, and **ImportJobName** values.

#### Solutions
In Amazon Personalize a trained model is called a *Solution*, each Solution can have many specific versions that relate to a given volume of data when the model was trained.

* Modify the **SolutionName** parameter if you would like to.

Amazon Personalize provides predefined recipes, based on common use cases, for training models. A recipe is a machine learning algorithm or algorithm variant that you use with settings, or hyperparameters, and a dataset group to train an Amazon Personalize model. With recipes, you can create a personalization system without prior machine learning experience. For more information on available recipies please visit our [recipies documentation](https://docs.aws.amazon.com/personalize/latest/dg/working-with-predefined-recipes.html)

* If you are using the example file you can keep the **RecipieName**, and **MinProvisionedTPS** parameters as defined bellow.

#### CampaignName

A campaign is used to make recommendations for your users. We are creating a campaign by deploying your solution version. For more information visit our [campaign documentation](https://docs.aws.amazon.com/personalize/latest/dg/campaigns.html)

* Modify the **CampaignName** parameter if you would like to.

## Triggering your State Maching

1. Select your newly created State Machine by navigating to your [AWS Step Functions Console](https://console.aws.amazon.com/states/home?region=us-east-1#/statemachines)
2. Click on **Start Execution**
3. Provide a **name** for you execution
4. For your input value please provide the **JSON object** from the above section.
5. Wait for the workflow to be completed, this process will take anywhere between 50 minutes to an hour
6. You will receive an email with your Campaign ARN, make sure you have confirm the subscription of your email address

## Next Steps

Congratulations! You have successfully trained a Personalize model and created a Campaign. You can get recommendations leveraging your campaign ARN or by visiting the [Amazon Personalize Console](https://console.aws.amazon.com/personalize/home?region=us-east-1#datasetGroups) Dataset Group Campaign section.

For additional information on Getting Recommendations please visit our [documentation](https://docs.aws.amazon.com/personalize/latest/dg/getting-recommendations.html) or one of our walkthrough [notebook examples](https://github.com/aws-samples/amazon-personalize-samples/blob/master/personalize_sample_notebook.ipynb).
