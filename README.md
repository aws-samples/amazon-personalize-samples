# Amazon Personalize Samples

Notebooks and examples on how to onboard and use various features of Amazon Personalize

## Getting Started with the Amazon Personalize

The [getting_started/](getting_started/) folder contains a CloudFormation template that will deploy all the resources you need to build your first campaign with Amazon Personalize. 

The notebooks provided can also serve as a template to building your own models with your own data. This repository is cloned into the environment so you can explore the more advanced notebooks with this approach as well.

## Amazon Personalize Next Steps

The [next_steps/](next_steps/) folder contains detailed examples of the following typical next steps in your Amazon Personalize journey. This folder contains the following advanced content:


* Core Use Cases.
  - [User Personalization](/next_steps/core_use_cases/user_personalization)
  - [Personalize Ranking](/next_steps/core_use_cases/personalize_ranking)
  - [Batch Recommendations](/next_steps/core_use_cases/batch_recommendations)
  - [Related Items](/next_steps/core_use_cases/related_items)
 
  

* Scalable Operations examples for your Amazon Personalize deployments
    - [MLOps Step function](/next_steps/operations/ml_ops)
        - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Step Functions. To get started navigate to the [ml_ops](operations/ml_ops/) folder and follow the README instructions.
    - [MLOps Data Science SDK](/next_steps/operations/ml_ops_ds_sdk)
        - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Data Science SDK. To get started navigate to the [ml_ops_ds_sdk](operations/ml_ops_ds_sdk/) folder and follow the README instructions.      
    - [Lambda Examples](/next_steps/operations/lambda_examples)
        - This folder starts with a basic example of integrating `put_events` into your Personalize Campaigns by using Lambda functions processing new data from S3. To get started navigate to the [lambda_examples](operations/lambda_examples/) folder and follow the README instructions.


* Workshops
    - [Workshops/](/next_steps/workshops/) folder contains a list of our most current workshops:
        - POC in a Box
        - Re:invent 2019
        - Immersion Days

* Data Science Tools
    - The [data_science/](/next_steps/data_science/) folder contains an example on how to approach visualization of the key properties of your input datasets.
        - Missing data, duplicated events, and repeated item consumptions
        - Power-law distribution of categorical fields
        - Temporal drift analysis for cold-start applicability
        - Analysis on user-session distribution

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
