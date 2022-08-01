# Amazon Personalize Cheat Sheet

## Is Amazon Personalize a Good Fit?

Amazon Personalize is a great platform for operating a recommendation system at scale on AWS but it is not appropriate for any and all personalization or recommendation scenarios. The chart below is a rough guide for good and bad fits.

|Good Fit	|Bad Fit	|
|---	|---	|
|Recommending items to known users. Movies to users based on their watching history.	|Recommendations based only on explicit metadata flags. When a new user answers preferences to guide their recommendations.	|
|Recommending new items to known users. A retail site adding new items for sale to their existing users.	|Low data volumes for users, items, and interactions (see chart below).	|
|Recommending items to new users. A user just signed up and quickly gets recommendations	|Mostly non identified users. An application where the users do not have a historical record of activity.	|
|Recommending new items to new users. A retail site recommending new items to a new user.	|**Next Best Action Workloads -** Personalize recommends likely items, it does not understand proper workflows and sequences.	|

### Minimum Suggested Data Volume

1. More than 50 users.
2. More than 50 items.
3. More than 1500 interactions.

If your datasets do not map to this, it is too early for Amazon Personalize.


## Use Cases By Recipe

What kind of use cases can be solved and how?

1. **Personalized Recommendations** `User-Personalization`/`Recommended For You`/`Top Picks for You`:
    1. This is a primary use case of Amazon Personalize, using user-item-interaction data to build a recommendation model that directly targets each user, and allows for new users to be added on the fly with PutEvents without re-training. PutEvents also allows for the users to see recommendations that are based on their most recent behavior so you do not lose out on that additional info. Also you can feed in context specific components like device type or location to improve results.
    2. You can also add item and user metadata in order to better enrich the model, or to filter recommendations by attribute.
    3. For Video On Demand and Retail use-cases, the domain recommenders “Top picks for you” and “Recommended for you” allow you to get up and going quickly and with less operational overhead.
2. **Recommending Items to New Users** `User-Personalization`/`Recommended For You`/`Top Picks for You`:
    1. New users (aka cold users) can be added to your existing User-Personalization solutions by leveraging the PutEvents feature. Each new user starts with a representation in the service that returns the popular items. This representation is shifted by the user’s behavior. As they interact with content within the application and the events are sent by the application to Personalize, recommendations are updated without having to re-train the model. This delivers up to date personalization without constant retraining.
    2. Metadata for new users can be added to the Users dataset using the PutUsers API or dataset import jobs. This data is incorporated into the model at the next retraining.
3. **Recommending New Items** `User-Personalization`/`Recommended For You`/`Top Picks for You`:
    1. This is incredibly useful when you have new items (aka cold items) that need to be showcased to users with some form of personalization. This allows for the items to be recommended without historical precedent based on metadata factors.
    2. This can also be used with incremental training and updating of your dataset to more easily cold-start new items.
    3. Lastly this approach leverages a bandit like exploration capacity to help you quickly determine which results make sense, and which do not for recommendations, a far better approach than just blindly pushing new content.
4. **Re-Ordering by Relevance** `Personalized-Ranking`:
    1. Uses the same HRNN algorithm underneath User-Personalization but takes in a user AND a collection of items. This will then look at the collection of items and rank them in order of most relevant to least for the user. This is great for promoting a pre-selected collection of items and knowing what is the right thing to promote for a particular user.
5. **Related Items** `Similar-Items`/`SIMS`:
    1. `Similar-Items`: Deep learning model that considers both interaction data and item metadata to balance related item recommendations based on interaction history and item metadata similarity. Useful when you have less interaction data but have quality item metadata or when you frequently introduce cold/new items.
    2. `SIMS`: Pretty simple idea, implemented via item-item collaborative filtering but basically looks at how people are co-interacting with particular items and then determine how similar items are at a global level based on interaction data. Does not consider item or user metadata and is not personalized to each user. Useful when you have a lot of relevant interaction data, do not have a lot of cold items (changing catalog), and/or lack item metadata.
    3. For Video On Demand and Retail use-cases, the domain recommenders “Because you watched X”, “More like X”, “Frequently bought together”, and “Customers who viewed X also viewed” allow you to get up and going quickly and with less operational overhead.
6. **Frequently Bought Together** `Similar-Items`/`SIMS`:
    1. The key is preparing the right data used to train a model in Personalize and choosing the right recipe. For example, train a SIMS model on purchase data only and, if possible, train only on purchase data where customers have purchased multiple items and/or purchased items across multiple categories. This will bring the desired behavior to the model and create diversity in recommendations (which is what you want for this use case).
    2. SIMS can also be combined with Personalized-Ranking to rerank recommendations from SIMS before presenting them to the user. This provides a personalized order of items that are frequently bought together.
    3. The domain recommender “Frequently bought together” will allow you to get up and going quickly and with less operational overhead.
