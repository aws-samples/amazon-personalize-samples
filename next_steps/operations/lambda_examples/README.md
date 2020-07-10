# Lambda Examples

This folder starts with a basic example of integrating `put_events` into your Personalize Campaigns by using Lambda functions processing new data from S3.

To get started here, first complete the `getting_started` notebook collection, including the second notebook that creates your initial Event Tracker.


## Sending Events to S3

Inside this folder you'll see a notebook `Sending_Events_to_S3.ipynb` it contains the boilerplate code to send a series of messages to your S3 bucket.

This will be key for using your Lambda function which will then send them to Personalize.

## Lambda Function

The notebook will now reliabily write files to your S3 bucket, the next task is to build a lambda function to invoke on the S3 trigger. The code for the Lambda is provided inside `event_processor.py`


First visit the Lambda console then click `Create Function`, give it any name you like and select Python 3.6 for the runtime.

You will need a new IAM role for this Lambda function, allow a default one first. Later it will be updated to work with Personalize and S3. Next hit `Create function`


Now click the `+ Add trigger`, search for S3, select your bucket, select `All object create events` for demo purposes, then for Suffix add `.json`. Lastly on this page click `Add`

Next click the icon for your Lamda function, when the editor appears below, copy the contents of `event_processor.py` into the editor and save it. Replace all the existing content.

Scroll down below the editor and for `Environment Variables` enter `trackingId` for a key, and for the value provide your tracking ID from the second notebook.

This is almost ready to go, the last configuration bit is to handle IAM, scroll below until you see `Execution role`, at the bottom you'll see a link `View the ....` right click and open that in a new tab.

Click `Attach policies`, add both `AmazonS3FullAccess` and `AmazonPersonalizeFullAccess` then click `Attach policy`. These configurations are not ideal for security but will illustrate the point. For a production workload create custom policies tailored explicitly to the resources you are working with.

Once attached, close the tab and revisit the Lambda Console page you left. Click `Save` in the top right corner.

Scroll back to the top, and select `Monitoring`, then go back to your notebook that simulates the events and execute that cell again to write new files and execute the Lambda function.

After a few seconds you can refresh the page and see the invocations were successful.
