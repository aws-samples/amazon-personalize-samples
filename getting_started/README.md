# Getting Started

This tutorial will walk you through how to get started using Amazon Personalize:

1. Building a work environment (see steps bellow)
2. Build your first use-case optimized recommenders for Video On Demand and E-commerce
3. Build your first custom dataset, model, and recommendation campaign

## Environment Prerequisites

Only applies if you are deploying with the CloudFormation template, otherwise consult the IAM permissions needed for your specific task.

1. AWS Account
2. User with administrator access to the AWS Account

## Building Your Environment

The first step is to deploy a CloudFormation template that will perform much of the initial setup for you. In another browser window login to your AWS account. Once you have done that open the link below in a new tab to start the process of deploying the items you need via CloudFormation.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=PersonalizeDemo&templateURL=https://amazon-personalize-github-samples.s3.amazonaws.com/PersonalizeDemo.yaml)

Follow along with the screenshots if you have any questions about these steps.

<details>
  <summary>Click to expand the instructions</summary>
  
### Cloud Formation Wizard

Start by clicking `Next` at the bottom like shown:

![StackWizard](static/imgs/img1.png)

In the next page you need to provide a unique S3 bucket name for your file storage, it is recommended to simply add your first name and last name to the end of the default option as shown below, after that update click `Next` again.

![StackWizard2](static/imgs/img3.png)

This page is a bit longer so scroll to the bottom to click `Next`.

![StackWizard3](static/imgs/img4.png)

Again scroll to the bottom, check the box to enable the template to create new IAM resources and then click `Create Stack`.

![StackWizard4](static/imgs/img5.png)

For a few minutes CloudFormation will be creating the resources described above on your behalf it will look like this while it is provisioning:

![StackWizard5](static/imgs/img6.png)

Once it has completed you'll see green text like below indicating that the work has been completed:

![StackWizard5](static/imgs/img7.png)

Now that you have your environment created, you need to save the name of your S3 bucket for future use, you can find it by clicking on the `Outputs` tab and then looking for the resource `S3Bucket`, once you find it copy and paste it to a text file for the time being.


</details>


## Using the Notebooks

Start by navigating to the Amazon SageMaker landing [page](https://console.aws.amazon.com/sagemaker/home). From the service page click the `Notebook Instances` link on the far left menu bar.

![StackWizard5](static/imgs/img10.png)

To get to the Jupyter interface, simply click `Open JupyterLab` on the far right next to your notebook instance.

![StackWizard5](static/imgs/img11.png)

Clicking the open link will take a few seconds to redirect you to the Jupyter system but once there you should see a collection of files on your left. 

To get started navigate to the first notebook using [domain dataset groups and use-case optimized recommenders](https://docs.aws.amazon.com/personalize/latest/dg/create-domain-dataset-group.html).

`amazon-personalize-samples/getting_started/notebooks/Building_Your_First_Recommender_Video_On_Demand.ipynb`

`amazon-personalize-samples/getting_started/notebooks/Building_Your_First_Recommender_Ecommerce.ipynb`

or using [custom dataset groups](https://docs.aws.amazon.com/personalize/latest/dg/custom-dataset-groups.html):

`amazon-personalize-samples/getting_started/notebooks/1.Building_Your_First_Campaign.ipynb`

The rest of the lab will take place via the Jupyter notebooks, simply read each block before executing it and moving onto the next. If you have any questions about how to use the notebooks please ask your instructor or if you are working independently this is a pretty good video to get started:

https://www.youtube.com/watch?v=Gzun8PpyBCo

## After the Notebooks

Once you have completed all of the work in the Notebooks and have completed the cleanup steps there as well, the last thing to do is to delete the stack you created with CloudFormation. To do that, inside the AWS Console again click the `Services` link at the top, and this time enter in `CloudFormation` and click the link for it.

![StackWizard5](static/imgs/img9.png)

Click the `Delete` button on the demo stack you created:

![StackWizard5](static/imgs/img13.png)

Lastly click the `Delete Stack` button that shows up on the popup:

![StackWizard5](static/imgs/img14.png)

You'll now notice that the stack is in progress of being deleted. Once you see `Delete Completed` you know that everything has been deleted and you are 100% done with this lab.

