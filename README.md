# Amazon Personalize Samples

Notebooks and examples on how to onboard and use various features of Amazon Personalize. This content is also available in four languages: Spanish, French, Korean and Chinese. The [translations/](translations/) folder contains the content in respective languages in thier folders.

## Getting Started with the Amazon Personalize

The [getting_started/](getting_started/) folder contains a CloudFormation template that will deploy all the resources you need to build your first campaign with Amazon Personalize.

The notebooks provided can also serve as a template to building your own models with your own data. This repository is cloned into the environment so you can explore the more advanced notebooks with this approach as well.

## Amazon Personalize Next Steps

The [next_steps/](next_steps/) folder contains detailed examples of the following typical next steps in your Amazon Personalize journey. This folder contains the following advanced content:

* Core Use Cases
  - [User Personalization](/next_steps/core_use_cases/user_personalization)
  - [Personalize Ranking](/next_steps/core_use_cases/personalized_ranking)
  - [Related Items](/next_steps/core_use_cases/related_items)
  - [Batch Recommendations](/next_steps/core_use_cases/batch_recommendations)
  - [User Segmentation](/next_steps/core_use_cases/user_segmentation)

* Generative AI
  - [Personalized marketing campaigns](/next_steps/generative_ai/personalized_marketing_campaign/)
  - [User personalized marketing messaging with Amazon Personalize and Generative AI](next_steps/generative_ai/user_personalized_marketing_messaging_with_amazon_personalize_and_gen_ai). 
        - Use this sample to create personalized marketing content (for instance emails) for each user using [Amazon Personalize](https://aws.amazon.com/personalize/) and [Amazon Bedrock](https://aws.amazon.com/bedrock/). In this sample you will train an [Amazon Personalize](https://aws.amazon.com/personalize/) 'Top picks for you' Recommender to get personalized recommendations for each user. You will then generate a prompt that includes the user's preferences, recommendations, and demographics. Finally you will use [Amazon Bedrock](https://aws.amazon.com/bedrock/) to generate a personalized email for each user.
  - [Amazon Personalize Langchain extensions](https://github.com/aws-samples/amazon-personalize-langchain-extensions)


* Scalable Operations examples for your Amazon Personalize deployments
    - [MLOps Step function](/next_steps/operations/ml_ops) (legacy)
        - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Step Functions. To get started navigate to the [ml_ops](/next_steps/operations/ml_ops) folder and follow the README instructions. This example has been replaced by the [Maintaining Personalized Experiences with Machine Learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/) solution.
    - [MLOps Data Science SDK](/next_steps/operations/ml_ops_ds_sdk)
        - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Data Science SDK. To get started navigate to the [ml_ops_ds_sdk](/next_steps/operations/ml_ops_ds_sdk) folder and follow the README instructions.
    - [Personalization APIs](https://github.com/aws-samples/personalization-apis)
        - Real-time low latency API framework that sits between your applications and recommender systems such as Amazon Personalize. Provides best practice implementations of response caching, API gateway configurations, A/B testing with [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html), inference-time item metadata, automatic contextual recommendations, and more.
    - [Lambda Examples](/next_steps/operations/lambda_examples)
        - This folder starts with a basic example of integrating `put_events` into your Personalize Campaigns by using Lambda functions processing new data from S3. To get started navigate to the [lambda_examples](/next_steps/operations/lambda_examples) folder and follow the README instructions.
    - [Personalize Monitor](https://github.com/aws-samples/amazon-personalize-monitor)
        - This project adds monitoring, alerting, a dashboard, and optimization tools for running Amazon Personalize across your AWS environments.
    - [Streaming Events](/next_steps/operations/streaming_events)
        - This is a project to showcase how to quickly deploy an API Layer in front of your Amazon Personalize Campaign and your Event Tracker endpoint. To get started navigate to the [streaming_events](operations/streaming_events/) folder and follow the README instructions.
    - [Clickstream Analytics](https://aws.amazon.com/solutions/implementations/clickstream-analytics-on-aws/)
        - This is a solution from AWS that collects, ingests, analyzes, and visualizes clickstream data. It can be used to collect clickstream data for Amazon Personalize

* Workshops
    - [Workshops/](/next_steps/workshops/) folder contains a list of our most current workshops:
        - [Immersion Day](https://github.com/aws-samples/amazon-personalize-immersion-day)
    - [Partner Integrations](https://github.com/aws-samples/retail-demo-store#partner-integrations)
        - Explore workshops demonstrating how to use Personalize with partners such as Amplitude, Braze, Optimizely, and Segment.

* Data Science Tools
    - The [data_science/](/next_steps/data_science/) folder contains an example on how to approach visualization of the key properties of your input datasets.
        - Missing data, duplicated events, and repeated item consumptions
        - Power-law distribution of categorical fields
        - Temporal drift analysis for cold-start applicability
        - Analysis on user-session distribution

* Demos/Reference Architectures
    - [Retail Demo Store](https://github.com/aws-samples/retail-demo-store)
        - Sample retail web application and workshop platform demonstrating how to deliver omnichannel personalized customer experiences using Amazon Personalize.
    - [Live Event Contextualization](https://github.com/aws-samples/amazon-personalize-live-event-contextualization)
        - This is a sample code base to illustrate the concept of personalization and contextualization for real-time streaming events. This [blog](https://aws.amazon.com/blogs/media/part-3-contextualized-viewer-engagement-and-monetization-for-live-ott-events/) illustrates the concept


## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
