Amazon Personalize User Personalization
---

Combining an HRNN-based algorithm for relevance with automatic exploration of new/cold item recommendations, the aws-user-personalization recipe provides the most flexibility when building user personalization use-case. Although the Interactions dataset is the only required dataset, this recipe will take advantage of all three dataset types (Interactions, Items, Users) if provided. In addition, it can optionally model on impression data if provided in your Interactions dataset and when streaming real-time events using an Event Tracker.

Although we provide sample notebooks for the HRNN-\* recipes for posterity, it is recommended that you start with the user-personalization recipe.
## Samples

### User-Personalization (recommended)

The [user-personalization-with-exploration.ipynb](user-personalization-with-exploration.ipynb) demonstrates how to use an Interactions and Items dataset to create solution and campaign that balances making recommendations based on relevance (exploitation) and exploring recommending new/cold items. A Users dataset could have been used as well but is not included in this sample. This sample also demonstrates how to include impression data in the Interactions dataset and in PutEvents API calls.

### HRNN (legacy)

The [personalize_hrnn_example.ipynb](personalize_hrnn_example.ipynb) uploads the 'past' data from temporal splitting and evaluates the recommendation against the held-out 'future' ground truth.

### HRNN-Metadata (legacy)

Meta-data is ubiquitous. User zipcodes and device types can be useful indicators of preference; item categories and tags can be useful patterns in decision making; click and purchase events may imply different utilities to the user.

This [personalize_hrnn_metadata_example.ipynb](personalize_hrnn_metadata_example.ipynb) shows how these useful information can be uploaded to our system to aid recommendation. A caveat is that the improvements of meta-data recipes depend on how much information can be extracted from the provided meta-data. Movie genres may be less useful compared with movie ratings, or better, directors and stars.

### HRNN-Metadata (legacy) + Contextual Recommendations + Event Tracker

In this example we are going over how to leverage Metadata and Context to provide best airline recommendations for users based on historical ratings of such across multiple cabin types with user's location as user metadata

This [personalize_hrnn_metadata_contextual_example.ipynb](personalize_hrnn_metadata_contextual_example.ipynb) shows how these useful information can be uploaded to our system to aid recommendation. A caveat is that the improvements of meta-data recipes depend on how much information can be extracted from the provided meta-data.

*Note that contextual metadata can also be used with the User-Personalization recipe.*

### HRNN-Coldstart (legacy)

An important functionality that meta-data, particularly item meta-data, provides is to generalize to new 'cold-start' items. Examples include new releases, new products, or live items. Without personalization, a global policy to introduce these new items may incur large promotional costs. Personalized 'cold-start' helps reduce these costs.

This [personalize_coldstart_demo.ipynb](personalize_hrnn_coldstart_example.ipynb) shows how we may personalize item 'cold-start' by exploring only in the same movie genres that the user would be interested in.

*Note that the item cold start capabilities of the User-Personalization recipe are preferred over the legacy HRNN-Coldstart recipe. Therefore, it is recommended that you start with the User-Personalization recipe for cold item scenarios.*

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
