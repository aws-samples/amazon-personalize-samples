# Amazon Personalize Cheat Sheet

## Personalize Terminology

1. **Dataset Groups:** 
A dataset group is a logical container for up to five dataset types, only one of which (item-interactions) is required across all recipes. Check the recipe documentation for the dataset type(s) considering during training. Multiple dataset groups are also supported. The dataset types that can be used in a dataset group are as follows;

    **a) Item-interaction data** (required for all recipes/use cases) must consisting of at minimum a `timestamp`, a `user_id`, and an `item_id` column/field. Each row should represent a positive interaction between user and item at a specific time. Personalize assumes that all item interactions are positive so if you have examples of user interactions with items that are not positive (such as customers leaving a bad review of an item or disliking an item) you should not include those interactions in your dataset or exclude them from training. Optional reserved columns `event_type` and `event_value` can be included which represent the type of interaction (e.g., `click`, `add-to-cart`, `watch`, `favorite`, `purchase`, etc) and a value associated with the event (watch duration, rating value, etc). Up to five additional custom columns can be added to this dataset which should represent contextual information of the event such as temporal values (time of day, day of week), current weather condition, current device type, current location, etc. **This is the only required dataset for most use cases.**

    **b) Items metadata** (required for similar-items and item-attribute-affinity) can include custom structured and unstructured fields for each item. Structured fields can be numeric or categorical. A single unstructured field is supported which should be a textual value in natural language (i.e., product description, movie plot, article text, etc). Up to 100 custom fields are supported in this dataset. An `item_id` column is required and must be populated for all items. An optional reserved column `creation_timestamp` can also be included which should be populated with a Unix timestamp value representing when the item was created. It is used to control the eligibility of new items for exploration with the user-personalization recipe (in which they receive a bonus to their score which is inversely proportional to the number of interactions/impressions the item has in the dataset) and can also be used in filters to include/exclude items in recommendations based on the item's age.

    **c) User metadata** (optional for all recipes) can include optional information about users that can influence the ranking of items for some of the recipes. Values included in this dataset should be information that never or rarely changes for users such as gender, age, subscription/membership tier, and so on.

    **d) Action metadata** (required only for the next-best-action), not used in other recipes, consists of at minimum an `action_id` field. Can consist of additional fields such as `creation_timestamp` which controls the eligibility of new items for exploration, `repeat_frequency`, which is the number of days after recommending an action to wait before recommending it again, and `action_exploration_timestamp` which represents the time (in unix epoch time) after which to cease recommending an action.

    **e) Action-interaction data** (optional of next-best-action) recommended for next-best-action use case consists at minimum of a `timestamp`, a `user_id`, an `action_id`, and an `event_type` representing a user taking an action (or choosing not to take an action when prompted) at a specific point in time. The `event_type` contains information on the user's response and can consist of `“taken”`, `“not taken“`, and `“viewed“`.

2. **Recipe:**
This refers to a specific type of model structure or ML algorithm designed for a specific family of business use cases. For example, the user personalization recipe will produce item recommendations that are likely to appeal to an individual user.

3. **Solution:**
A combination of dataset group, recipe, and configuration - basically the framework to train a model for a specific use case.

4. **Solution Version:**
A trained version of a model/solution. A solution for which a contained model has been trained for a specific use case, can be used to run batch recommendation (inference) jobs or deployed as a campaign for real-time inference.

5. **Domain Recommenders vs Custom**
A domain recommender (aka use case optimized recommender) is a recommender optimized for a use case in one of two specific domains: E-commerce or Video on Demand to facilitate the easier onboarding in these cases. A custom solution supports a broader array of use cases but leaves a lot of configuration up to the developer. There is nothing you can do in a domain dataset group that you can't also do in a custom dataset group. However, the reverse is not true.

6. **Campaign:**
A deployed solution version behind an auto-scaling real-time inference endpoint. After the campaign finishes deploying, you can get recommendations with the [GetRecommendations](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetRecommendations.html) or [GetPersonalizedRanking](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetPersonalizedRanking.html) API operations.

