# Amazon Personalize + Generative AI: Personalized Marketing Campaign

The notebooks and data in this folder are designed to give you hands-on experience building models in Amazon Personalize to identify users with an affinity for specific items and then use Amazon Bedrock to generate personalized marketing content tailored to those users.

## Scenario

Assume you are a marketing manager. Your task is to more effectively promote the flights for an airline through email campaigns using AI. To improve end user engagement (increase click-through-rate) and reduce churn (decrease email unsubscriptions), you will use AI to identify customers with an affinity for specific flights and then use generative AI to to generate marketing content to those users. There has two AI engines

1. Recommendation engine - Amazon Personalize service

2. Content Generative engine - Amazon Bedrock service

## Pipeline

Marketing request-->Amazon Personalize-->retrieve metadata-->combine with PromptTemplate--> LangChain-->Amazon Bedrock & LLM--> Generate content -->save in JSON

## Workshop steps

- Step1: Run the [airline_ticket_user_segmentation](airline_ticket_user_segmentation_09212023_github.ipynb) notebook

- Step2: Run the [personalized_marketing_campaign](personalized_marketing_campaign_10032023_1600_github.ipynb) notebook

If you're running the notebooks in Amazon SageMaker Studio, the IAM assume role requirements are,
1. AmazonPersonalizeFullAccess
2. AmazonS3FullAccess
3. bedrock_full_access_policy
4. IAMFullAccess
5. AmazonSageMakerFullAccess

The datasets used in this sample were generated, not from a customer.
