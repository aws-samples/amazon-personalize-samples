# Amazon Personalize 后续操作

关于如何开始使用 Amazon Personalize 各种功能的笔记本和示例

## Amazon Personalize 用例示例

[core_use_cases/](core_use_cases/) 文件夹中包含最常见用例的详细示例。

## 用于 Amazon Personalize 部署的可扩展 Operations 示例

[operations/](operations/) 文件夹中包含了以下主题的示例：

* [通过机器学习维护个性化体验](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
    - 此 AWS 解决方案允许您自动化导入以下端到端流程：数据集、创建解决方案和解决方案版本、创建和更新活动、创建筛选器以及运行批量推理作业。这些流程可以按需运行，也可以根据您定义的时间表触发运行。

* MLOps（旧版）
    - 该项目展示了如何使用 AWS Step Functions 以完全自动化的方式快速部署 Personalize 活动。如需开始，请导航至 [ml_ops](operations/ml_ops/) 文件夹，并按照 README 说明操作。这个示例已经被 AWS [用机器学习维护个性化体验](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)的解决方案所取代。

* MLOps Data Science SDK
    - 该项目展示了如何使用 AWS Data Science SDK 以完全自动化的方式快速部署 Personalize 活动。如需开始，请导航至 [ml_ops_ds_sdk](operations/ml_ops_ds_sdk/) 文件夹，并按照 README 说明操作。

* [个性化 API](https://github.com/aws-samples/personalization-apis)
    - 位于您的应用程序和 Amazon Personalize 等推荐系统之间的实时低延迟 API 框架。提供响应缓存、API Gateway 配置、使用 [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html) 进行 A/B 测试、推理时间项元数据、自动情境性推荐等的最佳实践实施。

* 流事件
    - 该项目展示了如何在您的 Amazon Personalize 活动和事件跟踪器端点前快速部署 API Layer。如需开始，请导航至 [streaming_events](operations/streaming_events/) 文件夹，并按照 README 说明操作。

* Lambda 示例
    - 这个文件夹从一个基本示例开始：通过使用 Lambda 函数处理来自 S3 的新数据，将 `put_events` 集成到您的 Personalize 活动中。如需开始，请导航至 [lambda_examples](operations/lambda_examples/) 文件夹，并按照 README 说明操作。

* 筛选器轮换
    - 这款[无服务器应用程序](operations/filter_rotator/)中包含一个 AWS Lambda 函数，该函数按计划执行，以轮换 Personalize 筛选器，该筛选器使用必须随时间更改的固定值表达式。例如，使用基于日期或时间值的区间运算符，旨在包括/排除基于滚动时间窗口的项。

* [Personalize Monitor](https://github.com/aws-samples/amazon-personalize-monitor)
    - 该项目添加了用于跨 AWS 环境运行 Amazon Personalize 的监控、警报、控制面板和优化工具。

## 参考架构

以下参考架构提供了如何跨行业应用 Amazon Personalize 的示例：

* 零售业 – [Retail Demo Store](https://github.com/aws-samples/retail-demo-store) 是一款全栈 Web 应用程序，它在 Web 应用程序、消息传收发和对话 AI 界面使用 Personalize 实现个性化。还有实践研讨会
* 媒体与娱乐业
* 旅游与酒店业

## 研讨会

[workshops/](workshops/) 文件夹中包含我们最新的研讨会列表：

* POC in a box
* re:invent 2019

## Data Science Tools

[data_science/](data_science/) 文件夹中包括关于如何实现输入数据集关键属性可视化的示例。

我们关注的关键组件包括：
- 缺失的数据、重复的事件，以及重复的项目消费
- 类别字段的幂律分布
- 冷启动适用性的时间漂移分析
- 分析用户会话分布

## 许可汇总

这个示例代码在修改后的 MIT 许可下可用。参见“许可”文件。
