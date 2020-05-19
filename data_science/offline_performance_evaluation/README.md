Offine Performance Evaluation
===

You have some historical data and you want to know how personalize performs on your data. Here is what we suggest:

1. Temporally split your data into a 'past' training set and a 'future' testing set.
2. Upload the 'past' data to Amazon Personalize, train a solution, and deploy a campaign.
3. Use your campaign to get recommendation for all of your users, and compare with the 'future' testing set.

This is an example, [personalize_temporal_holdout.ipynb](personalize_temporal_holdout.ipynb/) to complete the steps above. We include a basic popularity-based recommendation, which should be easy to beat. This is for sanity checking purposes. A common next-step is to kepp the same training and testing splits, but train different models for more serious offline comparisons.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
