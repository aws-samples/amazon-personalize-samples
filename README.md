## Amazon Personalize Samples

Notebooks and examples on how to onboard and use various features of Amazon Personalize

## Getting Started with the Amazon Personalize

Open the [getting_started/](getting_started/) folder to find a CloudFormation template that will deploy all the resources you need to build your first campaign with Amazon Personalize. 

The notebooks provided can also serve as a template to building your own models with your own data. This repository is cloned into the environment so you can explore the more advanced notebooks with this approach as well.

## Amazon Personalize use case specific examples

Open the [core_use_cases/](core_use_cases/) folder to see detailed descriptions of the following typical use cases.

* Collaborative filtering based on user-item interaction tables. The intuition behind is that similar users like similar items.
  - [Offline evaluation with 'hrnn' user-based recommendation.](core_use_cases/personalize_temporal_holdout.ipynb)
  - [Example of 'sims' item-based recommendation.](core_use_cases/personalize_sims_smell_tests.ipynb)
  - [How recommendation changes after 'put_events'.](core_use_cases/personalize_putEvents_demo.ipynb)
* Hybrid recommendation also considering user, item, and event meta-data. The result is to extrapolate to out-of-sample users and items, based on their meta-data features.
  - [How to use user, item, and event 'meta-data'.](core_use_cases/personalize_metadata_example.ipynb)
  - [Exploring 'cold-start' or 'future' items.](core_use_cases/personalize_coldstart_demo.ipynb)

## Scalable Operations examples for your Amazon Personalize deployments

Open the [operations/](operations/) folder to find examples on the following topics:

* MLOps
    - This is a project to showcase how to quickly deploy a Personalize Campaign in a fully automated fashion using AWS Step Functions. To get started navigate to the [ml_ops](opreations/ml_ops/) folder and follow the README instructions.
* Lambda Examples
    - This folder starts with a basic example of integrating `put_events` into your Personalize Campaigns by using Lambda functions processing new data from S3. To get started navigate to the [lambda_examples](opreations/lambda_examples/) folder and follow the README instructions.

## Reference Architectures

Open the [reference_architectures/](reference_architectures/) folder to find reference architectures on for the following industries:

* Retail
* Media and Entertainment
* Travel and Hospitality 

## Workshops

Open the [workshops/](workshops/) folder to find a list of our workshops:

* POC in a Box
* Re:invent 2019

## Data Science Tools

Open the [data_science/](data_science/) folder to explore a visualization approach of the key properties of your input datasets.

The key components we look out for include:
- Missing data, duplicated events, and repeated item consumptions
- Power-law distribution of categorical fields
- Temporal drift analysis for cold-start applicability
- Analysis on user-session distribution

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
