Amazon Personalize Updating Datasets
---

This directory has notebooks containing samples and explanations of common workflow patterns for updating datasets in Amazon Personalize. 

## Samples
Both samples notebooks contain an end-to-end workflow pattern including required setup and cleanup. These notebooks were developed and tested on an [Amazon SageMaker Notebook Instance](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html).

## Deployment Instructions:
- Launch a SageMaker Notebook Instance
- Ensure the Execution Role of your Notebook instance has the required Amazon IAM permissions. A sample policy document that grants appropriately-scoped permissions is defined in [sagemaker_notebook_exec_role.json](sagemaker_notebook_exec_role.json). You can attach this custom policy as a *customer-managed* policy of your Execution Role.
- Upload the notebook to the SageMaker Notebook Instance
- Run the Notebook from the Jupyter environment

### Updating Item Schemas 

Notebook [update-item-dataset-schema-example.ipynb](update-item-dataset-schema-example.ipynb) goes over the process for updating schemas of your datasets in Amazon Personalize; specifically schemas for items. Commentary in this notebook is centered around the an e-commerce use case that uses the item-attribute-affinity recipe.

### Importing New Items Data

Notebook [update-datasets-user-personalization-example.ipynb](update-datasets-user-personalization-example.ipynb) goes over the process for updating your datasets when using Amazon Personalize; specifically adding *new* items and interactions *for those new items*. Commentary in this notebook is centered around the an e-commerce use case that uses the user-personalization recipe. Thus, the auto-update feature for user-personalization solution versions is also discussed.


## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
