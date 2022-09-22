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

* Scalable Operations examples for your Amazon Personalize deployments
    - [Maintaining Personalized Experiences with Machine Learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
        - This AWS Solution allows you to automate the end-to-end process of importing datasets, creating solutions and solution versions, creating and updating campaigns, creating filters, and running batch inference jobs. These processes can be run on-demand or triggered based on a schedule that you define.
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

* Workshops
    - [Workshops/](/next_steps/workshops/) folder contains a list of our most current workshops:
        - [POC in a Box](/next_steps/workshops/POC_in_a_box)
        - [re:Invent 2019](/next_steps/workshops/Reinvent_2019)
        - [Immersion Day](/next_steps/workshops/Immersion_Day)
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

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