7. **Event Tracker:**
A mechanism that allows new events/interactions to be streamed to an Amazon Personalize dataset group in real-time via the [PutEvents](https://docs.aws.amazon.com/personalize/latest/dg/API_UBS_PutEvents.html) API. An event tracker performs two tasks: persists new events/interactions to the interactions dataset so they are available for the next retraining and makes recent events/interactions for each user available to models trained with recipes that support [real-time personalization](https://docs.aws.amazon.com/personalize/latest/dg/use-case-recipe-features.html#about-real-time-personalization) (User-Personalization(-v2), Personalized-Ranking(-v2), Recommended-For-You (E-COMM), and Top-Picks-For-You (VOD)). Real-time personalization is a feature where recommendations will adapt for users in near-real-time based on recent events/interactions (usually within 1-2 seconds of PutEvents being called). 

8. **Domain Recommenders (aka Use Case Optimized):**
When used in the context of Amazon Personalize this refers to a collection of preconfigured custom recipes that streamline the end-to-end process. Unlike with custom solutions where developers need to go through several steps to deploy an API capable of serving real time predictions, Domain Recommenders create and deploy model serving API’s directly from a dataset group, they also handle the deployment of some relevant filters, some aspects of maintenance of a deployed model such as retraining. However, this streamlined approach comes with some limitations such as not supporting batch inference, not being able to control retraining frequency, and others.

9. **Contextual Metadata:**
This refers to metadata relevant to the use case and specific to an interaction such as the user's current device type, the user's current location, temporal data such as time-of-day/day-of-week, or the current weather condition. During training, this allows Amazon Personalize to learn patterns of user behavior based on different context. Therefore, contextual metadata should be provided with historical interaction data and real-time event/interaction data. Then at inference, the current contextual values for the user are provided to Personalize so that recommendations are more relevant to the current context. Contextual metadata is only supported for a subset of recipes so check the documentation.

## Is Amazon Personalize a Good Fit?

Amazon Personalize is a great platform for operating a recommendation system at scale on AWS but it is not appropriate for any and all personalization or recommendation scenarios. The chart below is a rough guide for good and bad fits. Generating “Next Best Offer” is not supported by the service.

|Good Fit	|Bad Fit	|
|---	|---	|
|Recommending items to known users. Movies to users based on their watching history or products to retail users based on purchase and browsing behavior. Personalize will update new items being inserted into its dataset within 2 hours.	|Recommendations based only on explicit user or item metadata flags and there is no record of user history.	|
|Recommending items to new users based on their in-session behavior.	|Low data volumes for users, items, and interactions (see table below).	|
|Recommending new items to new users. Personalize can integrate new items into its reccomendations within 2 hours	|Personalize does not support explainability (exposing why a user is getting certain recommendations) and customers cannot bring their own models. For these two features, Amazon SageMaker is a better approach. 	|
|Media, Retail, Publishing and Travel & Hospitality are a good fit. 	|Finance, Insurance companies with limited inventory (types of insurance, bonds etc) and user behavior/interactions with the items being recommended.	|
|Companies whose technical teams are understaffed with large project backlogs - Personalize is MUCH quicker to deploy than a custom built recommendation system	|Use cases where you will only be recommending a small percentage items in your interaction history to your users (such a financial service use case where you have a history of bank transactions and account openings but are only interested in a recommendation on what sort of new account to recommend to a user).	|
|Companies who already track clickstream events - this makes using Amazon Personalize and benefiting from its ability to update user reccomendations in near real time easier.	|Companies who currently don't track clickstream events and lack the technical capacity to feed interactions to Amazon Personalize as they occur.	|
|Companies with large item catalogs (videos, products, content whatever) where the typical user journey involves a search through the catalog of a reasonable length before an item is purchased / viewed	|Companies who are soley intrested in recommending very new items with short shelf lives to their customers. Personalize works well in publishing and news for example but can't replace editorial curation of a breaking news section without substanital effort.	|
|More than 50 users and 50 items and 1000 interactions with items that are still active in your dataset	|More than 5M active items and you need to be capable of recommending them all to a customer	|

## Use Cases By Recipe

What kind of use cases can be solved and how?

1. **Personalized Recommendations** `User-Personalization(-v2)`/`Recommended For You`/`Top Picks for You`:
    1. This is a primary use case of Amazon Personalize, using user-item-interaction data to build a recommendation model that directly targets each user, and allows for new users to be added on the fly with PutEvents without re-training. PutEvents also allows for the users to see recommendations that are based on their most recent behavior so you do not lose out on that additional info. Also you can feed in context specific components like device type or location to improve results.
    2. You can also add item and user metadata in order to better enrich the model, or to filter recommendations by attribute.
    3. For Video On Demand and Retail use-cases, the domain recommenders “Top picks for you” and “Recommended for you” allow you to get up and going quickly and with less operational overhead.
2. **Recommending Items to New Users** `User-Personalization(-v2)`/`Recommended For You`/`Top Picks for You`:
    1. New users (aka cold users) can be added to your existing User-Personalization solutions by leveraging the PutEvents feature. Each new user starts with a representation in the service that returns popular items (items that other cold users frequently interact with first). This representation is shifted by the user’s behavior. As they interact with content within the application and the events are sent by the application to Personalize, recommendations are updated without having to re-train the model. This delivers up to date personalization without constant retraining.
    2. Metadata for new users can be added to the Users dataset using the PutUsers API or dataset import jobs. This data is incorporated into the model at the next retraining.
    3. Contextual metadata for new users, such as their current location or device type, can be provided when retrieving recommendations to influence recommendations.
3. **Recommending New Items** `User-Personalization(-v2)`/`Recommended For You`/`Top Picks for You`:
    1. This is incredibly useful when you have new items (aka cold items) that need to be showcased to users with some form of personalization. This allows for the items to be recommended without historical precedent based on metadata factors.
    2. This can also be used with incrementally updating your Items dataset to more easily cold-start new items. 
    3. Lastly, this approach leverages an exploration capacity to help you quickly determine which results make sense, and which do not for recommendations, a far better approach than just blindly pushing new content.
4. **Re-Ordering by Relevance** `Personalized-Ranking(-v2)`:
    1. Uses the same HRNN algorithm underneath User-Personalization(-v2) but takes in a user AND a list of items. This will then look at the collection of items and rank them in order of most relevant to least for the user. This is great for promoting a pre-selected collection of items and knowing what is the right thing to promote for a particular user or for personalizing search results.
5. **Related Items** `Similar-Items`/`SIMS`/`Because you watched X`/`More like X`/`Frequently bought together`/`Customers who viewed X also viewed`:
    1. `Similar-Items`: Deep learning model that considers both interaction data and item metadata (optional) to balance related item recommendations based on interaction history and item metadata similarity. Useful when you have less interaction data but have quality item metadata or when you frequently introduce cold/new items.
    2. `SIMS`: Pretty simple idea, implemented via item-item collaborative filtering but basically looks at how people are co-interacting with particular items and then determine how similar items are at a global level based on interaction data. Does not consider item or user metadata and is not personalized to each user. Useful when you have a lot of relevant interaction data, do not have a lot of cold items (changing catalog), and/or lack item metadata.
    3. For Video On Demand and Retail use-cases, the domain recommenders “Because you watched X”, “More like X”, “Frequently bought together”, and “Customers who viewed X also viewed” allow you to get up and going quickly and with less operational overhead.
6. **Frequently Bought Together (cross selling)** `SIMS`/`Similar-Items`/`Frequently bought together`:
    1. SIMS trains on interactions only, looking at co-interactions of items to identify the items that are most co-interacted with the input item. Similar-Items trains on interactions too but also considers item metadata to balance related item recommendations based on co-interactions and item similarity. Since the goal of FBT/cross-selling is to find items that are bought together, SIMS is typically a better match. However, the interactions data must provide enough of the right signal to produce a quality SIMS model (see potential issues below).
    2. The key is preparing the right data used to train a model in Personalize and choosing the right recipe. For example, train a SIMS model on purchase event data only and, if possible, train only on purchase data where customers have purchased multiple items and/or purchased items across multiple categories. This will bring the desired behavior to the model and create diversity in recommendations (which is what you want for this use case).
    3. SIMS can also be combined with Personalized-Ranking to rerank recommendations from SIMS before presenting them to the user. This provides a personalized order of items that are frequently bought together. You would call SIMS first to get a candidate set of related items for a given item and then pass those items and the userId to personalized-ranking to rerank them for the user. To optimize latency and cost, the SIMS recommendations could be generated ahead of time using batch inference and stored in a low-latency key/value store such as DynamoDB. At run-time, the related items are fetched from DynamoDB and then reranked using the GetPersonalizedRanking API.
    4. The retail domain recommender “Frequently bought together” will allow you to get up and going quickly and with less operational overhead. Behind the scenes this recommender is using SIMS trained on "Purchase" events.
    5. Potential challenges (and suggestions): 1/ If you have a poor distribution of purchase events across your catalog, SIMS may not be the best fit. For example, when the input item to SIMS is cold (no co-interactions), the model will return popular items. This is not a good result for a cross-selling/frequently bought together use case. 2/ Popularity bias can result in the same popular items appearing in SIMS responses even when co-interactions are present. This can be controlled by adjusting the "popularity_discount_factor" hyperparameter on SIMS and Similar-Items and using a filter to require recommended items to come from one or more categories related to the input item. See this blog post for more details: https://aws.amazon.com/blogs/machine-learning/introducing-popularity-tuning-for-similar-items-in-amazon-personalize/
7. **Most Popular Overall** `Popularity-Count`/`Most-Popular`/`Most-Viewed`/`Best-Sellers`:
    1. Not machine learning, just a baseline from counting the most commonly interacted with items. This recipe is useful for popular item recommendations or for creating a baseline of offline metrics that can be used to compare against solution versions created using other user-personalization recipes with the same datasets.
    2. For Video On Demand and Retail use-cases, the domain recommenders “Most popular”, “Most viewed”, and “Best sellers” allow you to get up and going quickly and with less operational overhead.
8. **Trending Items** `Trending-Now`:
    1. Also not machine learning - represents items for which the difference in the number of interactions occurring in the most recent 30 minute time-step and those occurring in the previous 30 minute time-step is the greatest. This is designed to capture items that are starting to go viral not those that are the most popular in the catalog (for that use one of the Most Popular Overall recipes)
9. **User Segmentation** `Item-Affinity`/`Item-Attribute-Affinity`:
    1. Create segments of users based on their affinity to specific items in your catalog or their affinity to item attributes. Excellent match with marketing campaigns where you’re looking to target users who will have an interest in specific items you’re looking to promote or items similar to existing items.
10. **Next Best Action** `Next-Best-Action`
    1. Create a model which predicts the likelihood a user taking a particular action at a point in time. Can be setup to predict the likelihood of a user taking an action by themselves or when prompted (recommended). Unlike other personalize recipes the score in this case is intended to be a human understandable probability suitable for downstream use in tasks like expected value calculations.

## Killer Features:

1. [Domain Optimized Reccomenders](https://docs.aws.amazon.com/personalize/latest/dg/domain-dataset-groups.html): recommenders for Video On Demand and Retail use cases
    1. A *Domain dataset group* is an Amazon Personalize container for domain specific pre-configured resources, including datasets, recommenders, and filters. Use a Domain dataset group if you have a streaming video or e-commerce application and want to let Amazon Personalize find the best configurations for your recommenders.
2. Contextual Recommendations
    1. Allows you to fine-tune recommendations based on state that varies with the interaction rather than specific to the user or item. Think the user’s current location, device/channel being used, time of day, day of week, etc. 
    2. See this blog post for a detailed example: https://aws.amazon.com/blogs/machine-learning/increasing-the-relevance-of-your-amazon-personalize-recommendations-by-leveraging-contextual-information/
    3. See this blog post for an example of how to use CloudFront to collect this sort of context to populate Get Recommendation requests in near real time: https://aws.amazon.com/blogs/machine-learning/recommend-and-dynamically-filter-items-based-on-user-context-in-amazon-personalize/
    4. This feature requires the contextual metadata field values to be provided in historical data (interactions data), in events sent to an Event Tracker via PutEvents (if used), and at inference when calling GetRecommendations or GetPersonalizedRanking APIs.
    5. Only supported by some recipes (user-personalization(-v2), personalized-ranking(-v2), recommended-for-you, top-picks).
3. Interaction and Metadata Filtering
    1. Filter recommendations based on the user’s interaction history or the metadata attributes for the items or current user. Very handy in nearly all Media or Retail workloads. For example, exclude recently purchased or out of stock items or include/exclude recommended items based on category or genre.
    2. See this blog post for details: https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/
4. Promotional Filters
    1. Promote specific items in recommendation responses based on a filter expression and control how many items in the recommendation response are promoted. For example, require that 30% of the recommended items have been recently released/published (where you control the timeframe) or require that 25% of the recommended items are private label or currently on sale.
    2. See this blog post for details: https://aws.amazon.com/blogs/machine-learning/customize-your-recommendations-by-promoting-specific-items-using-business-rules-with-amazon-personalize/
5. Batch Inference
    1. Great for exporting large quantities of recommendations to files for caches, for email campaigns, or just general exploration.
6. AutoScaling Campaigns/Recommenders
    1. For real time inference endpoints (campaigns and recommenders), the service will automatically scale to meet your traffic demands if a particular campaign or recommender is over-subscribed. It will then also reduce to your requested minimum capacity when the traffic volume abates. 
7. Unstructured Text as Item Metadata
    1. Add your product descriptions, video plot synopsis, or article content as an item metadata field and let Personalize use natural language processing (NLP) to extract hidden features from your text to improve the relevance of recommendations.
    2. If your textual data is very verbose, consider using an LLM to summarize your textual data before sending it to Personalize.
8. PutEvents
    1. Allows for applications to update Personalize in real time with changes in intent from user behavior. This means that each subsequent request for a user can adapt to that intent WITHOUT retraining. Note that regular retraining is still required to learn patterns across all users.
9. PutItems/PutUsers
    1. Allows for applications to add/update individual or mini-batches of items or users without having to upload the entire items and users datasets.
    2. See FAQs below for more detail.
10. KMS Integration
    1. All data can be encrypted using a customer managed key, all data is encrypted regardless.
11. No Information Sharing
    1. All customer data is fully isolated and is not leveraged in order to improve the recommendations of Amazon or any other party.
    2. Models are private to the customer’s AWS account.

## Video Series:

1. Introduction To Amazon Personalize: https://youtu.be/3gJmhoLaLIo
2. Understanding Your Data with Amazon Personalize: https://www.youtube.com/watch?v=TEioktJD1GE
3. Solving Real World Use Cases with Amazon Personalize: https://www.youtube.com/watch?v=9N7s_dVVWBE
4. Getting Your Amazon Personalize Recommendations in Front of Your Users: https://www.youtube.com/watch?v=oeVYCOFNFMI
5. Get Your Amazon Personalize POC to Production: https://www.youtube.com/watch?v=3YawVCO6H14
6. Enhancing Customers Experiences with Amazon Personalize (including a demo of the [Retail Demo Store](https://github.com/aws-samples/retail-demo-store)): https://youtu.be/71dWFhzw7iw
7. Personalized Search: https://www.youtube.com/watch?v=w8Ut02535_I&ab_channel=AmazonWebServices 

## FAQs:

1. How often should I retrain?
    1. Retraining frequency is determined by business requirements. How often do you need to learn globally about your users and their behavior with items? How often do you need to include new items? The answers determine how frequently you should train. Generally speaking, most customers retrain weekly. See below for more detailed guidance.
    2. If using the “aws-user-personalization”, “aws-user-personalization-v2”, “recommended-for-you”, or “top-picks” recipes, the service will automatically update the solution version in the background every 2 hours (at no additional cost). This auto update process will bring in new items added since the last update so they can start being recommended to users (i.e. cold starting items). This works in coordination with the explorationWeight parameter set on the campaign/recommender to control the weight placed on recommending new/cold items vs relevant items (explore/exploit). The auto-update process is NOT retraining.
    3. If the 2 hour auto-update is not frequent enough for introducing new items, you can manually create a new solution version with trainingMode=UPDATE and update the campaign more frequently (i.e. hourly). This essentially does the same thing as the auto-update, just on a custom frequency. However, there is a cost for training hours for doing this manually.
    4. Regardless of the auto or manual update mode process taken, this does not fully retrain the model. For most use cases weekly retrainings are sufficient. To be more precise in retraining frequency, another approach is to monitor online metrics. When they start to trail off (i.e. model drift), it may be time to retrain. Note personalize does have an auto retraining capability for more information on [see here](https://docs.aws.amazon.com/personalize/latest/dg/solution-config-auto-training.html) by default personalize solutions retrain once a week unless you turn off automatic retraining or change the cadence of the automatic retraining.
2. How do I add a new user?
    1. If you are using the PutEvents API, the new user exists as soon as you log their first event/interaction. If you are not leveraging PutEvents, then the user will exist in the system as soon as you have retrained a model that contains their behavior in your interactions dataset.
    2. If your user is not known (a new anonymous user before signup) you can still work to cold-start them. If you can assign a new UUID for their user and sessionID immediately, then you can continue the process as defined above to cold start a user.
    3. If that path does not work, you can still generate a new UUID for the sessionID, call PutEvents without a userID, and then continue to specify the same sessionID after a valid userID has been generated for them. When you retrain, Personalize will combine the historical data, with PutEvents data, and when it sees matching sessionIDs it will combine all prior anonymous interactions together with non-anonymous interactions for the user. This would allow you to specify the history before they had a valid internal userID. 
    4. You can add/update users individually or in mini-batches with the PutUsers API. However, only users with interactions will receive personalized recommendations either after (re)training or when cold started with the PutEvents API.
3. How do I add a new item?
    1. There are two ways to add items to the items dataset: 1/ Add new items to the items dataset by uploading the dataset using a dataset import job, or 2/ add items individually or in mini-batches using the PutItems API.
    2. New items will be incorporated into recommendations after retraining if interactions also exist (all recipes) or cold-starting new item recommendations with or without interactions after the solution has been updated (trainingMode = FULL/UPDATE for aws-user-personalization(-v2) and HRNN-Coldstart only).
    3. For example, you can organically stream new items into your historical dataset by placing banners for new releases. Anything that causes a user to interact with the new items and for that action to be logged can improve recommendations after the next training.
4. How do I filter results for certain conditions?
    1. Using the filters feature for either Interaction (https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) or Metadata information (https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/).
    2. Filtering based on interaction history currently only considers the most recent 100 real-time interactions (PutEvents API) and the most recent 200 historical interactions in the dataset at the time of retraining. All event types are included in the 100/200 limits. This can be raised to 2000 per event type by filing a service ticket
5. I need to filter items based on a rolling date value. What are my options?
    1. Filters support dynamic values with range operators (i.e. <, <=, >, >=). Add date values expressed as Unix timestamps to your Items dataset or reuse the `CREATION_TIMESTAMP` reserved column for filtering on item age. Then create a dynamic filter that compares a passed-in date value (passed in at inference using the `filterValues` parameter) to the date value for items. For example, `INCLUDE ItemID WHERE Items.CREATION_TIMESTAMP > $TIMESTAMP` where `$TIMESTAMP` can be a date from the recent past.
6. Why should I use Amazon Personalize over a custom solution?
    1. Assuming your data and use cases are aligned, this is a great way to get a best in class model in front of the end users faster. While handling the operational burden of running a recommendation system at scale, Personalize also frees you up to improve feature engineering, data collection, user experiences, or solve other problems.
7. I have a use case where my customers purchase or interact with items in my catalog infrequently (e.g. purchasing a car). Is Personalize still a good fit?
    1. Yes, Personalize can still be put to use effectively for this type of use case. For example, a Similar-Items model can be trained based on all user activity such as browsing or purchase history (online and/or offline) and then used for related item recommendations on item detail pages. This allows you to leverage recent activity across all active users to make relevant recommendations to anonymous/returning/cold users.
    2. Real-time recommendations are also effective here since Personalize is able to learn from a user’s current interest and adapt recommendations quickly. For example, recommend popular items initially and then quickly personalize recommendations after a few interactions are streamed using the PutEvents API.
8. Should I use AutoML?
    1. No, the recipes solve different use cases. Take the time to select the most appropriate recipe for the use-case and skip this feature.
9. Should I use HPO / How often?
    1. Infrequently. Take the results of one HPO job and use them explicitly in the solution config for a new solution for several retrainings. Then run HPO again and repeat. Realistically, tuned parameters should not shift much between training jobs. This approach will keep your training times, and therefore costs, lower than running HPO for all training jobs without sacrificing model quality.
10. How can I predict the cost of training?
    1. For the user-personaliztion-v2 and personalized-ranking-v2 recipes, training costs are based on the number of interactions (rows) in your interactions dataset. If you're unsure of the number of rows in this dataset, you can run a dataset analysis job (no charge) from the Personalize console. The results of this job will provide many useful statistics on your datasets, including the number of rows in each dataset type. For these recipes, Personalize will train on up to 3B interactions. If you have more than 3B interactions, you will be charged for 3B. To reduce the number of rows in this dataset, you can export your current interactions dataset, delete the dataset, trim the exported data, and re-import the trimmed dataset. Since deleting the dataset from an active dataset group can result in downtime for real-time recommendations, you can instead import your trimmed dataset into a new dataset group, retrain in the new dataset group, and switch your application to use the new model(s) in the new dataset group. Be sure to delete your old dataset group after making this trasition.
    2. For all of the other custom recipes, unfortunately there really is not a great way to estimate training costs beforehand, we do have some testing that has been done on the MovieLens dataset. For example using `User-Personalization` it takes around  6 human hours for the training on 25M interactions but less than 1 human hour to train on 100k interactions. Because training is sharded over multiple hosts, the actual hours are, 53.9 hours for 50M and 2.135 hours for 100k. Billing is done on the actual hours, not the human ones.
11. How can I predict the cost for real-time recommendations?
    1. When you create a campaign or recommender for real-time recommendations, Amazon Personalize spins up dedicated compute resources that will remain provisioned in order to meet your expected minimum throughput requirements (Transactions per Second or TPS for campaigns; Requests per Second or RPS for recommenders). You are billed based on the maximum of the minimum TPS/RPS on the campaign/recommender or the actual number of requests. 
    2. If your campaign/recommender is idle (i.e., no requests being sent to it) or the number of requests is below the minimum provisioned TPS/RPS, you will be charged for the number of requests represented by the minimum provisioned TPS/RPS. Therefore, it's important to not leave idle campaigns/recommenders running (unless you intend to) or overprovision your campaigns/recommenders by setting their minimum provisioned TPS/RPS too high.
    3. The service will automatically scale up for you if your traffic exceeds the minimum provisioned TPS/RPS on the campaign/recommender, and it has proven to be a valuable tool for many of our customers. A capacity buffer is allocated above the minimum provisioned TPS to allow the service to absorb increases in request load while it scales out. Auto-scaling can take 10-15 minutes to complete step changes.
    4. If you know you are going to have a large and sudden spike of activity such as a flash sale or promotional event, use an automated process to update the provisioned capacity to meet the new need, then throttle it down later if you cannot wait 10-15 minutes for the service to auto-scale.
    5. The Amazon Personalize Monitor project provides a CloudWatch dashboard, custom metrics, utilization alarms, and cost optimization functions for Personalize campaigns: https://github.com/aws-samples/amazon-personalize-monitor
12. How can I tell if a Personalize model is providing high quality recommendations?
    1. Personalize provides offline metrics for each solution version that measure the accuracy of predictions from the model against held out data from the interactions dataset. Use these metrics to provide a directional sense of the quality of a solution version against other versions. 
    2. Online testing (i.e. A/B testing) is always going to be the best measure of the impact of a model on business metrics against a control experience. 
    3. When you are comparing Personalize models against an existing recommendation system, all the historical data is initially biased towards the existing approach. Often the offline metrics do not reflect what a user MAY have done if they were exposed to something else (how could they, the data does not reflect it). So worth noting this effect, and the bandit based exploration Personalize can do to organically learn better from your users. Therefore running an online test for a few weeks **before** actually starting a test to measure results is recommended.
    4. See this blog post for details: https://aws.amazon.com/blogs/machine-learning/using-a-b-testing-to-measure-the-efficacy-of-recommendations-generated-by-amazon-personalize/
13. How can I optimize for cost?
    1. DO NOT USE AUTOML!
    2. DO NOT START WITH HPO - build something working first, optimize last.
    3. Turn off automatic retraining and Re-Train based on business requirements only. See FAQ question for details.
    4. Rely heavily on auto-scaling by setting the minimum provisioned TPS low unless it negatively impacts your throughput / latency targets.
    5. Consider using batch recommendations when the use-case aligns with a downstream batch process such as email marketing. Since batch recommendations run against a solution version, they do not require a campaign.
    6. The Amazon Personalize Monitor project provides some cost optimization features for optimizing campaign provisioning as well as alerting and deleting idle/abandoned campaigns: https://github.com/aws-samples/amazon-personalize-monitor
    7. You do not need to draw a new series of recommendations every time a page is refreshed. Use clever caching strategies. Users will likely find it unpleasant if a large number of assets on a page change merely because users view details on an individual product or piece of content. In addition new users will have very similar recommendations the first time they visit a page. Recommendations for each device type and other piece of contextual metadata and their unique combinations can be cached and shown to a new user at the start of a session. A personalized recommendation can then be drawn after some interactions are collected for the user.
14. How do I provide high quality recommendations for new (cold-start) users and items in the user-personalization recipe?
    1. For cold-start users higher quality recommendations can be generated by feeding contextual metadata in with the get recommendation request (what device type the user is logging in from, where they are logging in from ect). Personalize also updates to new user interactions fed to it through `putEvents` in near real time so while the initial recommendation quality for a new user may not be ideal - much higher quality recommendations can be shown to the user during the session.
    2. For cold-start items submit them to personalize through the put items function. These items will be picked up by personalize within ~2hours worst case - usually faster. If exploration is enabled new items will receive a bonus to their score so that they are shown to more users.
15. How does Exploration work?
    1. For most recipies exploration works as follows:
        1. Items are separated into items eligible for exploration and items ineligible for exploration. This eligibility is determined by comparing the items `creation_timestamp` (in the items metadata) to the current time minus the `explorationItemAgeCutoff` (a parameter set for the campaign) in days. If the creation timestamp is within that window the item is eligible for exploration.
        2. The item receives a bonus to its estimated user affinity score which is inversely proportional to its interactions count / impressions count. This count is updated approximately every 2 hours, new items are also picked up at this time
        3. The item also has a small amount of noise added to it to represent potential uncertainty in the user-item affinity learned so far and to assist with discoverability
    2. For newer recipes exploration (user-personalization-v2 and personalized-ranking-v2) is much simpler - .1% of items in recommendations will automatically be items added in the past 30 days.
16. How do I use contextual metadata?
    1. Contextual metadata is additional information known about the user, or the session at the time a recommendation request is made that might change a users preferences. Examples include the weather or location for food delivery, ongoing sales and other events for retail use cases and the device type a user is logging in on for media use cases.
    2. Contextual metadata must be defined in the schema and supplied as part of the historical interaction data that the model is trained on as well as in events sent to an Event Tracker (if being used). It MUST also be supplied as part of a `GetRecommendations` or `GetPersonalizedRanking` API request.
    3. Contextual metadata is not for information about the interaction that is only known after the interaction such as what kind of discount the item was purchased at or the quantity of an item purchased.
17. What are the best ways to use caching with Amazon Personalize? How should I integrate Personalize with my existing applications?
    1. Check out the [Personalization APIs](https://github.com/aws-samples/personalization-apis) solution: Real-time low latency API framework that sits between your applications and recommender systems such as Amazon Personalize. Provides best practice implementations of response caching, API gateway configurations, inference-time item metadata, automatic contextual recommendations, and more.
18. What is the best way to compare Personalize to an existing user experience or another recommendation system?
    1. A/B testing is the most common technique for evaluating the effectiveness of Personalize against online metrics.
19. How do incremental records influence recommendations for the current user?
    1. Amazon Personalize allows you to import [interactions](https://docs.aws.amazon.com/personalize/latest/dg/importing-interactions.html), [users](https://docs.aws.amazon.com/personalize/latest/dg/importing-users.html), and [items](https://docs.aws.amazon.com/personalize/latest/dg/importing-items.html) incrementally. These can affect recommendations for the current user in different ways depending on whether the a new solution version has been trained and what type of trainingMode was used see https://docs.aws.amazon.com/personalize/latest/dg/how-new-data-influences-recommendations.html
20. How can Personalize be used to recommend items based on location, near a location, or the user's current location?
    1. Personalize does not natively support/interpret geo-location data elements such as latitude/longitude, geohash, etc. However, location information can be represented in categorical fields using values such as city IDs, postal codes, state IDs/codes, DMA IDs/codes, etc. These fields can be used in training to learn engagement patterns based on location as well as with filtering to include/exclude items based on their location attributes. An important limitation to keep in mind is that Personalize will only consider the top 1000 distinct values of each categorical field during training. Therefore, the cardinality of categorical fields is an important consideration. When filtering on categorical fields, all values are considered.
    2. Personalize does not support reward based on distance when recommending items. For example, Personalize will not rank items that are closer to a point higher than items farther from a point. Items are always ranked based on relevance.
    3. Recommending items based on location can be accomplished using a Personalize filter (e.g., items with one or more city IDs or postal codes as item metadata).
    4. A more precise and flexible approach is to pair Personalize with a datastore that supports geospatial queries (OpenSearch, Elastic, Solr, MongoDB, most RDMSs, etc). The geospatial query identifies a candidate set of items based on distance and other criteria (e.g., vegetarian restaurants within 5 miles of a point) and then those items are sent to a Personalize model trained with the personalized-ranking(-v2) recipe to rerank those items based on the user's interests. To balance the relevancy from the geospatial search and Personalize, it's typically desirable to adjust the final ranking by considering the scores/ranks from the geospatial search and the reranked items from Personalize. The [Amazon Personalize Search Ranking plugin for OpenSearch](https://docs.aws.amazon.com/personalize/latest/dg/personalize-opensearch.html) automatically performs this additional balanced ranking step.

|Increment	|Recipe	|No retraining	|Retraining trainingMode=UPDATE	|Retraining trainingMode=FULL	|Comments	|
|---	|---	|---	|---	|---	|---	|
|putEvent with new user	|User personalization	|Personalization begins after 1 event, but will be more visible after ~2-5 events with 1-2 seconds delay after the PutEvents call after each event is recorded	|No additional effect beyond the effects described in 'No retraining'	|Personalized recommendations	|The more events streamed, the more personalized the recs become. Impression discounting will occur for cold start items when new users records include impressions data.	|
|putEvent with new user	|Personalized Ranking	|Personalization begins after 1 event, but will be more visible after ~2-5 events with 1-2 seconds delay after the PutEvents call after each event is recorded	|-	|Personalized recommendations	|Using Personalized Ranking, it is more difficult in many cases to see the direct impact of putEvents records as a customer supplied curated list is re-ranked (compared to user-personalization where recomendations are generated from the full vocabulary of items in the catalog based on the learned model behavior/metadata features and user interaction history.)	|
|putEvent with new user	|SIMS	|-	|-	|Included in the model to generate the recommendations	|SIMS doesn't really do personalization so in the context of new users being added with PutEvents, a new user's events are considered in similar item recs only after retraining.	|
|putUser	|User personalization	|-	|-	|Personalized recommendations	|Users added via putUser will be warm users based on the conbination of their known interaction history and userID after the next full retraining.	|
|putUser	|Personalized Ranking	|-	|-	|Personalized recommendations	|Users added via putUser will be warm users based on the conbination of their known interaction history and userID after the next full retraining.	|
|putUser	|SIMS	|-	|-	|No effect	|SIMS doesn't really do personalization so in the context of new users being added with PutUsers, a new user's events are considered in similar item recs only after retraining.	|
|putItem	|User personalization	|-	|Appear as cold start items eligible based on the exploration age cut-off when exploration is enabled.	|Personalized recommendations	|For new/cold start items, recommendations are personalized based on the user's interaction history and item metadata of new/cold start items. Cold start items (eligible based on the exploration age cut-off when exploration is enabled) will be included during the next update. Cold start items will be auto-updated based on impression discounting from interacting generated during exploration. This weighting is non-linear combined with metadata based features but cold start items which are less popular (provided in the impressions field via putEvents will receive less exploration weighting over time)	|
|putItem	|Personalized Ranking	|-	|-	|Personalized only after some interactions	|-	|
|putItem	|SIMS	|-	|-	|New interactions are included in the model to generate similar item recommendations based on co-occurence	|SIMS doesn't really do personalization so in the context of new users being added with PutEvents, a new user's events are considered in similar item recs only after retraining.	|

## Technical Enablement Links:

1. Overall Samples: https://github.com/aws-samples/amazon-personalize-samples
2. Getting Started: https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started
3. POC in a Box 2.0: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/workshops/POC_in_a_box
4. Use Case Based Notebooks: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/core_use_cases
5. Data Science Tools: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/data_science
6. MLOps for Personalize: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops
7. Monitoring/Alerting/Cost Optimization: https://github.com/aws-samples/amazon-personalize-monitor
8. Personalized Marketing Outreach: https://aws.amazon.com/blogs/architecture/amazon-personalize-customer-outreach-on-your-ecommerce-platform/

## Demos/Workshops:

* Media & Entertainment
    * Unicorn Flix
        * Running instance: [https://unicornflix.amplify-video.com](https://unicornflix.amplify-video.com/) 
* Retail 
    * The Retail Demo Store
        * Source: https://github.com/aws-samples/retail-demo-store 
        * Workshops: https://github.com/aws-samples/retail-demo-store#hands-on-workshops

## Technology Partners:

There are several technology partners that provide complementary functionality to Personalize that can accelerate customers getting to production with Personalize or enhancing the ROI on implementing personalization with Personalize.

### Customer Data Platforms - Event Collection/Activating Recommendations

**Segment** is a [Customer Data Platform](https://en.wikipedia.org/wiki/Customer_data_platform). They are an AWS Advanced Technology Partner and hold the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) and [Retail](https://aws.amazon.com/retail/partner-solutions/) competencies.

Segment helps customers with Personalize in the following ways:

* Event collection - this is a core capability of Segment. Customers use Segment to collect clickstream events across their web app, mobile apps, and other integrations. These events are collected, validated, and fanned out to downstream destinations configured by the customer. One of these destinations is Amazon Personalize.
* Customer/user profile identity resolution - because Segment sees events across all channels for a customer's users, they are able to create a unified customer profile. This profile/identity is key to being able to deliver omnichannel personalization.
* Activation across an organization's other marketing tools - because Segment allows customers to create connections to other marketing tools, attaching personalized recommendations from Personalize to profiles in Segment allows customers and downstream partners to leverage those recommendations in their tools.

**Resources**

* Segment CTO video: https://www.youtube.com/watch?v=LQSGz8ryvXU
* Blog post: https://segment.com/blog/introducing-amazon-personalize/
* AWS/Segment Workshops
    * Real-time personalization events: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-5-Real-time-events-Segment.ipynb
    * Customer data platforms and Personalize: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.1-Segment.ipynb
    * Segment/Personalize (legacy workshop): https://github.com/james-jory/segment-personalize-workshop
* Documentation: https://segment.com/docs/connections/destinations/catalog/amazon-personalize/

**mParticle** is a Customer Data Platform. They are an AWS Advanced Technology Partner and hold the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) and [Retail](https://aws.amazon.com/retail/partner-solutions/) competencies.

mParticle helps customers with Personalize in the following ways:

* Event collection - this is a core capability of mParticle. Customers use mParticle to collect clickstream events across their web app, mobile apps, and other integrations. These events are collected, validated, and fanned out to downstream destinations configured by the customer. 
* Customer/user profile identity resolution - because mParticle sees events across all channels for a customer's users, they are able to create a unified customer profile. This profile/identity is key to being able to deliver omnichannel personalization.
* Activation across an organization's other marketing tools - because mParticle allows customers to create connections to other marketing tools, attaching personalized recommendations from Personalize to profiles in mParticle allows customers and downstream partners to leverage those recommendations in their tools.

**Resources**

* AWS/mParticle Workshops
    * Real-time personalization events: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-6-Real-time-events-mParticle.ipynb
    * Customer data platforms and Personalize: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.2-mParticle.ipynb

### Analytics/Measurement/Experimentation

**Amplitude** is an AWS Advanced Technology Partner and holds the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) competency.
Amplitude helps customers with Personalize in the following ways:

* Product insights - Amplitude provides visibility into the event types that lead to conversion through sophisticated funnel analysis. This provides the insight that customers need to optimize their event taxonomy and select the right events and metadata fields to train models on in Personalize.
* A/B test evaluation - Amplitude provides online measurement of A/B tests that can be represented by personalized customer experiences powered by Personalize.

**Resources**

* Workshop: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.5-Amplitude-Performance-Metrics.ipynb
* Blog post: https://aws.amazon.com/blogs/apn/measuring-the-effectiveness-of-personalization-with-amplitude-and-amazon-personalize/

**Optimizely** is a market leading A/B testing platform. They are an AWS Advanced Technology Partner and hold the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) competency.

Optimizely helps customers with Personalize in the following ways:

* A/B test results - a core offering of Optimizely is measurement and reporting of experiments such as personalization techniques.
* Feature flagging - enable/disable personalized experiences

**Resources**

* Workshop: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.6-Optimizely-AB-Experiment.ipynb

### Messaging

**Braze** is a market leading messaging platform (email, push, SMS). They are an AWS Advanced Technology Partner and hold the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) and [Retail](https://aws.amazon.com/retail/partner-solutions/) competencies.

Braze helps customers with Personalize in the following ways:

* Deliver personalized messages to customers on the right communication channels through either a real-time integration or batch integration.

**Resources**

* Braze documentation: https://www.braze.com/docs/partners/data_augmentation/recommendation/amazon_personalize/
* AWS ML Blog Post: https://aws.amazon.com/blogs/machine-learning/optimizing-your-engagement-marketing-with-personalized-recommendations-using-amazon-personalize-and-braze/
* AWS Media Blog Post: https://aws.amazon.com/blogs/media/speed-relevance-insight-how-streaming-services-can-master-effective-content-discovery-and-engagement/
* Workshop: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/4-Messaging/4.2-Braze.ipynb

### Direct/Managed Integrations

**Magento 2**: A Magento 2 extension was developed by a Magento and AWS partner called Customer Paradigm. The extension was NOT developed by Adobe Magento.

The extension can be easily installed into any Magento 2 storefront whether it's running on-premises, another cloud provider, or on AWS. Amazon Personalize is always accessed in the customer's AWS account.

**Resources**

* Partner website: https://www.customerparadigm.com/amazon-personalize-magento/
* Magento Marketplace: https://marketplace.magento.com/customerparadigm-amazon-personalize-extension.html

**Shopify:** [Obviyo](https://www.obviyo.com/) (formerly known as HiConversion) has built a managed integration with Personalize for Shopify storefronts. This means Obviyo is managing Personalize in their AWS environment and Shopify merchants pay Obviyo for personalization capabilities that are powered by Personalize.

**Resources**

* Partner website: https://www.obviyo.com/
