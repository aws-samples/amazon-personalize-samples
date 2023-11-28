# Generative AI with Amazon Personalize

There are many ways to use foundation models, the basis of generative AI, with Amazon Personalize. Samples will be added to this folder as they are developed.

* Marketing use cases
  - [Personalized marketing campaigns](personalized_marketing_campaign/)
  - [User personalized marketing messaging with Amazon Personalize and Generative AI](user_personalized_marketing_messaging_with_amazon_personalize_and_gen_ai/). Use this sample to create personalized marketing content (for instance emails) for each user using [Amazon Personalize](https://aws.amazon.com/personalize/) and [Amazon Bedrock](https://aws.amazon.com/bedrock/). In this sample you will train an [Amazon Personalize](https://aws.amazon.com/personalize/) 'Top picks for you' Recommender to get personalized recommendations for each user. You will then generate a prompt that includes the user's preferences, recommendations, and demographics. Finally you will use [Amazon Bedrock](https://aws.amazon.com/bedrock/) to generate a personalized email for each user.
