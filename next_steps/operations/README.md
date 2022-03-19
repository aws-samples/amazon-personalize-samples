# Amazon Personalize Operations

This topic contains examples on the following topics:

* [Maintaining Personalized Experiences with Machine Learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
    - This AWS Solution allows you to automate the end-to-end process of importing datasets, creating solutions and solution versions, creating and updating campaigns, creating filters, and running batch inference jobs. These processes can be run on-demand or triggered based on a schedule that you define.

* MLOps (legacy)
    - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Step Functions. To get started navigate to the [ml_ops](ml_ops) folder and follow the README instructions. This project has been replaced by the [Maintaining Personalized Experiences with Machine Learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/) solution.

* Data Science SDK
    - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Data Science SDK. To get started navigate to the [ml_ops_ds_sdk](ml_ops_ds_sdk) folder and follow the README instructions.

* [Personalization APIs](https://github.com/aws-samples/personalization-apis)
    - Real-time low latency API framework that sits between your applications and recommender systems such as Amazon Personalize. Provides best practice implementations of response caching, API gateway configurations, A/B testing with [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html), inference-time item metadata, automatic contextual recommendations, and more.

* Lambda Examples
    - This folder starts with a basic example of integrating `put_events` into your Personalize Campaigns by using Lambda functions processing new data from S3. To get started navigate to the [lambda_examples](lambda_examples/) folder and follow the README instructions.

* Streaming Events
    - This is a project to showcase how to quickly deploy an API Layer infront of your Amazon Personalize Campaign and your Event Tracker endpoint. To get started navigate to the [streaming_events](streaming_events/) folder and follow the README instructions.

* Filter Rotation
    - This [serverless application](filter_rotator/) includes an AWS Lambda function that is executed on a schedule to rotate Personalize filters that use expressions with fixed values that must be changed over time. For example, using a range operator based on a date or time value that is designed to include/exclude items based on a rolling window of time.

* [Personalize Monitor](https://github.com/aws-samples/amazon-personalize-monitor)
    - This project adds monitoring, alerting, a dashboard, and optimization tools for running Amazon Personalize across your AWS environments.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
