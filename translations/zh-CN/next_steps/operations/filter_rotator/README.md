# Amazon Personalize 筛选器轮换功能

该项目包含用于部署无服务器应用程序的源代码和支持文件，该应用程序为 [Amazon Personalize](https://aws.amazon.com/personalize/) 提供自动[筛选](https://docs.aws.amazon.com/personalize/latest/dg/filter.html)轮换功能。Amazon Personalize 是 AWS 提供的一款 AI 服务，允许您根据自己的数据创建自定义 ML 推荐系统。项目亮点包括：

- 基于您提供的动态筛选器模板创建筛选器
- 基于您提供的动态筛选表达式模板构建筛选表达式
- 基于您提供的动态匹配表达式删除筛选器（可选）
- 创建或删除筛选器时将事件发布至 [Amazon EventBridge](https://aws.amazon.com/eventbridge/)（可选）

## <a name='Whatarefilters'></a>什么是筛选器？
Amazon Personalize 筛选器是一种很好的方法，可以在推荐返回到应用程序之前将业务规则应用到推荐。筛选器可用于根据考虑用户交互历史、项目元数据和用户元数据的类 SQL 语法，包括或排除向用户推荐的项目。例如，只推荐用户曾经看过或喜欢的电影来填充“再次观看”小部件。

```
INCLUDE ItemID WHERE Interactions.event_type IN ('watched','favorited')
```

或者排除推荐目前缺货的产品。

```
EXCLUDE ItemID WHERE Items.out_of_stock IN ('yes')
```

您甚至可以在运行时指定筛选器表达式值的地方使用动态筛选器。例如，只推荐特定类型的电影。

```
INCLUDE ItemID WHERE Items.genre IN ($GENRES)
```

要使用上述筛选器，您需要在使用 [GetRecommendations API](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetRecommendations.html) 检索推荐时为 `$GENRE` 变量传递相应的值。

您可以在[此处](https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/)和[此处](https://aws.amazon.com/blogs/machine-learning/amazon-personalize-now-supports-dynamic-filters-for-applying-business-rules-to-your-recommendations-on-the-fly/)的 AWS Personalize 博客文章中了解有关筛选器的更多信息。

## <a name='Whyisfilterrotationnecessary'></a>为什么需要筛选器轮换功能？
筛选器很棒！但会有一些限制。其中一项限制就是要能够为范围查询指定动态值（即 `<`、`<=`、`>`、`>=`）。例如，以下筛选器将推荐限制为由于过去的滚动点**不**受支持而创建的新项。

**这是行不通的！**
```
INCLUDE ItemID WHERE Items.creation_timestamp > $NEW_ITEM_THRESHOLD
```

解决这个限制的方法是使用带硬编码值的筛选器表达式进行范围查询。

**这行得通！**
```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

但是，这个方法不太灵活，也不可维护，因为静态筛选器表达式不会随着时间而推进。解决方法是定期更新您的筛选器表达式，以保持时间窗口滚动。可惜的是，筛选器无法更新，所以必须创建一个新的筛选器，您的应用程序必须转为使用新的筛选器，只有这样，之前的筛选器才能安全删除。

此无服务器应用程序的目的是使此过程更易于维护，方法是通过自动创建和删除筛选器，并允许您提供一个动态表达式，该表达式可在创建新筛选器时解析为相应的硬编码值。

## <a name='Hereshowitworks'></a>运作方式如下

AWS Lambda [函数](./src/filter_rotator_function/filter_rotator.py)由这个反复调用的应用程序部署。您可以控制该调度，它可以是一个 [Cron 或 Rate 表达式](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html)。只有在与当前筛选器名称模板匹配的筛选器不存在时，该函数才会创建一个新的筛选器，并且只会删除与删除模板匹配的现有筛选器。因此，即使在不必要时也可以多运行该函数（即，如果您没有可预测且连续的时间，则应轮换筛选器）。

筛选器轮换功能的关键是用于验证当前模板是否存在以及现有模板是否符合删除条件的模板。由于每次执行该函数时都会解析模板，因此解析值可能会随时间变化。我们来看一些示例。您在部署此应用程序时，将这些模板值作为 CloudFormation 参数提供。

### <a name="Currentfilternametemplate"></a>当前筛选器名称模板

假设您想使用一个只推荐最近创建的项目的筛选器。项目数据集中的`CREATION_TIMESTAMP`列是一个方便用于此目的的字段。这个列名是保留的，用于支持 `aws-user-personalization` 配方的冷门项目探索功能。该列的值必须以 `long` 的 Unix 时间戳格式表示（即从 Epoch 开始所经过的秒数）。下面的筛选器表达式限制了上个月创建的项目（`1633240824` 是写本文时一个月前的 Unix 时间戳）。

```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

或者，您可以使用筛选器自定义元数据列，使用更粗制和/或人类可读的格式，但仍然与范围查询类似，如 `YYYYMMDD`。

```
INCLUDE ItemID WHERE Items.published_date > 20211001
```

如前所述，筛选器无法更新。因此您不能只更改筛选器的筛选表达式。相反，您应该用新的表达式创建新筛选器，切换应用程序，使用新的筛选器，然后删除旧的筛选器。这需要使用可预测筛选器命名标准，以便应用程序可以自动切换，使用新的筛选器，而不需要更改编码。继续创建时间戳主题，筛选器名称可以是类似这样的。

```
filter-include-recent-items-20211101
```

假设我们每天都要轮换这个筛选器，那么第二天的筛选器名称将是 `filter-include-recent-items-20211004`，第三天将是 `filter-include-recent-items-20211005`，以此类推。由于您在任何时候可以拥有的活动筛选器数量有限，因此您无法预先创建大量筛选器。相反，该应用程序将根据需要动态创建新的筛选器，并在适当的时候删除旧的筛选器。实现这一点要通过您为筛选器名称和表达式定义的模板，这些模板在运行时会经过解析。下面是一个匹配上述方案的筛选器名称模板示例。

```
filter-include-recent-items-{{datetime_format(now,'%Y%m%d')}}
```

上述筛选器名称模板将在运行时解析并替换 `{{` 和 `}}` 字符（Handlebars 或 Mustache）中的表达式。在这种情况下，我们将当前时间表示为 `now`，并使用 `%Y%m%d` 日期格式表达式对时间进行格式化。结果（截止今天）为 `20211102`。如果轮换函数找到此名称的现有筛选器，则不需要创建新的筛选器。否则，将创建一个名为 `filter-include-recent-items-20211102` 的新筛选器。

`PersonalizeCurrentFilterNameTemplate` CloudFormation 模板参数是您如何指定您自己的自定义筛选器名称模板。

下面介绍了模板语法中可用的函数和操作符。

### <a name="Currentfilterexpressiontemplate"></a>当前筛选表达式模板

轮换并创建新筛选器时，我们还可能需要动态解析实际的筛选表达式。`PersonalizeCurrentFilterExpressionTemplate` CloudFormation 参数可以用于实现这一点。一些示例。

```
INCLUDE ItemID WHERE Items.CREATION_TIMESTAMP > {{int(unixtime(now - timedelta_days(30)))}}
```

```
INCLUDE ItemID WHERE Items.published_date > {{datetime_format(now - timedelta_days(30),'%Y%m%d')}}
```

上述模板根据解析时的当前时间解析为硬编码的筛选器表达式。第一个生成 30 天前的 Unix 时间戳（按照 Personalize 对 `CREATION_TIMESTAMP` 的要求，以秒表示）。第二个模板生成一个 30 天前日期的整数，以 `YYYYMMDD` 格式表示。

### <a name="Deletefiltermatchtemplate"></a>删除筛选器匹配模板

最后，在转换到新版本的筛选器之后，我们需要清理旧的筛选器。否则我们最终会达到极限。为此可以使用匹配模板的筛选器名称，并且可以以一种在创建新筛选器后延迟删除一段时间的方式编写。这样可以让您的应用程序有时间在删除旧筛选器之前从旧筛选器转换至新筛选器。`PersonalizeDeleteFilterMatchTemplate` CloudFormation 模板参数是指定删除筛选器匹配模板的地方。

下面的删除筛选器匹配模板将匹配以 `filter-include-recent-items-` 开头的筛选器名称，并且后缀名比今天早一天多。换句话说，在删除旧的筛选器之前，我们有 1 天时间将客户端应用程序转换至新的筛选器。这可以根据您的应用程序进行自定义。

```
starts_with(filter.name,'filter-include-recent-items-') and int(end(filter.name,8)) < int(datetime_format(now - timedelta_days(1),'%Y%m%d'))
```

任何触发此模板解析为 `true` 的筛选器都将被删除。其他的则会单独留下。注意，[ListFilters API](https://docs.aws.amazon.com/personalize/latest/dg/API_ListFilters.html) 响应的 [FilterSummary](https://docs.aws.amazon.com/personalize/latest/dg/API_FilterSummary.html) 中的所有可用字段都可用于此模板。例如，上面的模板匹配 `filter.name`。`filter.status`、`filter.creationDateTime`，和 `filter.lastUpdatedDateTime` 等其他筛选汇总字段也可以在模板逻辑中进行检查。

## <a name='Filterevents'></a>筛选事件

如果您想同步应用程序的配置，或者在创建或删除筛选器时收到通知，您可以选择配置轮换函数，将事件发布到 [Amazon EventBridge](https://aws.amazon.com/eventbridge/)。事件启动后，轮换函数会发布三种类型的事件详细信息：`PersonalizeFilterCreated`、`PersonalizeFilterCreateFailed` 和 `PersonalizeFilterDeleted`。每一种都有一个 `personalize.filter.rotator` 的 `Source` 事件，并包含创建或删除的筛选器的详细信息。允许您设置 EventBridge 规则来按照您的意愿处理事件。例如，创建一个新筛选器时，您可以在 Lambda 函数中处理 `PersonalizeFilterCreated` 事件，更新应用程序的配置，从而在推断调用中切换使用新的筛选器。
## <a name='Filtertemplatesyntax'></a>筛选器模板语法

[Simple Eval](https://github.com/danthedeckie/simpleeval) 库被用作模板语法的基础。它提供了一种比使用 Python [eval](https://docs.python.org/3/library/functions.html#eval) 函数更安全、更沙盒化的替代方法。有关可用函数和示例的详细信息，请查看 Simple Eval 库文档。

作为该应用程序的一部分，添加了以下附加函数，以使编写模板更容易轮换筛选器。

- `unixtime(value)`：返回给定 string、datetime、date 或 time 的 Unix 时间戳值。如果提供了一个字符串，它将首先被解析为一个 datetime。
- `datetime_format(date, pattern)`：使用指定模式格式化 datetime、date 或 time。
- `timedelta_days(int)`：返回数天的 timedelta。可以用于日期计算。
- `timedelta_hours(int)`：返回数小时的 timedelta。可以用于日期计算。
- `timedelta_minutes(int)`：返回数分钟的 timedelta。可以用于日期计算。
- `timedelta_seconds(int)`：返回数秒的 timedelta。可以用于日期计算。
- `starts_with(str, prefix)`：如果字符串值以 prefix 开头，则返回“True”。
- `ends_with(str, suffix)`：如果字符串值以 suffix 结尾，则返回“True”。
- `start(str, num)`：返回字符串值的第一个 num 字符。
- `end(str, num)`：返回字符串值的最后一个 num 字符。
- `now`：当前的 datetime

## <a name='Installingtheapplication'></a>安装应用程序

***重要提示：**在 AWS 账户中部署此应用程序将创建和使用 AWS 资源，这需要花钱。Lambda 函数根据您提供的时间表调用，但调用频率通常不应该超过每小时一次。Personalize 不收取筛选器的费用，但您账户中可随时处于活跃状态的筛选器数量有限。在任何时间点处于待处理或正在进行状态的筛选器数量也有限制。因此，如果安装此应用程序后，您选择不使用，作为解决方案的一部分，请确保根据下一节中的卸载说明进行卸载，避免产生持续费用并清理所有数据。*

该应用程序使用 AWS [Serverless Application Model](https://aws.amazon.com/serverless/sam/)（SAM）建立资源并将资源部署到您的 AWS 账户。

要使用 SAM CLI，您需要在本地安装以下工具。

* SAM CLI – [安装 SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 已安装](https://www.python.org/downloads/)
* Docker – [安装 Docker 社区版](https://hub.docker.com/search/?type=edition&offering=community)

首次构建和部署该应用程序，请在您的 shell 中运行以下命令：

```bash
sam build --use-container --cached
sam deploy --guided
```

如果第一个命令提示错误，不能从 `public.ecr.aws` 下载 Docker 镜像，那么您可能需要登录。请运行以下命令，然后重试以上两个命令。

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

第一个命令将构建应用程序的源代码。第二个命令会将应用程序打包并部署到您的 AWS 账户，并提供一系列提示：

| 提示/参数 | 说明 | 默认设置 |
| --- | --- | --- |
| 堆栈名称 | 用于部署 CloudFormation 的堆栈的名称。该名称应为您账户和您所在区域的唯一名称。 | `personalize-filter-rotator` |
| AWS 区域 | 您希望将此应用程序部署到的 AWS 区域。 | 您的当前区域 |
| PersonalizeDatasetGroupArn 参数 | Amazon Personalize 数据集组 ARN，用于轮换其中的筛选器。 | |
| PersonalizeCurrentFilterNameTemplate 参数 | 检查和创建当前筛选器时使用的模板。 | |
| PersonalizeCurrentFilterExpressionTemplate 参数 | 创建当前筛选器并构建筛选表达式时使用的模板。 | |
| PersonalizeDeleteFilterMatchTemplate 参数（可选） | 用于匹配应该删除的现有筛选器的模板。 | |
| RotationSchedule 参数 | 用于控制轮换函数调用频率的 Cron 或 Rate 表达式。 | `rate(1 day)` |
| Timezone 参数 | 设置轮换函数 Lambda 环境的时区以匹配您自己的环境。 | `UTC` |
| PublishFilterEvents 参数 | 是否在创建和删除筛选器时将事件发布到默认的 EventBridge 总线。 | `Yes` |
| 部署前确认变更 | 如果设为“Yes”，将在执行之前显示任何 CloudFormation 变更集，以进行手动检查。如果设为“No”，AWS SAM CLI 会自动部署应用程序变更。 | |
| 允许 SAM CLI IAM 角色创建 | 由于此应用程序创建 IAM 角色以允许 Lambda 函数访问 AWS 服务，因此此设置必须为 `Yes`。 | |
| 将参数保存到 samconfig.toml | 如果设为“Yes”，您的选择将被保存到应用程序内的配置文件中，以便将来您可以在没有参数的情况下重新运行 `sam deploy`，以将变更部署到应用程序中。 | |

**TIP**：SAM 命令行工具提供了将参数值保存到本地文件（`samconfig.toml`）的选项，以便在下次部署应用程序时将它们作为默认值使用。但是，SAM 将参数值置于双引号中。因此，如果您的模板参数值包含嵌入的字符串值（如上述示例中显示的日期格式表达式），请确保这些嵌入的值使用单引号。否则，您的参数值将无法正确保存。

## <a name='Uninstallingtheapplication'></a>卸载应用程序

如需删除此应用程序在您的 AWS 账户中创建的资源，请使用 AWS CLI。假设您使用默认的应用程序名称作为堆栈名称（`personalize-filter-rotator`），您可以运行以下命令：

```bash
aws cloudformation delete-stack --stack-name personalize-filter-rotator
```

或者，您可以在 AWS 控制台中删除 CloudFormation 中的堆栈。

## <a name='FAQs'></a>常见问题解答

***问：部署此解决方案后，如何更改轮换器脚本的运行频率？***

***答：***有两个选择。以不同频率重新部署此解决方案。这将创建一个变更集，仅以新的频率更新 EventBridge 规则。或者，您可以直接在您的 AWS 账户中编辑该解决方案创建的 EventBridge 规则。

***问：如何用这个解决方案以不同的模板和更新频率轮换多个筛选器？***

***答：***部署该解决方案后，您可以创建额外的 EventBridge 规则，用不同的输入值调用轮换函数。对于规则目标，选择轮换函数并指定一个 JSON 常量的输入值，格式如下：

```javascript
{
    "datasetGroupArn": "[INSERT_PERSONALIZE_DATASET_GROUP_ARN]",
    "currentFilterNameTemplate": "[INSERT_CURRENT_FILTER_NAME_TEMPLATE]",
    "currentFilterExpressionTemplate": "[INSERT_CURRENT_FILTER_EXPRESSION_TEMPLATE]",
    "deleteFilterMatchTemplate": "[INSERT_DELETE_FILTER_MATCH_TEMPLATE]"
}
```

## <a name='Licensesummary'></a>许可汇总

这个示例代码在修改后的 MIT 许可下可用。参见“许可”文件。
