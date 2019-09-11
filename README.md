## Amazon Personalize Samples

Notebooks and examples on how to onboard and use various features of Amazon Personalize

## Getting Started Workshop

Open the [getting_started/](getting_started/) folder to find a CloudFormation template that will deploy all the resources you need to build your first campaign with Amazon Personalize. The notebooks provided can also serve as a template to building your own models with your own data.

This repository is cloned into the environment so you can explore the more advanced notebooks with this approach as well.

If you just want a simple walkthrough to explore later you can execute [personalize_sample_notebook.ipynb](personalize_sample_notebook.ipynb), it works well inside the same Jupyter environments.


## Demos and Ablation Studies with Temporal Holdout Evaluation

The following codes are accessible in the folder
[personalize_temporal_holdout/](personalize_temporal_holdout/)

Collaborative filtering based on user-item interaction tables. The intuition behind is that similar users like similar items.

1. Offline evaluation with 'hrnn' user-based recommendation.
2. Example of 'sims' item-based recommendation.
3. How recommendation changes after 'put_events'.

Hybrid recommendation also considering user, item, and event meta-data. The result is to extrapolate to out-of-sample users and items, based on their meta-data features.

1. How to use user, item, and event 'meta-data'.
2. Exploring 'cold-start' or 'future' items.

## Diagnostic / Data Visualizatoin Tools

The key components to diagnose include: missing data, duplications, and repeated
events; power-law distribution of categorical fields; temporal drift analysis
for cold-start applicability; and an analysis for session-based hierarchical
models. The details are available in the folder [diagnose/](diagnose/).


## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
