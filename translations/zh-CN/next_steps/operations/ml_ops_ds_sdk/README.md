## 使用 AWS Step Functions Data Science SDK 实现 Personalize 工作流自动化

随着机器学习（ML）在公司核心业务中占据的份量越来越重，缩短从模型创建到部署的时间就变得越来越重要。2019 年 11 月，AWS 发布了适用于 Amazon SageMaker 的 AWS Step Functions Data Science SDK，开发人员可以通过这款开源开发工具包使用 Python 创建基于 Step Functions 的机器学习工作流。现在，您可以使用这款 SDK，使用与模型开发所用的同款工具创建可重复使用的模型部署工作流。您可以在我们 GitHub 存储库的“automate_personalize_workflow”文件夹中找到该解决方案的完整笔记本。

该存储库用一个常见用例演示了 Data Science SDK 的功能：如何实现 Personalize 自动化。在这篇文章中，您将创建一个无服务器工作流来训练一个电影推荐引擎。最后展示了如何根据周期性计划触发工作流。

### 本文使用了以下 AWS 服务：
•	AWS Step Functions 使您能够将多个 AWS 服务整合至一个无服务器工作流中。您可以设计并执行工作流，其中，一个步骤的输出作为下一个步骤的输入，并支持将错误处理嵌入到工作流中。\
•	AWS Lambda 是一项让您在运行代码时无需预置或管理服务器的计算服务。Lambda 仅当被触发时才会执行您的代码，并且支持自动扩展，从每天处理几个请求扩展到每秒可处理数千个请求。\
•	Amazon Personalize 是一项机器学习服务，能够让您使用可以在 Amazon Personalize 中创建的自定义机器学习模型，来个性化您的网站、应用程序、广告、电子邮件等，并且无需机器学习经验。

## SDK 概述
此 SDK 提供了一种使用 AWS Step Functions 的新方式。一个 Step Function 是由多个离散步骤组成的状态机。其中，每个步骤都可以执行任务、作出选择、启动并行执行或管理超时。您可以开发单独的步骤并使用 Step Functions 来处理整个工作流的触发、协调和状态管理。在 Data Science SDK 诞生之前，您只能使用基于 JSON 的 Amazon States Language 来定义 Step Functions。现在，您可以借助此 SDK 使用 Python 代码轻松创建、执行和可视化 Step Functions。

本文提供了此 SDK 的概述，包括如何创建 Step Function 步骤、使用参数、集成服务特定的功能以及将这些步骤关联在一起以创建和可视化工作流。您可以在本文中找到多个示例代码；同时，我们也为整个流程创建了详细的 Amazon SageMaker 笔记本。

## Amazon Personalize 概述
Amazon Personalize 是一项机器学习服务，让开发人员能够轻松为使用他们应用程序的客户创建个性化推荐。

机器学习为个性化的产品和内容推荐、定制化搜索结果和定向营销推广等提供支持，被越来越多地用于提高客户参与度。然而，开发生产这些复杂的推荐系统所需的机器学习能力已经超出了当今大多数组织的能力范围，因为太过复杂。Amazon Personalize 能够让没有机器学习经验的开发人员，利用 Amazon.com 通过多年的应用而完善的机器学习技术，轻松将复杂的个性化功能构建到他们的应用程序中。

有了 Amazon Personalize，您可以从您的应用程序中提供活动流：点击量、页面浏览量、注册量、购买量等等，以及一个您想推荐的项目清单，如文章、产品、视频或音乐。您还可以选择向 Amazon Personalize 提供来自用户的其他人口统计信息，如年龄或地理位置。Amazon Personalize 会处理并检查数据、确定哪些数据有意义、选择正确的算法，以及训练和优化为您的数据定制的个性化模型。Amazon Personalize 分析的所有数据都是保密且安全的，仅用于为您提供定制化建议。您可以通过一个简单的 API 调用开启个性化推荐。随用随付，没有最低费用，也无需预付款。

Amazon Personalize 就像是您的独家 Amazon.com 机器学习个性化团队，全天候待命。



## 说明
上载笔记本并按照说明操作

## 许可

该库在 MIT-0 许可下授权。参见“许可”文件。


