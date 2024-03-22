# Amazon Personalize 样本

关于如何开始使用 Amazon Personalize 各种功能的笔记本和示例

## Amazon Personalize 入门指南

[getting_started/](getting_started/) 文件夹中包含一个 CloudFormation 模板，该模板将部署您通过 Amazon Personalize 构建第一个活动所需的所有资源。

提供的笔记本还可以作为模板，供您使用自己的数据构建模型。该存储库已复制到该环境中，所以您可以用这种方法探索更多高级笔记本。

## Amazon Personalize 后续操作

[next_steps/](next_steps/) 文件夹中包含您的 Amazon Personalize 旅程中下列常见后续步骤的详细示例。该文件夹包含以下进阶内容：

* 核心用例
  - [用户个性化](next_steps/core_use_cases/user_personalization)
  - [个性化排名](next_steps/core_use_cases/personalized_ranking)
  - [相关项目](next_steps/core_use_cases/related_items)
  - [批量推荐](next_steps/core_use_cases/batch_recommendations)
  - [用户细分](next_steps/core_use_cases/user_segmentation)

* 用于 Amazon Personalize 部署的可扩展 Operations 示例
    - [通过机器学习维护个性化体验](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
        - 此 AWS 解决方案允许您自动化导入以下端到端流程：数据集、创建解决方案和解决方案版本、创建和更新活动、创建筛选器以及运行批量推理作业。这些流程可以按需运行，也可以根据您定义的时间表触发运行。
    - [MLOps Step Function](next_steps/operations/ml_ops)（旧版）
        - 该项目展示了如何使用 AWS Step Functions 以完全自动化的方式快速部署 Personalize 活动。如需开始，请导航至 [ml_ops](next_steps/operations/ml_ops) 文件夹，并按照 README 说明操作。这个示例已经被 AWS [用机器学习维护个性化体验](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)的解决方案所取代。
    - [MLOps Data Science SDK](next_steps/operations/ml_ops_ds_sdk)
        - 该项目展示了如何使用 AWS Data Science SDK 以完全自动化的方式快速部署 Personalize 活动。如需开始，请导航至 [ml_ops_ds_sdk](next_steps/operations/ml_ops_ds_sdk) 文件夹，并按照 README 说明操作。
    - [个性化 API](https://github.com/aws-samples/personalization-apis)
        - 位于您的应用程序和 Amazon Personalize 等推荐系统之间的实时低延迟 API 框架。提供响应缓存、API Gateway 配置、使用 [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html) 进行 A/B 测试、推理时间项元数据、自动情境性推荐等的最佳实践实施。
    - [Lambda 示例](next_steps/operations/lambda_examples)
        - 这个文件夹从一个基本示例开始：通过使用 Lambda 函数处理来自 S3 的新数据，将 `put_events` 集成到您的 Personalize 活动中。如需开始，请导航至 [lambda_examples](next_steps/operations/lambda_examples) 文件夹，并按照 README 说明操作。
    - [Personalize Monitor](https://github.com/aws-samples/amazon-personalize-monitor)
        - 该项目添加了用于跨 AWS 环境运行 Amazon Personalize 的监控、警报、控制面板和优化工具。
    - [流事件](next_steps/operations/streaming_events)
        - 该项目展示了如何在您的 Amazon Personalize 活动和事件跟踪器端点前快速部署 API Layer。如需开始，请导航至 [streaming_events](operations/streaming_events/) 文件夹，并按照 README 说明操作。
    - [筛选器轮换](next_steps/operations/filter_rotator)
        - 这款无服务器应用程序中包含一个 AWS Lambda 函数，该函数按计划执行，以旋转 Personalize 筛选器，该筛选器使用必须随时间更改的固定值表达式。例如，使用基于日期或时间值的区间运算符，旨在包括/排除基于滚动时间窗口的项。

* 研讨会
    - [workshops/](next_steps/workshops/) 文件夹中包含我们最新的研讨会列表：
        - [POC in a box](next_steps/workshops/POC_in_a_box)
        - [re:Invent 2019](next_steps/workshops/Reinvent_2019)
        - [沉浸日](next_steps/workshops/Immersion_Day)
    - [合作伙伴集成](https://github.com/aws-samples/retail-demo-store#partner-integrations)
        - 探索演示如何与 Amplitude、Braze、Optimizely 和 Segment 等合作伙伴使用 Personalize 的研讨会。

* Data Science Tools
    - [data_science/](next_steps/data_science/) 文件夹中包括关于如何实现输入数据集关键属性可视化的示例。
        - 缺失的数据、重复的事件，以及重复的项目消费
        - 类别字段的幂律分布
        - 冷启动适用性的时间漂移分析
        - 分析用户会话分布

* 演示/参考架构
    - [Retail Demo Store](https://github.com/aws-samples/retail-demo-store)
        - 零售 Web 应用程序和研讨会平台示例，用于演示如何通过 Amazon Personalize 提供全方位的个性化客户体验。

## 许可汇总

这个示例代码在修改后的 MIT 许可下可用。参见“许可”文件。
