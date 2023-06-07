# Creating the CloudFormation stack in other regions



1. Populate the region code in URL below and the launch cloudformation template. Be sure to be logged into your AWS account before doing so. Refer to the [AWS regions list] (https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html#Concepts.RegionsAndAvailabilityZones.Regions) to identify the corresponding region code.
````
    https://console.aws.amazon.com/cloudformation/home?region=<region-code>#/stacks/new?stackName=personalize-auto-context-stack&templateURL=https://personalize-solution-staging-us-east-1.s3.amazonaws.com/personalize-auto-context/personalize-auto-context-template.yml
````
2. Click "Next".
3. Proceed as usual from there to create the stack.
