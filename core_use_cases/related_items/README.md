Amazon Personalize Related Items
---

## Example of 'sims' item-based recommendation.<a name="sims"/>

The 'sims' recipe allows next-item recommendation based on a single previous item. It is faster to train and easier to interpret, e.g., in the form of "you see these recommendations because you watched A". (On the contrary, 'hrnn' considers the entire user consumption histories as the recommendation contexts and can therefore be more personalized).

The [personalize_sims_example.ipynb](personalize_sims_example.ipynb) uploads the 'past' data from temporal splitting and evaluates the recommendation against the held-out 'future' ground truth. The results compare favorably with a popularity-based recommendation baseline. We also include examples showing that different "cause" items would lead to different 'sims' results.

In this example, we only have interactions data, so we will choose one from the basic recipes.

| Feasible? | Recipe | Description 
|-------- | -------- |:------------
| Y | aws-popularity-count | Calculates popularity of items based on count of events against that item in user-item interactions dataset.
| Y | aws-hrnn | Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.
| N - requires meta data | aws-hrnn-metadata | Predicts items a user will interact with. HRNN with additional features derived from contextual (user-item interaction metadata), user medata (user dataset) and item metadata (item dataset)
| N - for bandits and requires meta data | aws-hrnn-coldstart | Predicts items a user will interact with. HRNN-metadata with with personalized exploration of new items.
| N - for item-based queries | aws-sims | Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset
| N - for reranking a short list | aws-personalized-ranking | Reranks a list of items for a user. Trains on user-item interactions dataset. 


