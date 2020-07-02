Amazon Personalize User Personalization
---


HRNN based recipes predict items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.

In this examples, we have interactions data, so we will choose one from the basic recipes.

| Feasible? | Recipe | Description 
|-------- | -------- |:------------
| Y - collaborative filtering based | aws-hrnn | Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.
| Y - hrnn but requires meta data | aws-hrnn-metadata | Predicts items a user will interact with. HRNN with additional features derived from contextual (user-item interaction metadata), user metadata (user dataset) and item metadata (item dataset)
| Y - hrnn plus bandits and requires meta data | aws-hrnn-coldstart | Predicts items a user will interact with. HRNN-metadata with personalized exploration of new items.
| N - used for reranking a short list | aws-personalized-ranking | Reranks a list of items for a user. Trains on user-item interactions dataset. 
| N - used for related items | aws-sims | Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset
| N - used for popular items | aws-popularity-count | Calculates popularity of items based on count of events against that item in user-item interactions dataset.

## Content

### HRNN

The [personalize_hrnn_example.ipynb](personalize_hrnn_example.ipynb) uploads the 'past' data from temporal splitting and evaluates the recommendation against the held-out 'future' ground truth.

### HRNN-METADATA

Meta-data is ubiquitous. User zipcodes and device types can be useful indicators of preference; item categories and tags can be useful patterns in decision making; click and purchase events may imply different utilities to the user. 

This [personalize_hrnn_metadata_example.ipynb](personalize_hrnn_metadata_example.ipynb) shows how these useful information can be uploaded to our system to aid recommendation. A caveat is that the improvements of meta-data recipes depend on how much information can be extracted from the provided meta-data. Movie genres may be less useful compared with movie ratings, or better, directors and stars.

### HRNN-METADATA + Contextual Recommendations + Even Tracker

In this example we are going over how to leverage Metadata and Context to provide best airline recommendations for users based on historical ratings of such across multiple cabin types with user's location as user metadata

This [personalize_hrnn_metadata_contextual_example.ipynb](personalize_hrnn_metadata_contextual_example.ipynb) shows how these useful information can be uploaded to our system to aid recommendation. A caveat is that the improvements of meta-data recipes depend on how much information can be extracted from the provided meta-data.


### HRNN-COLDSTART

An important functionality that meta-data, particularly item meta-data, provides is to generalize to new 'cold-start' items. Examples include new releases, new products, or live items. Without personalization, a global policy to introduce these new items may incur large promotional costs. Personalized 'cold-start' helps reduce these costs.

This [personalize_coldstart_demo.ipynb](personalize_hrnn_coldstart_example.ipynb) shows how we may personalize item 'cold-start' by exploring only in the same movie genres that the user would be interested in. The steps are:
 
### License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.


