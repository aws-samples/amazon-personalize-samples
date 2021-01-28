Amazon Personalize User Personalization
---

Combining an HRNN-based algorithm for relevance with automatic exploration of new/cold item recommendations, the aws-user-personalization recipe provides the most flexibility when building user personalization use-case. Although the Interactions dataset is the only required dataset, this recipe will take advantage of all three dataset types (Interactions, Items, Users) if provided. In addition, it can optionally model on impression data if provided in your Interactions dataset and when streaming real-time events using an Event Tracker.

Although we provide sample notebooks for the HRNN-\* recipes for posterity, it is recommended that you start with the user-personalization recipe.
## Samples

### User-Personalization 

The [user-personalization-with-exploration.ipynb](user-personalization-with-exploration.ipynb) demonstrates how to use an Interactions and Items dataset to create solution and campaign that balances making recommendations based on relevance (exploitation) and exploring recommending new/cold items. A Users dataset could have been used as well but is not included in this sample. This sample also demonstrates how to include impression data in the Interactions dataset and in PutEvents API calls.

### Contextual Recommendations + Event Tracker

In this example we are going over how to leverage Metadata and Context to provide best airline recommendations for users based on historical ratings of such across multiple cabin types with user's location as user metadata

This [user-personalization-with-contextual-recommendations.ipynb](user-personalization-with-contextual-recommendations.ipynb) shows how these useful information can be uploaded to our system to aid recommendation. A caveat is that the improvements of meta-data recipes depend on how much information can be extracted from the provided meta-data.


*Note that the item cold start capabilities of the User-Personalization recipe are preferred over the legacy HRNN-Coldstart recipe. Therefore, it is recommended that you start with the User-Personalization recipe for cold item scenarios.*

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
