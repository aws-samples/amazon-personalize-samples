Amazon Personalize Core Use Cases
---

Amazon Personalize is a machine learning service that makes it easy for developers to add individualized recommendations to customers who use their applications. It reflects the vast experience that Amazon has in building personalization systems.
You can use Amazon Personalize in a variety of scenarios, such as giving users recommendations based on their preferences and behavior, personalized re-ranking of results, and personalizing content for emails and notifications.

As the developer, you only need to do the following:

- Format input data and upload the data into an Amazon S3 bucket, or send real-time event data.
- Select a training recipe (algorithm) to use on the data.
- Train a solution version using the recipe.
- Deploy the solution version.

### Mapping use cases to recipes

| Use Case | Recipe | Description 
|-------- | -------- |:------------
| User Personalization | aws-hrnn | Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.
| User Personalization | aws-hrnn-metadata | Predicts items a user will interact with. HRNN with additional features derived from contextual (user-item interaction metadata), user medata (user dataset) and item metadata (item dataset)
| User Personalization | aws-hrnn-coldstart | Predicts items a user will interact with. HRNN-metadata with with personalized exploration of new items.
| Related Items | aws-sims | Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset
| Personalized Ranking | aws-personalized-ranking | Reranks a list of items for a user. Trains on user-item interactions dataset. 


### Content

In this directory we have examples various use cases

1. [User Personalization](user_personalization/)
    - Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.
2. [Related Items](related_items/)
    - Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset 
3. [Personalized Ranking](personalized_ranking/)
    - Reranks a list of items for a user.
4. [Batch Recommendations](batch_recommendations/)
    - Create recommendations on a batch basis

### License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.


