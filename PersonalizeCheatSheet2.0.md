# Amazon Personalize Cheat Sheet 2.0

## Is Amazon Personalize a Good Fit?

Amazon Personalize is a great platform for operating a recommendation system at scale on AWS but it is not appropriate for any and all personalization or recommendation scenarios. The chart below is a rough guide for good and bad fits.


|Good Fit	|Bad Fit	|
|---	|---	|
|Recommending items to known users. Movies to users based on their watching history.	|Recommendations based on explicit metadata flags. When a new user answers preferences to guide their recommendations.	|
|Recommending new items to known users. A retail site adding new items for sale to their existing users.	|Low data volumes for users, items, and intereactions( see chart below).	|
|Recommending items to new users. A user just signed up and quickly gets recommendations	|Mostly non identified users. An application where the users do not have a historical record of activity.	|
|Recommending new items to new users. A retail site recommending new items to a new user.	|	|
|	|	|

### Minimum Suggested Data Volume

1. More than 50 users.
2. More than 50 items.
3. More than 1500 interactions.


If your dataset does not map to this, it is too early for Amazon Personalize.

## Use Cases By Recipe

What kind of use cases can be solved and how?


1. **Personalized Recommendations** `User-Personalization`:
    1. This is a primary use case of Amazon Personalize, using user-item-interaction data to build a recommendation model that directly targets each user, and allows for new users to be added on the fly with PutEvents without re-training. PutEvents also allows for the users to see recommendations that are based on their most recent behavior so you do not lose out on that additional info. Also you can feed in context specific components like device type or location to improve results.
    2. You can also add item and user metadata in order to better enrich the model, or to filter recommendations by attribute.
2. **Recommending Items to New Users** `User-Personalization`:
    1. New users (aka cold users) can be added to your existing User-Personalization solutions by leveraging the PutEvents feature. Each new user starts with a representation in the service that returns the popular items. This representation is shifted by the user’s behavior. As they interact with content within the application and the events are sent by the application to Personalize, recommendations are updated without having to re-train the model. This delivers up to date personalization without constant retraining.
3. **Recommending New Items **`User-Personalization`:
    1. This is incredibly useful when your customer has new items (aka cold items) that need to be showcased to their users with some form of personalization. This allows for the items to be recommended without historical precedent based on metadata factors.
    2. This can also be used with incremental training and updating of your dataset to more easily cold-start new items. 
    3. Lastly this approach leverages a bandit like exploration capacity to help you quickly determine which results make sense, and which do not for recommendations, a far better approach than just blindly pushing new content.
4. **Re-Ordering by Relevance** `Personalized-Ranking`:
    1. Uses the same HRNN algorithm underneath User-Personalization but takes in a user AND a collection of items. This will then look at the collection of items and rank them in order of most relevant to least for the user. This is great for promoting a pre-selected collection of items and knowing what is the right thing to promote for a particular user. 
5. **Similar Items** `SIMS`:
    1. Pretty simple idea, implemented via item-item collaborative filtering but basically look at how people are interacting with particular things and then determine how similar things are at a global level based on that data. Not user specific at all.
6. **Most Popular Overall** `Popularity-Count`:
    1. Not machine learning, just a baseline from counting the most commonly interacted with items. This recipe is useful for popular item recommendations or for creating a baseline of offline metrics that can be used to compare against solution versions created using other user-personalization recipes with the same datasets.

## Killer Features:

1. Context Recommendations
    1. Allows for you to scope recommendations to state that is varies with the interaction rather than specific to the user or item. Think their current location or device/channel being used.
2. Interaction and Metadata Filtering
    1. Filter recommendations based on the user’s interaction history or the metadata attributes for the items or current user. Very handy in nearly all Media or Retail workloads. For example, exclude recently purchased items or include/exclude recommended items based on category or genre.
3. Batch Inference
    1. Great for exporting large quantities of recommendations to files for caches, for email campaigns, or just general exploration.
4. AutoScaling Campaigns
    1. The service will automatically scale to meet your traffic demands if a particular campaign is over-subscribed. It will then also reduce to your requested minimum capacity when the traffic volume abates. 
5. Put Events
    1. Allows for applications to update Personalize in real time with changes in intent from user behavior. This means that each subsequent request can adapt to that intent WITHOUT retraining.
6. KMS Integration
    1. All data can be encrypted using a customer managed key, all data is encrypted regardless.
