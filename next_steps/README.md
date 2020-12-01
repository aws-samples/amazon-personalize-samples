# Amazon Personalize Next Steps

Notebooks and examples on how to onboard and use various features of Amazon Personalize

## Amazon Personalize Use Cases examples

The [core_use_cases/](core_use_cases/) folder contains detailed examples of the most typical use cases.

## Scalable Operations examples for your Amazon Personalize deployments

The [operations/](operations/) folder contains examples on the following topics:

* MLOps
    - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Step Functions. To get started navigate to the [ml_ops](operations/ml_ops/) folder and follow the README instructions.

* MLOps Data Science SDK
This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Data Science SDK. To get started navigate to the [ml_ops_ds_sdk](operations/ml_ops_ds_sdk/) folder and follow the README instructions.

* Lambda Examples
    - This folder starts with a basic example of integrating `put_events` into your Personalize Campaigns by using Lambda functions processing new data from S3. To get started navigate to the [lambda_examples](operations/lambda_examples/) folder and follow the README instructions.

* [Personalize Monitor](https://github.com/aws-samples/amazon-personalize-monitor)
    - This project adds monitoring, alerting, a dashboard, and optimization tools for running Amazon Personalize across your AWS environments.

## Reference Architectures

The following reference architectures provide examples of how to apply Amazon Personalize across industries:

* Retail - the [Retail Demo Store](https://github.com/aws-samples/retail-demo-store) is a full stack web application that implements personalization using Personalize in a web application, messaging, and conversation AI interfaces. There are hands-on workshops
* Media and Entertainment
* Travel and Hospitality

## Workshops

The [workshops/](workshops/) folder contains a list of our most current workshops:

* POC in a Box
* Re:invent 2019

## Data Science Tools

The [data_science/](data_science/) folder contains an example on how to approach visualization of the key properties of your input datasets.

The key components we look out for include:
- Missing data, duplicated events, and repeated item consumptions
- Power-law distribution of categorical fields
- Temporal drift analysis for cold-start applicability
- Analysis on user-session distribution

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
