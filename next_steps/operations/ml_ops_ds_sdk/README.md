## Automating your Personalize workflow using AWS Step Functions Data Science SDK

As machine learning (ML) becomes a larger part of companies’ core business, there is a greater emphasis on reducing the time from model creation to deployment. In November of 2019, AWS released the AWS Step Functions Data Science SDK for Amazon SageMaker, an open-source SDK that allows developers to create Step Functions-based machine learning workflows in Python. You can now use the SDK to create reusable model deployment workflows with the same tools you use to develop models. You can find the complete notebook for this solution in the “automate_personalize_workflow” folder of our GitHub repo. 

This repo demonstrates the capabilities of the Data Science SDK with a common use case: how to automate Personalize. In this post, you create a serverless workflow to train a movie recommendation engine. Finally, the shows how to trigger a workflow based off a periodic schedule.

### This post uses the following AWS services:
•	AWS Step Functions allows you to coordinate several AWS services into a serverless workflow. You can design and run workflows in which the output of one step acts as the input to the next step, and embed error handling into the workflow.\
•	AWS Lambda is a compute service that lets you run code without provisioning or managing servers. Lambda executes your code only when triggered and scales automatically, from a few requests per day to thousands per second.\
•	Amazon Personalize is a machine learning service which enables you to personalize your website, app, ads, emails, and more, with custom machine learning models which can be created in Amazon Personalize, with no prior machine learning experience.

## Overview of the SDK
The SDK provides a new way to use AWS Step Functions. A Step Function is a state machine that consists of a series of discrete steps. Each step can perform work, make choices, initiate parallel execution, or manage timeouts. You can develop individual steps and use Step Functions to handle the triggering, coordination, and state of the overall workflow. Before the Data Science SDK, you had to define Step Functions using the JSON-based Amazon States Language. With the SDK, you can now easily create, execute, and visualize Step Functions using Python code. 

This repo provides an overview of the SDK, including how to create Step Function steps, work with parameters, integrate service-specific capabilities, and link these steps together to create and visualize a workflow. You can find several code examples throughout the post; however, we created a detailed Amazon SageMaker notebook of the entire process. 

## Overview of Amazon Personalize
Amazon Personalize is a machine learning service that makes it easy for developers to create individualized recommendations for customers using their applications. 

Machine learning is being increasingly used to improve customer engagement by powering personalized product and content recommendations, tailored search results, and targeted marketing promotions. However, developing the machine-learning capabilities necessary to produce these sophisticated recommendation systems has been beyond the reach of most organizations today due to the complexity. Amazon Personalize allows developers with no prior machine learning experience to easily build sophisticated personalization capabilities into their applications, using machine learning technology perfected from years of use on Amazon.com. 

With Amazon Personalize, you provide an activity stream from your application – clicks, page views, signups, purchases, and so forth – as well as an inventory of the items you want to recommend, such as articles, products, videos, or music. You can also choose to provide Amazon Personalize with additional demographic information from your users such as age, or geographic location. Amazon Personalize will process and examine the data, identify what is meaningful, select the right algorithms, and train and optimize a personalization model that is customized for your data. All data analyzed by Amazon Personalize is kept private and secure, and only used for your customized recommendations. You can start serving personalized recommendations via a simple API call. You pay only for what you use, and there are no minimum fees and no upfront commitments. 

Amazon Personalize is like having your own Amazon.com machine learning personalization team at your disposal, 24 hours a day.



## Instructions
Upload the notebook and follow the instructions

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