7. No Information Sharing
    1. All customer data is fully isolated and is not leveraged in order to improve the recommendations of Amazon or any other party.
    2. Models are private to the customer’s AWS account.

## FAQs:

1. How often should I retrain?
    1. Retraining frequency is determined by the business requirements. How often do you need to learn globally about your users and their behavior with items? How often do you need to include new items? The answers determine how frequently you should train. If you are adding items daily and want them recommended that would be daily. Otherwise, weekly is generally a good fit for many workloads.
2. How do I add a new user?
    1. If you are using the PutEvents API, the new user exists as soon as you log their first action. If you are not leveraging this, then the user will exist in the system as soon as you have retrained a model that contains their behavior in your interactions dataset.
3. How do I add a new item?
    1. This is a batch process. Items are added to all models if they exist in the interactions dataset when you retrain. Items can be added to coldstarts by adding the item_metadata entries, described here.
    2. For example, you can organically stream new items into your historical dataset by placing banners for new releases. Anything that causes a user to interact with the new items and for that action to be logged can improve recommendations after the next training.
4. How do I filter results for certain conditions?
    1. Using the filters feature for either Interaction ( https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/ )  or Metadata information ( https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/ ).
5. Why should I use Amazon Personalize over a custom solution?
    1. Assuming your data and use cases are aligned, this is a great way to get a best in class model in front of the end users faster. While also handling the operational burden of running a recommendation system at scale. This frees you up to improve feature engineering, data collection, or solve other problems.
6. Should I use AutoML?
    1. No, the algorithms solve different use cases. Take the time to select the most appropriate recipe for the use-case and skip this feature.
7. Should I use HPO / How often?
    1. Infrequently, take the results of one HPO job and use them manually for a while. Realistically they should not shift much between training jobs.
8. How can I predict the pricing of training?
    1. Unfortunately there really is not a great way to know this beforehand, we do have some testing that has been done on the MovieLens dataset. For example using `User-Personalization` it takes around  6 human hours for the training on 25M interactions but around 50 human minutes to train on 100k interactions. Because this is sharded over multiple hosts, the actual hours are, 53.9 hours for 50M and 2.135 hours for 100k. Billing is done on the actual hours, not the human ones.
9. What is a TPS hour and how does it relate to pricing / usability?
    1. Amazon Personalize spins up dedicated compute resources that will remain provisioned in order to meet your expected minimum throughput requirements (Transactions per Second or TPS), they are billed in terms of hours that these resources are allocated, thus a TPS-Hour. 1 TPS-Hour is the amount of compute capacity required to deliver 1 recommendation per second for an entire hour. 
    2. Usage is measured in 5 minute increments where the maximum of the average number of requests in each increment and the minimum provisioned throughput is used as the TPS-Hour value. Therefore, when the service scales above the minimum provisioned TPS, the customer is only billed for capacity actually consumed. The TPS-Hours for all 5 minute increments are summed during the billing period to determine the total TPS-Hours for billing calculations.
    3. The service will automatically scale up for you if your traffic exceeds the minimum provisioned TPS on the campaign, and it has proven to be a valuable tool for many of our customers. A capacity buffer is allocated above the minimum provisioned TPS to allow the service to absorb increases in request load while it scales out. 
    4. If your customer knows they are going to have a spike of activity such as a flash sale or promotional event, have them use some automated process to update the provisioned capacity to meet the new need, then throttle it down later if they cannot wait 5-10 minutes for the service to auto-scale for them.
10. How can I optimize for cost?
    1. DO NOT USE AUTOML!
    2. DO NOT START WITH HPO - build something working first, optimize last.
    3. Re-Train based on business requirements only.
    4. Rely heavily on auto-scaling by setting the minimum provisioned TPS low unless it negatively impacts your throughput / latency targets.
    5. Consider using batch recommendations when the use-case aligns with a downstream batch process such as email marketing. Since batch recommendations run against a solution version, they do not require a campaign.

## Technical Enablement Links:

1. Overall Samples: https://github.com/aws-samples/amazon-personalize-samples
2. Getting Started: https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started
3. POC in a Box 2.0: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/workshops/POC_in_a_box
4. Use Case Based Notebooks: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/core_use_cases
5. Data Science Tools: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/data_science
6. MLOps for Personalize: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops


## Demos:

