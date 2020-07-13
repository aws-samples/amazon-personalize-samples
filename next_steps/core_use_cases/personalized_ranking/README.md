Amazon Personalize Ranking
---

The 'ranking' recipe generates personalized rankings. A personalized ranking is a list of recommended items that are re-ranked for a specific user.

| Feasible? | Recipe | Description 
|-------- | -------- |:------------
| Y | aws-personalized-ranking | Reranks a list of items for a user. Trains on user-item interactions dataset. 
| N - used for similar items | aws-sims | Computes items similar to a given item based on co-occurrence of item in same user history in user-item interaction dataset
| N - used for popularity count| aws-popularity-count | Calculates popularity of items based on count of events against that item in user-item interactions dataset.
| N - used for personalized recommendations | aws-hrnn | Predicts items a user will interact with. A hierarchical recurrent neural network which can model the temporal order of user-item interactions.
| N - requires meta data | aws-hrnn-metadata | Predicts items a user will interact with. HRNN with additional features derived from contextual (user-item interaction metadata), user medata (user dataset) and item metadata (item dataset)
| N - for bandits and requires meta data | aws-hrnn-coldstart | Predicts items a user will interact with. HRNN-metadata with with personalized exploration of new items.


### Content

The [personalize_ranking_example.ipynb](personalize_ranking_example.ipynb)


### License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.



