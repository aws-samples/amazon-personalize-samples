# Amazon Personalize Filter Rotation

This project contains the source code and supporting files for deploying a serverless application that provides automatic [filter](https://docs.aws.amazon.com/personalize/latest/dg/filter.html) rotation capabilities for [Amazon Personalize](https://aws.amazon.com/personalize/), an AI service from AWS that allows you to create custom ML recommenders based on your data. Project highlights include:

- Creates filters based on a dynamic filter naming template you provide
- Builds filter expressions based on a dynamic filter expression template you provide
- Deletes filters based on a dynamic matching expression you provide (optional)
- Publishes events to [Amazon EventBridge](https://aws.amazon.com/eventbridge/) when filters are created or deleted (optional)

## <a name='Whatarefilters'></a>What are filters?
Amazon Personalize filters are a great way to have business rules applied to recommendations before they are returned to your application. They can be used to include or exclude items from being recommended for a user based on a SQL-like syntax that considers the user's interaction history, item metadata, and user metadata. For example, only recommend movies that the user has watched or favorited in the past to populate a "Watch again" widget.

```
INCLUDE ItemID WHERE Interactions.event_type IN ('watched','favorited')
```

Or exclude products from being recommended that are currently out of stock.

```
EXCLUDE ItemID WHERE Items.out_of_stock IN ('yes')
```

You can even use dynamic filters where the filter expression values are specified at runtime. For example, only recommend movies for a specific genre.

```
INCLUDE ItemID WHERE Items.genre IN ($GENRES)
```

To use the filter above, you would pass the appropriate value(s) for the `$GENRE` variable when retrieving recommendations using the [GetRecommendations API](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetRecommendations.html).

You can learn more about filters on the AWS Personalize blog [here](https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) and [here](https://aws.amazon.com/blogs/machine-learning/amazon-personalize-now-supports-dynamic-filters-for-applying-business-rules-to-your-recommendations-on-the-fly/).

## <a name='Whyisfilterrotationnecessary'></a>Why is filter rotation necessary?
Filters are great! However, if you need to periodically change filters on a predictable schedule or in a particular way, it can be difficult to implement this functionality.

**NOTE: one of the original purposes for creating this solution was to work around a limitation where dynamic filters could not be used with range operators (i.e., `<`, `<=`, `>`, `>=`). This limitation has been addressed and you can now combine dynamic filters with range operators. Nevertheless, we are keeping this solution around in case it's useful for other purposes.**

The purpose of this serverless application is to make this process easier to maintain by automating the creation and deletion of filters and allowing you to provide a dynamic expression that is resolved to the appropriate hard-coded value when the new filter is created.

## <a name='Hereshowitworks'></a>Here's how it works

An AWS Lambda [function](./src/filter_rotator_function/filter_rotator.py) is deployed by this application that is called on a recurring basis. You control the schedule which can be a [cron or rate expression](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html). The function will only create a new filter if a filter does not already exist that matches the current filter name template and it will only delete existing filters that match the delete template. Therefore, it is fine to have the function run more often than necessary (i.e. if you don't have a predictable and consistent time when filters should be rotated).

The key to the filter rotation function is the templates used to verify that the current template exists and if existing template(s) are eligible to delete. Since the templates are resolved each time the function is executed, the resolved value can change over time. Let's look at some examples. You provide these template values as CloudFormation parameters when you deploy this application.

### <a name="Currentfilternametemplate"></a>Current filter name template

Let's say you want to use a filter that only recommends recently created items. The `CREATION_TIMESTAMP` column in the items dataset is a convenient field to use for this. This column name is reserved and is used to support the cold item exploration feature of the `aws-user-personalization` recipe. Values for this column must be expressed in the Unix timestamp format as `long`'s (i.e., number of seconds since the Epoch). The following filter expression limits items that were created in the last month (`1633240824` is the Unix timestamp for 1 month ago as of this writing).

```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

Alternatively, you can use a custom metadata column for the filter that uses a more coarse and/or human readable format but is still comparable for range queries, like `YYYYMMDD`.

```
INCLUDE ItemID WHERE Items.published_date > 20211001
```

As noted earlier, filters cannot be updated. Therefore you can't just change the filter expression of the filter. Instead, you have to create a new filter with a new expression, switch your application to use the new filter, and then delete the old filter. This requires using a predictable naming standard for filters so applications can automatically switch to using the new filter without a coding change. Continuing with the creation timestamp theme, the filter name could be something like.

```
filter-include-recent-items-20211101
```

Assuming we want to rotate this filter each day, the next day's filter name would be `filter-include-recent-items-20211004`, the next would be `filter-include-recent-items-20211005`, and so on as time passes. Since there are limits on how many active filters you can have at any time, you cannot precreate a large number of filters. Instead, this application will dynamically create new filters as needed and delete old ones when appropriate. What makes this work is the templates that you define for the filter name and expression and that they are resolved at run-time. Here is an example of a filter name template that matches the scheme described above.

```
filter-include-recent-items-{{datetime_format(now,'%Y%m%d')}}
```

The above filter name template will resolve and replace the expression within the `{{` and `}}` characters (handlebars or mustaches) at run-time. In this case, we are taking the current time expressed as `now` and formatting it using the `%Y%m%d` date format expression. The result (as of today) is `20211102`. If the rotation function finds an existing filter with this name, a new filter does not need to be created. Otherwise, a new filter is created using `filter-include-recent-items-20211102` as the name.

The `PersonalizeCurrentFilterNameTemplate` CloudFormation template parameter is how you specify your own custom filter name template.

The functions and operators available to use in template syntax are described below.

### <a name="Currentfilterexpressiontemplate"></a>Current filter expression template

When rotating and creating the new filter, we also may have to dynamically resolve the actual filter expression. The `PersonalizeCurrentFilterExpressionTemplate` CloudFormation parameter can be used for this. Some examples.

```
INCLUDE ItemID WHERE Items.CREATION_TIMESTAMP > {{int(unixtime(now - timedelta_days(30)))}}
```

```
INCLUDE ItemID WHERE Items.published_date > {{datetime_format(now - timedelta_days(30),'%Y%m%d')}}
```

The above templates resolve to a hard-coded filter expression based on current time when they're resolved. The first produces a Unix timestamp (expressed in seconds as required by Personalize for `CREATION_TIMESTAMP`) that is 30 days ago. The second template produces an integer representing the date in `YYYYMMDD` format from 30 days ago.

### <a name="Deletefiltermatchtemplate"></a>Delete filter match template

Finally, we need to clean up old filters after we have transitioned to a newer version of the filter. Otherwise we will eventually hit a limit. A filter name matching template can be used for this and can be written in such a way to delay the deletion for some time after the new filter is created. This gives your application time to transition from the old filter to the new filter before the old filter is deleted. The `PersonalizeDeleteFilterMatchTemplate` CloudFormation template parameter is where you specify the delete filter match template.

The following delete filter match template will match on filters with a filter name that start with `filter-include-recent-items-` and have a suffix that is more than one day older than today. In other words, we have 1 day to transition client applications to the new filter before the old filter is deleted. This can be customized however suits your application.

```
starts_with(filter.name,'filter-include-recent-items-') and int(end(filter.name,8)) < int(datetime_format(now - timedelta_days(1),'%Y%m%d'))
```

Any filters that trigger this template to resolve to `true` will be deleted. All others will be left alone. Note that all fields available in the [FilterSummary](https://docs.aws.amazon.com/personalize/latest/dg/API_FilterSummary.html) of the [ListFilters API](https://docs.aws.amazon.com/personalize/latest/dg/API_ListFilters.html) response are available to this template. For example, the template above matches on `filter.name`. Other filter summary fields such as `filter.status`, `filter.creationDateTime`, and `filter.lastUpdatedDateTime` can also be inspected in the template's logic.

## <a name='Filterevents'></a>Filter events

If you'd like to synchronize your application's configuration or be notified when a filter is created or deleted, you can optionally configure the rotator function to publish events to [Amazon EventBridge](https://aws.amazon.com/eventbridge/). When events are enabled, there are three event detail types published by the rotator function: `PersonalizeFilterCreated`, `PersonalizeFilterCreateFailed`, and `PersonalizeFilterDeleted`. Each has an event `Source` of `personalize.filter.rotator` and includes details on the filter created or deleted. This allows you to setup EventBridge rules to process events as you please. For example, when a new filter is created, you can process the `PersonalizeFilterCreated` event in a Lambda function to update your application's configuration to switch to using the new filter in inference calls.
## <a name='Filtertemplatesyntax'></a>Filter template syntax

The [Simple Eval](https://github.com/danthedeckie/simpleeval) library is used as the foundation of for the template syntax. It provides a safer and more sandboxed alternative than using Python's [eval](https://docs.python.org/3/library/functions.html#eval) function. Check the Simple Eval library documentation for details on the functions available and examples.

The following additional functions were added as part of this application to make writing templates easier for rotating filters.

- `unixtime(value)`: Returns the Unix timestamp value given a string, datetime, date, or time. If a string is provided, it will be parsed into a datetime first.
- `datetime_format(date, pattern)`: Formats a datetime, date, or time using the specified pattern.
- `timedelta_days(int)`: Returns a timedelta for a number of days. Can be used for date math.
- `timedelta_hours(int)`: Returns a timedelta for a number of hours. Can be used for date math.
- `timedelta_minutes(int)`: Returns a timedelta for a number of minutes. Can be used for date math.
- `timedelta_seconds(int)`: Returns a timedelta for a number of seconds. Can be used for date math.
- `starts_with(str, prefix)`: Returns True if the string value starts with prefix.
- `ends_with(str, suffix)`: Returns True if the string value ends with suffix.
- `start(str, num)`: Returns the first num characters of the string value
- `end(str, num)`: Returns the last num characters of the string value
- `now`: Current datetime

## <a name='Installingtheapplication'></a>Installing the application

***IMPORTANT NOTE:** Deploying this application in your AWS account will create and consume AWS resources, which will cost money. The Lambda function is called according to the schedule you provide but typically should not need to be called more often than hourly. Personalize does not charge for filters but your account does have a limit on the number of filters that are active at any time. There are also limits on how many filters can be in a pending or in-progress status at any point in time. Therefore, if after installing this application you choose not to use it as part of your solution, be sure to follow the Uninstall instructions in the next section to avoid ongoing charges and to clean up all data.*

This application uses the AWS [Serverless Application Model](https://aws.amazon.com/serverless/sam/) (SAM) to build and deploy resources into your AWS account.

To use the SAM CLI, you need the following tools installed locally.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy the application for the first time, run the following in your shell:

```bash
sam build --use-container --cached
sam deploy --guided
```

If you receive an error from the first command about not being able to download the Docker image from `public.ecr.aws`, you may need to login. Run the following command and then retry the above two commands.

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

The first command will build the source of the application. The second command will package and deploy the application to your AWS account, with a series of prompts:

| Prompt/Parameter | Description | Default |
| --- | --- | --- |
| Stack Name | The name of the stack to deploy to CloudFormation. This should be unique to your account and region. | `personalize-filter-rotator` |
| AWS Region | The AWS region you want to deploy this application to. | Your current region |
| Parameter PersonalizeDatasetGroupArn | Amazon Personalize dataset group ARN to rotate filters within. | |
| Parameter PersonalizeCurrentFilterNameTemplate | Template to use when checking and creating the current filter. | |
| Parameter PersonalizeCurrentFilterExpressionTemplate | Template to use when building the filter expression when creating the current filter. | |
| Parameter PersonalizeDeleteFilterMatchTemplate (optional) | Template to use to match existing filters that should be deleted. | |
| Parameter RotationSchedule | Cron or rate expression to control how often the rotation function is called. | `rate(1 day)` |
| Parameter Timezone | Set the timezone of the rotator function's Lambda environment to match your own. | `UTC` |
| Parameter PublishFilterEvents | Whether to publish events to the default EventBridge bus when filters are created and deleted. | `Yes` |
| Confirm changes before deploy | If set to yes, any CloudFormation change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes. | |
| Allow SAM CLI IAM role creation | Since this application creates IAM roles to allow the Lambda functions to access AWS services, this setting must be `Yes`. | |
| Save arguments to samconfig.toml | If set to yes, your choices will be saved to a configuration file inside the application, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application. | |

**TIP**: The SAM command-line tool provides the option to save your parameter values in a local file (`samconfig.toml`) so they're available as defaults the next time you deploy the app. However, SAM wraps your parameter values in double-quotes. Therefore, if your template parameter values contain embedded string values (like the date format expressions shown in the examples above), be sure to use single-quotes for those embedded values. Otherwise, your parameter values will not be properly preserved.

## <a name='Uninstallingtheapplication'></a>Uninstalling the application

To remove the resources created by this application in your AWS account, use the AWS CLI. Assuming you used the default application name for the stack name (`personalize-filter-rotator`), you can run the following:

```bash
aws cloudformation delete-stack --stack-name personalize-filter-rotator
```

Alternatively, you can delete the stack in CloudFormation in the AWS console.

## <a name='FAQs'></a>FAQs

***Q: How can I change the frequency that the rotator script runs once this solution is deployed?***

***A:*** Two options here. Either redeploy this solution with a different frequency. A change set will be created that only updates the EventBridge rule with the new frequency. Otherwise, you can edit the EventBridge rule created by this solution directly in your AWS account.

***Q: How do I use this solution to rotate multiple filters with different templates and different update frequencies?***

***A:*** Once you deploy this solution, you can create additional EventBridge rules that call the rotator function with different input values. For the rule target, select the rotator function and specify an input value that is constant JSON in the following format:

```javascript
{
    "datasetGroupArn": "[INSERT_PERSONALIZE_DATASET_GROUP_ARN]",
    "currentFilterNameTemplate": "[INSERT_CURRENT_FILTER_NAME_TEMPLATE]",
    "currentFilterExpressionTemplate": "[INSERT_CURRENT_FILTER_EXPRESSION_TEMPLATE]",
    "deleteFilterMatchTemplate": "[INSERT_DELETE_FILTER_MATCH_TEMPLATE]"
}
```

## <a name='Licensesummary'></a>License summary

This sample code is made available under a modified MIT license. See the LICENSE file.
