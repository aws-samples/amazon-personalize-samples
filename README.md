## Amazon Personalize Samples

Notebooks and examples on how to onboard and use various features of Amazon Personalize

## Getting Started Workshop

Open the [getting_started/](getting_started/) folder to find a CloudFormation template that will deploy all the resources you need to build your first campaign with Amazon Personalize. The notebooks provided can also serve as a template to building your own models with your own data.

This repository is cloned into the environment so you can explore the more advanced notebooks with this approach as well.

If you just want a simple walkthrough to explore later you can execute [personalize_sample_notebook.ipynb](personalize_sample_notebook.ipynb), it works well inside the same Jupyter environments.


## Demos and Ablation Studies with Temporal Holdout Evaluation

Open the [personalize_temporal_holdout/](personalize_temporal_holdout/) folder to see detailed descriptions of the following typical use cases.

* Collaborative filtering based on user-item interaction tables. The intuition behind is that similar users like similar items.
  - [Offline evaluation with 'hrnn' user-based recommendation.](personalize_temporal_holdout/personalize_temporal_holdout.ipynb)
  - [Example of 'sims' item-based recommendation.](personalize_temporal_holdout/personalize_sims_smell_tests.ipynb)
  - [How recommendation changes after 'put_events'.](personalize_temporal_holdout/personalize_putEvents_demo.ipynb)
* Hybrid recommendation also considering user, item, and event meta-data. The result is to extrapolate to out-of-sample users and items, based on their meta-data features.
  - [How to use user, item, and event 'meta-data'.](personalize_temporal_holdout/personalize_metadata_example.ipynb)
  - [Exploring 'cold-start' or 'future' items.](personalize_temporal_holdout/personalize_coldstart_demo.ipynb)

## Diagnostic / Data Visualization Tools

Open the [diagnose/](diagnose/) folder to have a visualization of the key properties of your input datasets.
The key components we look out for include:
missing data, duplicated events, and repeated item consumptions;
power-law distribution of categorical fields;
temporal drift analysis for cold-start applicability;
and an analysis on user-session distribution.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
