Amazon Personalize Related Items
---

The 'SIMS' recipe allows your system to recommend what items are most similar to a specific item using an item-to-item collaborative filtering algorithm. It is faster to train and easier to interpret. This recipe is commonly used on item detail pages where you want to display similar items to the current item based on the behavior of users who also interacted with the item.

## Sample

The [personalize_sims_example.ipynb](personalize_sims_example.ipynb) uploads the 'past' data from temporal splitting and evaluates the recommendation against the held-out 'future' ground truth. The results compare favorably with a popularity-based recommendation baseline. We also include examples showing that different "cause" items would lead to different 'sims' results.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.




