# Crafting Personalized Experiences: A Two-Notebook Guide to Building a Powerful Recommender Agent

## Key Services
- Amazon Bedrock
- Amazon Personalize

## Introduction
Welcome to this two-notebook step-by-step guide on building a powerful recommender agent for personalized recommendations. In this guide, we will take you through the process of creating a recommendation system that enhances user experience and engagement.

Personalized content is essential for enhancing user experience and engagement in today's digital landscape. An AI agent capable of delivering tailored content to individual users based on their preferences, behaviors, and context can significantly increase user satisfaction and loyalty. By presenting relevant and timely content that aligns with each user's unique needs and interests, an AI agent can lead to increased engagement, higher conversion rates, and improved customer retention.

## Environment Prerequisites

This only applies if you are deploying with the CloudFormation template, otherwise consult the IAM permissions needed for your specific task and add them to the role(s) you will be using when running this example.

For this example you require:
1. An AWS Account
2. A user with administrator access to the AWS Account

## Building Your Environment

The first step is to deploy a CloudFormation template that will perform much of the initial setup for you. In another browser window login to your AWS account. Once you have done that open the link below in a new tab to start the process of deploying the items you need via CloudFormation. After clicking one of the Launch Stack buttons below, follow the procedures to launch the template. Be sure to enter a CloudFront stack name in lowercase letters (numbers and hyphens are okay too).

With this deployment option, the CloudFormation template will import this GitHub repository into an Amazon SageMaker Notebook it creates in your account. This notebook can be found in the AWS Console in the SageMaker Service under Notebooks/Notebook Instances. This CloudFormation template will also create the roles with required permissions to do this demo. The CloudFormation template used can be found at [personalizeCFRecommenderAgent.yaml](./personalizeCFRecommenderAgent.yaml).

| Region | Region Code | Launch stack |
|--------|--------|--------------|
| US East (N. Virginia) | us-east-1 | [![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=PersonalizeExample&templateURL=https://personalize-solution-staging-us-east-1.s3.amazonaws.com/personalize-samples-genai-recommender-agent/personalizeCFRecommenderAgent.yml) |

## Notebooks overview

Once you are logged into your AWS Account and you have deployed the CloudFormation template, you will need to find the Amazon SageMaker Notebook under SageMaker -> Notebooks -> Notebook Instances. Locate the Notebook that was deployed through CloudFormation and click on *Open Jupyter*. Once inside the notebook, navigate to:

```
amazon-personalize-samples/next_steps/generative_ai/personalized_recommender_agent/
```

#### Notebook 1: Data Preparation and Recipe Recommendations
In the first notebook, we will focus on preparing the data, training and deploying the [Amazon Personalize](https://aws.amazon.com/personalize/) recommender and custom solution. Throughout this notebook, we will create a [Recommended for you](https://docs.aws.amazon.com/personalize/latest/dg/ECOMMERCE-use-cases.html#recommended-for-you-use-case) recommender and a Similar items solution, set up filters, and create an event tracker that will help us interact with Personalize in real-time.

The estimated time to run through this notebook is about 60 minutes.  
  
#### Notebook 2: Building the Recommender Agent
The second notebook will walk you through the process of creating the recommender agent using a variety of tools, including the resources created in Notebook 1. We will use [Amazon Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) to leverage [Anthropic's tool use (Function Calling)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use).
Throughout the second notebook, we will demonstrate how to integrate the data prepared in Notebook 1, utilize Amazon Personalize features, and incorporate additional tools to enhance the functionality of the recommender agent.

By the end of these two notebooks, you will have a comprehensive understanding of building a recommender agent, leveraging Amazon Bedrock, Amazon Personalize and other tools to create a seamless user experience.

The estimated time to run through this notebook is about 90 minutes.  

#### Notebook 3: Clean Up
This third notebook will delete all created resources from notebook 1 and 2


## Cleanup Resources

In order to cleanup the resources, you must do 2 steps:
1. Cleanup resources created during the demo. To do this, run [the cleanup notebook](./03_Recommender-Agent_CleanUp.ipynb).
2. Delete the stack you created with CloudFormation. To do this, in the AWS Console again click the `Services` link at the top, and this time enter in `CloudFormation` and click the link for it. Then Click the `Delete` button on the stack you created.

Once you see `Delete Completed` you know that all resources created have been deleted.
