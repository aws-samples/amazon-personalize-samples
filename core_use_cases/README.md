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

In this directory we have examples for 4 use cases
1. User Personalization
2. Related Items
3. Personalized Ranking
4. Batch Recommendations


Collaborative filtering based on user-item interaction tables. The intuition behind is that similar users like similar items.

1. [Offline evaluation with 'hrnn' user-based recommendation.](#hrnn)

1. [Example of 'sims' item-based recommendation.](#sims)

1. [How recommendation changes after 'put_events'.](#put_events)

Hybrid recommendation also considering user, item, and event meta-data. The result is to extrapolate to out-of-sample users and items, based on their meta-data features.

1. [How to use user, item, and event 'meta-data'.](#metadata)

1. [Exploring 'cold-start' or 'future' items.](#item_cold_start)


## Example of 'sims' item-based recommendation.<a name="sims"/>

The 'sims' recipe allows next-item recommendation based on a single previous item. It is faster to train and easier to interpret, e.g., in the form of "you see these recommendations because you watched A". (On the contrary, 'hrnn' considers the entire user consumption histories as the recommendation contexts and can therefore be more personalized).

Similar to the 'hrnn' example, [personalize_metadata_example.ipynb](personalize_metadata_example.ipynb) uploads the 'past' data from temporal splitting and evaluates the recommendation against the held-out 'future' ground truth. The results compare favorably with a popularity-based recommendation baseline. We also include examples showing that different "cause" items would lead to different 'sims' results.

## How recommendation changes after 'put_events'.<a name="put_events"/>

Real-time personalization should respond to new click events by the user. For 'hrnn' sequence model, this is straightforward. After you 'put_events' to our system, the user states get updated and the corresponding recommendations change.

Here is an [personalize_putEvents_demo.ipynb](personalize_putEvents_demo.ipynb) showing how User A's recommendation will eventually look like User B's recommendation, if User B's events are appended after User A.

## How to use user, item, and event 'meta-data'.<a name="metadata"/>

Meta-data is ubiquitous. User zipcodes and device types can be useful indicators of preference; item categories and tags can be useful patterns in decision making; click and purchase events may imply different utilities to the user.

This [personalize_metadata_example.ipynb](personalize_metadata_example.ipynb) shows how these useful information can be uploaded to our system to aid recommendation. A caveat is that the improvements of meta-data recipes depend on how much information can be extracted from the provided meta-data. Movie genres may be less useful compared with movie ratings, or better, directors and stars.

## Exploring 'cold-start' or 'future' items.<a name="item_cold_start"/>

An important functionality that meta-data, particularly item meta-data, provides is to generalize to new 'cold-start' items. Examples include new releases, new products, or live items. Without personalization, a global policy to introduce these new items may incur large promotional costs. Personalized 'cold-start' helps reduce these costs.

This [personalize_coldstart_demo.ipynb](personalize_coldstart_demo.ipynb) shows how we may personalize item 'cold-start' by exploring only in the same movie genres that the user would be interested in. The steps are:

1. Randomly hold out 50% of all items to simulate an item 'cold-start' scenario.
2. Remove these items from the interactions table.
3. Use temporal splitting, train a solution, and deploy a campaign with the remaining training data.
4. Compute metrics on the held out items in the testing data split; these items never show up in the training split.

We can see that the cold-start recipe indeed recommends new movies in the same genres that the user prefers. As a baseline and without personalization, new movies would have a lower click rate, which implies larger promotional costs.
