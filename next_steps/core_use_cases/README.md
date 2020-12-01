Amazon Personalize Core Use Cases
---

Amazon Personalize is a machine learning service that makes it easy for developers to produce individualized recommendations for customers who use their applications. It reflects the vast experience that Amazon has in building personalization systems. You can use Amazon Personalize in a variety of scenarios, such as giving users recommendations based on their preferences and behavior, personalized re-ranking of results, and personalizing content for emails and notifications.

As the developer, you only need to do the following:

- Format input data and upload the data into an Amazon S3 bucket, or send real-time event, user, and item data using the Personalize SDK.
- Select a training recipe (algorithm) to use on the data.
- Train a solution version using the recipe.
- Deploy the solution version.

## Mapping use cases to recipes

| Use Case | Recipe | Description
|-------- | -------- |:------------
| User Personalization | aws-user-personalization | This recipe is optimized for all user recommendation scenarios. It predicts the items that a user will interact with based on Interactions, Items, and Users datasets. It uses an HRNN algorithm to generate recommendations based on relevance (exploitation) and automatic item exploration to recommend new/cold items. You control the weighting of exploitation vs exploration.
| Related Items | aws-sims | Computes items similar to a given item based on co-occurrence of item in same user history in the Interactions dataset.
| Personalized Ranking | aws-personalized-ranking | Reranks a list of items for a user. Trains on Interactions, Items, and Users datasets.

*The above table lists the core and most recommended mappings of use-cases to recipes. Personalize does support other recipes such as aws-popularity-count and the legacy aws-hrnn, aws-hrnn-coldstart, and aws-hrnn-metadata recipes. However, the algorithms in the aws-hrnn-\* recipes were subsumed and extended by the aws-user-personalization recipe so are no longer recommended for user personalization use-cases.*

## Content

In this directory we have examples various use cases

1. [User Personalization](user_personalization/)
    - Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions combined with automatic exploration of new/cold items.
2. [Related Items](related_items/)
    - Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset.
3. [Personalized Ranking](personalized_ranking/)
    - Reranks a list of items for a user based on relevance.
4. [Batch Recommendations](batch_recommendations/)
    - Create recommendations for multiple users or items in a single batch job.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
