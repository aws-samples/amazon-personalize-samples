Amazon Personalize Related Items
---

The 'sims' recipe allows your system to recommend what item is most similar to a specific item. It is faster to train and easier to interpret, an example of related items can be a section on your website stating "you see these recommendations because you watched A"

In this example, we have interactions data, so we will choose one from the basic recipes.

| Feasible? | Recipe | Description 
|-------- | -------- |:------------
| Y | aws-sims | Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset
| Y | aws-popularity-count | Calculates popularity of items based on count of events against that item in user-item interactions dataset.
| Y | aws-hrnn | Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.
| N - requires meta data | aws-hrnn-metadata | Predicts items a user will interact with. HRNN with additional features derived from contextual (user-item interaction metadata), user medata (user dataset) and item metadata (item dataset)
| N - for bandits and requires meta data | aws-hrnn-coldstart | Predicts items a user will interact with. HRNN-metadata with with personalized exploration of new items.
| N - for reranking a short list | aws-personalized-ranking | Reranks a list of items for a user. Trains on user-item interactions dataset. 

### Content

The [personalize_sims_example.ipynb](personalize_sims_example.ipynb) uploads the 'past' data from temporal splitting and evaluates the recommendation against the held-out 'future' ground truth. The results compare favorably with a popularity-based recommendation baseline. We also include examples showing that different "cause" items would lead to different 'sims' results.

### License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.