7. **Most Popular Overall** `Popularity-Count`:
    1. Not machine learning, just a baseline from counting the most commonly interacted with items. This recipe is useful for popular item recommendations or for creating a baseline of offline metrics that can be used to compare against solution versions created using other user-personalization recipes with the same datasets.
    2. For Video On Demand and Retail use-cases, the domain recommenders “Most popular”, “Most viewed”, and “Best sellers” allow you to get up and going quickly and with less operational overhead.
8. **User Segmentation** `Item-Affinity`/`Item-Attribute-Affinity`:
    1. Create segments of users based on their affinity to specific items in your catalog or their affinity to item attributes. Excellent match with marketing campaigns where you’re looking to target users who will have an interest in specific items you’re looking to promote or items similar to existing items.

## Killer Features:

1. [Domain dataset groups](https://docs.aws.amazon.com/personalize/latest/dg/domain-dataset-groups.html): recommenders for Video On Demand and Retail use cases
    1. A *Domain dataset group* is an Amazon Personalize container for domain specific pre-configured resources, including datasets, recommenders, and filters. Use a Domain dataset group if you have a streaming video or e-commerce application and want to let Amazon Personalize find the best configurations for your recommenders.
2. Contextual Recommendations
    1. Allows you to fine-tune recommendations based on state that varies with the interaction rather than specific to the user or item. Think the user’s current location, device/channel being used, time of day, day of week, etc.
    2. See this blog post for a detailed example: https://aws.amazon.com/blogs/machine-learning/increasing-the-relevance-of-your-amazon-personalize-recommendations-by-leveraging-contextual-information/
3. Interaction and Metadata Filtering
    1. Filter recommendations based on the user’s interaction history or the metadata attributes for the items or current user. Very handy in nearly all Media or Retail workloads. For example, exclude recently purchased or out of stock items or include/exclude recommended items based on category or genre.
    2. See this blog post for details: https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/
4. Batch Inference
    1. Great for exporting large quantities of recommendations to files for caches, for email campaigns, or just general exploration.
5. AutoScaling Campaigns/Recommenders
    1. For real time inference endpoints (campaigns and recommenders), the service will automatically scale to meet your traffic demands if a particular campaign or recommender is over-subscribed. It will then also reduce to your requested minimum capacity when the traffic volume abates.
6. Unstructured Text as Item Metadata
    1. Add your product descriptions, video plot synopsis, or article content as an item metadata field and let Personalize use natural language processing (NLP) to extract hidden features from your text to improve the relevance of recommendations.
7. Put Events
    1. Allows for applications to update Personalize in real time with changes in intent from user behavior. This means that each subsequent request can adapt to that intent WITHOUT retraining.
8. Put Items/Put Users
    1. Allows for applications to add/update individual or mini-batches of items or users without having to upload the entire items and users datasets.
    2. See FAQs below for more detail.
9. KMS Integration
    1. All data can be encrypted using a customer managed key, all data is encrypted regardless.
10. No Information Sharing
    1. All customer data is fully isolated and is not leveraged in order to improve the recommendations of Amazon or any other party.
    2. Models are private to the customer’s AWS account.

## Video Series:

1. Introduction To Amazon Personalize: https://youtu.be/3gJmhoLaLIo
2. Understanding Your Data with Amazon Personalize: https://www.youtube.com/watch?v=TEioktJD1GE
3. Solving Real World Use Cases with Amazon Personalize: https://www.youtube.com/watch?v=9N7s_dVVWBE
4. Getting Your Amazon Personalize Recommendations in Front of Your Users: https://www.youtube.com/watch?v=oeVYCOFNFMI
5. Get Your Amazon Personalize POC to Production: https://www.youtube.com/watch?v=3YawVCO6H14
6. Enhancing Customers Experiences with Amazon Personalize (including a demo of the [Retail Demo Store](https://github.com/aws-samples/retail-demo-store)): https://youtu.be/71dWFhzw7iw

## FAQs:

1. How often should I retrain?
    1. Retraining frequency is determined by the business requirements. How often do you need to learn globally about your users and their behavior with items? How often do you need to include new items? The answers determine how frequently you should train. Generally speaking, most customers retrain weekly. See below for more detailed guidance.
    2. If using the “aws-user-personalization” recipe, the service will automatically update the solution version in the background every 2 hours (at no additional cost). This auto update process will bring in new items added since the last update so they can start being recommended to users (i.e. cold starting items). This works in coordination with the explorationWeight parameter set on the campaign to control the weight placed on recommending new/cold items vs relevant items (explore/exploit).
    3. If the 2 hour auto-update is not frequent enough for introducing new items, you can manually create a new solution version with trainingMode=UPDATE and update the campaign more frequently (i.e. hourly). This essentially does the same thing as the auto-update, just on a customer-defined frequency. However, there is a cost for training hours for doing this manually.
    4. Regardless of the auto or manual update mode process taken, this does not fully retrain the model. The customer would still need to occasionally create a new solution version with trainingMode=FULL to fully retrain the model. This is important to do occasionally to recalculate the weights across the model based on all data but the auto-update process makes full retraining necessary less frequently. This is where the weekly guidance comes in. So let auto update run all week and do full retraining once a week.
    5. To be more precise in retraining frequency, another approach is to monitor online metrics. When they start to trail off (i.e. model drift), it’s time to retrain.
2. How do I add a new user?
    1. If you are using the PutEvents API, the new user exists as soon as you log their first action. If you are not leveraging this, then the user will exist in the system as soon as you have retrained a model that contains their behavior in your interactions dataset.
    2. If your user is not known (a new anonymous user before signup) you can still work to cold-start them. If you can assign a new UUID for their user and sessionID immediately, then you can continue the process as defined above to cold start a user.
    3. If that path does not work, you can still generate a new UUID for the sessionID, call PutEvents without a userID, and then continue to specify the same sessionID after a valid userID has been generated for them. When you retrain, Personalize will combine the historical data, with PutEvents data, and when it sees matching sessionIDs it will combine all prior anonymous interactions together with non-anonymous interactions for the user. This would allow you to specify the history before they had a valid internal userID.
    4. You can add/update users individually or in mini-batches with the PutUsers API. However, only users with interactions will receive personalized recommendations either after (re)training or when cold started with the PutEvents API.
3. How do I add a new item?
    1. There are two ways to add items to the items dataset: 1/ Add new items to the items dataset by uploading the full dataset using a dataset import job, or 2/ add items individually or in mini-batches using the PutItems API.
    2. New items will be incorporated into recommendations after retraining if interactions also exist (all recipes) or cold-starting new item recommendations with or without interactions after the solution has been updated (trainingMode = FULL/UPDATE for aws-user-personalization and HRNN-Coldstart only).
    3. For example, you can organically stream new items into your historical dataset by placing banners for new releases. Anything that causes a user to interact with the new items and for that action to be logged can improve recommendations after the next training.
4. How do I filter results for certain conditions?
    1. Using the filters feature for either Interaction (https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) or Metadata information ( https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/ ).
    2. Filtering based on interaction history currently only considers the most recent 100 real-time interactions (PutEvents API) and the most recent 200 historical interactions in the dataset at the time of retraining. All event types are included in the 100/200 limits.
5. I need to filter items based on a rolling date value but filters do not support dynamic values for range operators. What are my options?
    1. Range operators currently cannot be used with dynamic values so you must create a filter expression with a fixed value and then rotate the filter periodically to update the fixed value. The [filter rotator](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/filter_rotator) solution can be used to automate the rotation process.
6. Why should I use Amazon Personalize over a custom solution?
    1. Assuming your data and use cases are aligned, this is a great way to get a best in class model in front of the end users faster. While handling the operational burden of running a recommendation system at scale, Personalize also frees you up to improve feature engineering, data collection, user experiences, or solve other problems.
7. I have a use case where my customers purchase or interact with items in my catalog infrequently (e.g. purchasing a car). Is Personalize still a good fit?
    1. Yes, Personalize can still be put to use effectively for this type of use case. For example, a SIMS model can be trained based on all user activity such as browsing or purchase history (online and/or offline) and then used for similar item recommendations on item detail pages. This allows you to leverage recent activity across all active users to make relevant recommendations to returning users.
    2. Real-time recommendations are also effective here since Personalize is able to learn from a user’s current interest and adapt recommendations quickly. For example, recommend popular items initially and then quickly personalize recommendations after a few interactions are streamed using the PutEvents API.
8. Should I use AutoML?
    1. No, the recipes solve different use cases. Take the time to select the most appropriate recipe for the use-case and skip this feature.
9. Should I use HPO / How often?
    1. Infrequently. Take the results of one HPO job and use them explicitly in the solution config for several retrainings. Then run HPO again and repeat. Realistically tuned parameters should not shift much between training jobs. This approach will keep your training times, and therefore costs, lower than running HPO for all training jobs without sacrificing model accuracy.
10. How can I predict the pricing of training?
    1. Unfortunately there really is not a great way to know this beforehand, we do have some testing that has been done on the MovieLens dataset. For example using `User-Personalization` it takes around  6 human hours for the training on 25M interactions but less than 1 human hour to train on 100k interactions. Because training is sharded over multiple hosts, the actual hours are, 53.9 hours for 50M and 2.135 hours for 100k. Billing is done on the actual hours, not the human ones.
11. What is a TPS hour and how does it relate to pricing / usability?
    1. Amazon Personalize spins up dedicated compute resources that will remain provisioned in order to meet your expected minimum throughput requirements (Transactions per Second or TPS), they are billed in terms of hours that these resources are allocated, thus a TPS-Hour. 1 TPS-Hour is the amount of compute capacity required to deliver 1 recommendation per second for an entire hour.
    2. Usage is measured in 5 minute increments where the maximum of the average number of requests and the minimum provisioned throughput in each increment is used as the TPS-Hour value. Therefore, when the service scales above the minimum provisioned TPS, the customer is only billed for capacity actually consumed. The TPS-Hours for all 5 minute increments are summed during the billing period to determine the total TPS-Hours for billing calculations.
    3. The service will automatically scale up for you if your traffic exceeds the minimum provisioned TPS on the campaign, and it has proven to be a valuable tool for many of our customers. A capacity buffer is allocated above the minimum provisioned TPS to allow the service to absorb increases in request load while it scales out.
    4. If your customer knows they are going to have a spike of activity such as a flash sale or promotional event, have them use some automated process to update the provisioned capacity to meet the new need, then throttle it down later if they cannot wait 5-10 minutes for the service to auto-scale for them.
    5. The Amazon Personalize Monitor project provides a CloudWatch dashboard, custom metrics, utilization alarms, and cost optimization functions for Personalize campaigns: https://github.com/aws-samples/amazon-personalize-monitor
12. How can I tell if a Personalize model is providing high quality recommendations?
    1. Personalize provides offline metrics for each solution version that measure the accuracy of predictions from the model against held out data from the interactions dataset. Use these metrics to provide a directional sense of the quality of a solution version against other versions.
    2. Online testing (i.e. A/B testing) is always going to be the best measure of the impact of a model on business metrics.
    3. When you are comparing Personalize models against an existing recommendation system, all the historical data is initially biased towards the existing approach. Often the offline metrics do not reflect what a user MAY have done if they were exposed to something else (how could they, the data does not reflect it). So worth noting this effect, and the bandit based exploration Personalize can do to organically learn better from your users. Therefore running an online test for a few weeks **before** actually starting a test to measure results is recommended.
    4. See this blog post for details: https://aws.amazon.com/blogs/machine-learning/using-a-b-testing-to-measure-the-efficacy-of-recommendations-generated-by-amazon-personalize/
13. How can I optimize for cost?
    1. DO NOT USE AUTOML!
    2. DO NOT START WITH HPO - build something working first, optimize last.
    3. Re-Train based on business requirements only. See FAQ question for details.
    4. Rely heavily on auto-scaling by setting the minimum provisioned TPS low unless it negatively impacts your throughput / latency targets.
    5. Consider using batch recommendations when the use-case aligns with a downstream batch process such as email marketing. Since batch recommendations run against a solution version, they do not require a campaign.
    6. The Amazon Personalize Monitor project provides some cost optimization features for optimizing campaign provisioning as well as alerting and deleting idle/abandoned campaigns: https://github.com/aws-samples/amazon-personalize-monitor
14. What are the best ways to use caching with Amazon Personalize? How should I integrate Personalize with my existing applications?
    1. Check out the [Personalization APIs](https://github.com/aws-samples/personalization-apis) solution: Real-time low latency API framework that sits between your applications and recommender systems such as Amazon Personalize. Provides best practice implementations of response caching, API gateway configurations, A/B testing with [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html), inference-time item metadata, automatic contextual recommendations, and more.
15. What is the best way to compare Personalize to an existing user experience or another recommendation system?
    1. A/B testing is the most common technique for evaluating the effectiveness of Personalize against online metrics. [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html) is an A/B testing tool from AWS that can be used with Personalize. The [Personalization APIs](https://github.com/aws-samples/personalization-apis) project provides a deployable solution and reference architecture.
16. How do incremental records influence recommendations for the current user?
    1. Amazon Personalize allows you to import [interactions](https://docs.aws.amazon.com/personalize/latest/dg/importing-interactions.html), [users](https://docs.aws.amazon.com/personalize/latest/dg/importing-users.html), and [items](https://docs.aws.amazon.com/personalize/latest/dg/importing-items.html) incrementally. These can affect recommendations for the current user in different ways depending on whether the a new solution version has been trained and what type of trainingMode was used:

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
