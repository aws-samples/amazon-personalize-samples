Amazon Personalize Batch Recommendations
---

Use an asynchronous batch workflow to get recommendations from large datasets that do not require real-time updates. For instance, you might create a batch inference job to get product recommendations for all users on an email list, or to get item-to-item similarities (SIMS) across an inventory. To get batch recommendations, you can create a batch inference job by calling CreateBatchInferenceJob.

| Feasible? | Recipe | Description 
|-------- | -------- |:------------
| Y - item re-ranking | aws-personalized-ranking | Reranks a list of items for a user. Trains on user-item interactions dataset. 
| Y - similar items | aws-sims | Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset
| Y - personalized recommendations | aws-hrnn | Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.
| Y - requires meta data | aws-hrnn-metadata | Predicts items a user will interact with. HRNN with additional features derived from contextual (user-item interaction metadata), user medata (user dataset) and item metadata (item dataset)
| Y - for bandits and requires meta data | aws-hrnn-coldstart | Predicts items a user will interact with. HRNN-metadata with with personalized exploration of new items.


### Content

The [hrnn_batch_recommendations_example.ipynb](hrnn_batch_recommendations_example.ipynb)

### License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.