Media: Unicorn Flix - [https://unicornflix.amplify-video.com](https://unicornflix.amplify-video.com/) 

Retail: The Retail Demo Store - GitHub: https://github.com/aws-samples/retail-demo-store; Running instance: [http://retaildemostore.jory.cloud/](http://retaildemostore.jory.cloud/#/)

## Technology Partners:

There are several technology partners that provide complementary functionality to Personalize that can accelerate customers getting to production with Personalize or enhancing the ROI on implementing personalization with Personalize.

### Data Collection

**Segment** is a [Customer Data Platform](https://en.wikipedia.org/wiki/Customer_data_platform). They are an AWS Advanced Technology Partner and hold the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) and [Retail](https://aws.amazon.com/retail/partner-solutions/) competencies.

Segment helps customers with Personalize in the following ways:

* Event collection - this is a core capability of Segment. Customers use Segment to collect clickstream events across their web app, mobile apps, and other integrations. These events are collected, validated, and fanned out to downstream destinations configured by the customer. One of these destinations is Amazon Personalize.
* Customer/user profile identity resolution - because Segment sees events across all channels for a customer's users, they are able to create a unified customer profile. This profile/identity is key to being able to deliver omnichannel personalization.
* Activation across an organization's other marketing tools - because Segment allows customers to create connections to other marketing tools, attaching personalized recommendations from Personalize to profiles in Segment allows customers and downstream partners to leverage those recommendations in their tools.

**Resources**
Segment CTO video: https://www.youtube.com/watch?v=LQSGz8ryvXU
Blog post: https://segment.com/blog/introducing-amazon-personalize/
AWS/Segment Workshop: https://github.com/james-jory/segment-personalize-workshop
Documentation: https://segment.com/docs/connections/destinations/catalog/amazon-personalize/

### Analytics and Measurement

**Amplitude** is an AWS Advanced Technology Partner and holds the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) competency.
Amplitude helps customers with Personalize in the following ways:

* Product insights - Amplitude provides visibility into the event types that lead to conversion through sophisticated funnel analysis. This provides the insight that customers need to optimize their event taxonomy and select the right events and metadata fields to train models on in Personalize.
* A/B test evaluation - Amplitude provides online measurement of A/B tests that can be represented by personalized customer experiences powered by Personalize.

**Resources**
Workshop: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.5-Amplitude-Performance-Metrics.ipynb
Blog post: https://aws.amazon.com/blogs/apn/measuring-the-effectiveness-of-personalization-with-amplitude-and-amazon-personalize/

**Optimizely** is a market leading A/B testing platform. They are an AWS Advanced Technology Partner and hold the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) competency.

Optimizely helps customers with Personalize in the following ways:

* A/B test results - a core offering of Optimizely is measurement and reporting of experiments such as personalization techniques.
* Feature flagging - enable/disable personalized experiences

**Resources**
Workshop: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.6-Optimizely-AB-Experiment.ipynb

### Messaging

**Braze** is a market leading messaging platform (email, push, SMS). They are an AWS Advanced Technology Partner and hold the [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) and [Retail](https://aws.amazon.com/retail/partner-solutions/) competencies.

Braze helps customers with Personalize in the following ways:

* Deliver personalized messages to customers on the right communication channels through either a real-time integration or batch integration.

**Resources**
Braze documentation: https://www.braze.com/docs/partners/data_augmentation/recommendation/amazon_personalize/
AWS ML Blog Post: https://aws.amazon.com/blogs/machine-learning/optimizing-your-engagement-marketing-with-personalized-recommendations-using-amazon-personalize-and-braze/
Workshop: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/4-Messaging/4.2-Braze.ipynb

### Direct Integrations

**Magento 2**: A Magento 2 extension was developed by a Magento and AWS partner called Customer Paradigm. The extension was NOT developed by Adobe Magento.

The extension can be easily installed into any Magento 2 storefront whether it's running on-premises, another cloud provider, or on AWS. Amazon Personalize is always accessed in the customer's AWS account.

**Resources**
https://www.customerparadigm.com/amazon-personalize-magento/

**Shopify: **HiConversion has built a managed integration with Personalize for Shopify storefronts. This means HiConversion is managing Personalize in their AWS environment and Shopify merchants pay HiConversion for personalization capabilities that are powered by Personalize.

**Resources**
https://www.hiconversion.com/amazon-personalize/
