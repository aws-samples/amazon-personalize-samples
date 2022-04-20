![banner](static/imgs/MagicMovieMachine_banner.png)
# Building your own movie recommender
This tutorial walks you through building your own movie recommender.
You will see how you can create resources in Amazon Personalize that generate recommendations, just like the Magic Movie Machine!

## Tutorial overview
Completing this tutorial involes the following steps:

1. Follow the instructions in this file to build your environment and find the notebooks in AWS Sagemaker. This involves deploying an AWS CloudFormation stack that sets up the notebook environment for you.
2. Run the `Building_the_Magic_Movie_Machine_Recommender.ipynb` notebook on AWS Sagemaker. You deployed this notebook in step one. This notebook guides you through building your first movie recommenders and getting your first recommendations.
3. Run the `Clean_Up_Resources.ipynb`. This notebook deletes anything that was created in the previous notebook so you are not charged for additional resources. 
4. Delete the AWS CloudFormation stack to delete environment resources you created in step 2.

*Note*: You can explore the notebook directly in github. However, to successfully run it you must follow the steps below to deploy the notebook in a preconfigured environment.

## Building your Environment 
Before you can build your own movie recommender, you must building a work environment as follows:

1. Make sure you have satisfied the environment prerequsites listed below.
2. Deploy the AWS CloudFormation stack.
3. Navigate to the Amazon SageMaker console 

### Environment Prerequisites

To deploy with the CloudFormation template, you must have the following.

1. An AWS Account
2. A user with administrator access to the AWS Account

### Deploying the Environment

The first step is to deploy a CloudFormation template that will perform much of the initial setup for you. In another browser window login to your AWS account. Once you have done that open the link below in a new tab to start the process of deploying the items you need via CloudFormation.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=PersonalizeDemo&templateURL=https://amazon-personalize-github-samples.s3.amazonaws.com/PersonalizeDemo.yaml)

Follow along with the screenshots below if you have any questions about these steps.

<details>
  <summary>Click to expand the instructions</summary>
  
### Using the AWS CloudFormation Wizard

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


### Using the Notebooks

Start by navigating to the Amazon SageMaker landing [page](https://console.aws.amazon.com/sagemaker/home). From the service page click the `Notebook Instances` link on the far left menu bar.

![StackWizard5](static/imgs/img10.png)

To get to the Jupyter interface, simply click `Open JupyterLab` on the far right next to your notebook instance.

![StackWizard5](static/imgs/img11.png)

Clicking the open link will take a few seconds to redirect you to the Jupyter system but once there you should see a collection of files on your left. 

To get started navigate to the next_steps folder > workshops > magic_movie_machine > notebooks > Building the Magic Movie Machine Recommender.pynb

`amazon-personalize-samples/next_steps/workshops/magic_movie_machine/notebooks/Building the Magic Movie Machine Recommender.ipynb`


Make sure to choose a kernel that uses Python 3.x (kernel name will end with p3x) before you run the lab. The rest of the lab will take place via the Jupyter notebooks, simply read each block before executing it and moving onto the next. If you have any questions about how to use the notebooks, this is a pretty good video to get started:

https://www.youtube.com/watch?v=Gzun8PpyBCo

## Deleting environment resources

Once you have completed all of the work in the Notebooks and have completed the cleanup steps there as well, the last thing to do is to delete the stack you created with CloudFormation. To do that, inside the AWS Console again click the `Services` link at the top, and this time enter in `CloudFormation` and click the link for it.

![StackWizard5](static/imgs/img9.png)

Click the `Delete` button on the demo stack you created:

![StackWizard5](static/imgs/img13.png)

Lastly click the `Delete Stack` button that shows up on the popup:

![StackWizard5](static/imgs/img14.png)

You'll now notice that the stack is in progress of being deleted. Once you see `Delete Completed` you know that everything has been deleted and you are 100% done with this lab.

