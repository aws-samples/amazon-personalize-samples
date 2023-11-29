# Personalized marketing email with Movie Recommendations using Amazon Bedrock and Amazon Personalize

# When to use this sample

**Industry: Media & Entertainment (M&E)**

# Key Technologies

- Amazon Bedrock
  - Claude model
- Amazon Personalize
  - Real-time item recommendations
  
# Getting Started

This demo will walk you through how to create personalized marketing content (for instance emails) for each user using Amazon Personalize and Amazon Bedrock.

1. Building a work environment (follow the steps bellow)
2. Format your data to use with [Amazon Personalize](https://aws.amazon.com/personalize/). We used the following data for model training:
* Interations data: we use the ml-latest-small dataset from the [Movielens](https://grouplens.org/datasets/movielens/) project as a proxy for user-item interactions. 
* Item data: in order provide additional metadata, and also to provide a consistent experience for our users we leverage a subset of the IMDb Essential Metadata for Movies/TV/OTT dataset. IMDb is the world's most popular and authoritative source for information on movies, TV shows, and celebrities and powers entertainment experiences around the world. IMDb has [multiple datasets available in the Amazon Data Exchange](https://aws.amazon.com/marketplace/seller-profile?id=0af153a3-339f-48c2-8b42-3b9fa26d3367). <br><img src="./images/IMDb_Logo_Rectangle.png" alt="IMDb logo" style="width:50px;"/></br>

3. Train an Amazon Personalize 'Top picks for you' Recommender to get personalized recommendations for each user.
4. Generate a prompt that includes the user's preferences, recommendations, and demographics.
5. Generate a personalized email for each user with [Amazon Bedrock](https://aws.amazon.com/bedrock/).

## Environment Prerequisites

This only applies if you are deploying with the CloudFormation template, otherwise consult the IAM permissions needed for your specific task and add them to the role(s) you will be using when running this example.

For this example you require:
1. An AWS Account
2. A user with administrator access to the AWS Account

## Building Your Environment

The first step is to deploy a CloudFormation template that will perform much of the initial setup for you. In another browser window login to your AWS account. Once you have done that open the link below in a new tab to start the process of deploying the items you need via CloudFormation. After clicking one of the Launch Stack buttons below, follow the procedures to launch the template. Be sure to enter a CloudFront stack name in lowercase letters (numbers and hyphens are okay too).

With this deployment option, the CloudFormation template will import this GitHub repository into an Amazon SageMaker Notebook it creates in your account. This notebook can be found in the AWS Console under Notebooks/Notebook Instances. This CloudFormation template will also create the roles with required permissions to do this demo. The CloudFormation template used can be found at [personalizeSimpleCFMarketingContentGen.yml](./personalizeSimpleCFMarketingContentGen.yml).

| Region | Region Code | Launch stack | 
|--------|--------|--------------|
| US East (N. Virginia) | us-east-1 | [![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=PersonalizeExample&templateURL=https://personalize-solution-staging-us-east-1.s3.amazonaws.com/personalize-samples-genai-marketing-content/personalizeSimpleCFMarketingContentGen.yml) |
| Europe (Ireland) | eu-west-1 | [![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=PersonalizeExample&templateURL=https://personalize-solution-staging-eu-west-1.s3.eu-west-1.amazonaws.com/personalize-samples-genai-marketing-content/personalizeSimpleCFMarketingContentGen.yml) |
| Asia Pacific (Sydney) | ap-southeast-2 |[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=PersonalizeExample&templateURL=https://personalize-solution-staging-ap-southeast-2.s3.ap-southeast-2.amazonaws.com/personalize-samples-genai-marketing-content/personalizeSimpleCFMarketingContentGen.yml) |

## Cleanup Resources

In order to cleanup the resources, you must do 2 steps:
1. Cleanup resources created during the demo. To do this, run [the cleanup notebook](./02_Clean_Up.ipynb).
2. Delete the stack you created with CloudFormation. To do this, in the AWS Console again click the `Services` link at the top, and this time enter in `CloudFormation` and click the link for it. Then Click the `Delete` button on the stack you created.

Once you see `Delete Completed` you know that all resources created have been deleted.

