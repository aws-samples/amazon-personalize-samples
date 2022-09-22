# Amazon Personalize 备忘单

## Amazon Personalize 是否为最佳选择？

Amazon Personalize 是在 AWS 上大规模操作推荐系统的绝佳平台，但不适用于个性化或推荐场景。下表粗略列出了适合与不适合的场景。

|适合场景	|不适合场景	|
|---	|---	|
|向已知用户推荐项目。根据用户的观看历史向用户推荐电影。	|基于显式元数据标志进行推荐。当新用户回答了偏好以期获得推荐指导时。	|
|向已知用户推荐新项目。添加新项目以向现有用户销售的零售网站。	|用户、项目和交互的数据量小（见下表）。	|
|向新用户推荐项目。用户刚刚注册并迅速获得推荐	|大多数都是未识别的用户。没有用户活动历史记录的应用程序。	|
|向新用户推荐新项目。向新用户推荐新项目的零售网站。	|**下一个最佳操作工作负载 –** Personalize 推荐可能的项目，但它并不了解正确的工作流程和顺序。	|

### 最小建议数据量

1. 用户超过 50 个。
2. 项目超过 50 个。
3. 交互超过 1500 次。

如果您的数据集达不到这个建议量，那么使用 Amazon Personalize 还为时过早。


## 按配方的用例

可以解决什么样的用例以及如何解决？

1. **个性化推荐** `User-Personalization`：
    1. 这是 Amazon Personalize 的主要用例，它使用用户-项目交互数据来构建推荐模型（直接针对每个用户），并允许使用 PutEvents 即时添加新用户而无需重新训练。PutEvents 还允许用户查看基于用户最近的行为的推荐，这样您就不会丢失这些附加信息。您还可以输入特定于上下文的组件，例如设备类型或位置，以改善结果。
    2. 您还可以添加项目和用户元数据以更好地丰富模型，或按属性筛选推荐。
    3. 对于视频点播和零售用例，域推荐器“精品甄选”和“精心推荐”可帮助您快速上手和可减少运营开销。
2. **向新用户推荐项目** `User-Personalization`：
    1. 借助 PutEvents 功能，可以将新用户（又名冷用户）添加到您现有的 User-Personalization 解决方案中。每个新用户都从返回流行项目的服务中的一个表示开始。这种表示会因用户的行为而改变。当表示与应用程序内的内容交互并且事件由应用程序发送到 Personalize 时，推荐即会更新，而无需重新训练模型。这样可以提供最新的个性化，而且无需不断进行再训练。
3. **推荐新项目** `User-Personalization`：
    1. 当您的客户有新项目（又名冷项目）需要通过某种形式的个性化展示给他们的用户时，这会非常有用。这样，即使有些项目没有历史先例，也可以根据元数据因素被推荐。
    2. 这也可以用于增量训练和数据集更新，以便更轻松地冷启动新项目。
    3. 最后，这种方法利用了类似 Bandit 的探索能力来帮助您快速确定哪些结果有意义，哪些结果不适合推荐，比盲目推送新内容效果更好。
4. **按相关性重新排序** `Personalized-Ranking`：
    1. 在 User-Personalization 下使用相同的 HRNN 算法，但接受用户和项目集合。然后查看项目的集合，并按照从与用户最相关到最不相关的顺序对它们进行排名。这对于推广预先选择的项目集合并了解为特定用户推广正确的内容非常有用。
5. **相关项目** `Similar-Items`/`SIMS`：
    1. `Similar-Items`：深度学习模型会考虑交互数据和项目元数据，然后基于交互历史和项目的元数据相似性来平衡相关项目推荐。当您的交互数据较少但项目的元数据质量高，或者经常引入冷项目/新项目时，这样做很有用。
    2. `SIMS`：想法其实非常简单，通过项目-项目协同筛选即可实现，但基本上是着眼于人们如何与特定项目进行交互，然后根据交互数据确定全局相似项目的程度。无需考虑项目或用户元数据，也不用针对每个用户进行个性化。当您相关的交互数据很多、冷项目（更改目录）不多和/或缺少项目元数据时很有用。
    3. 对于视频点播和零售用例，域推荐器“因为您观看过 X”、“更像 X”、“经常一起购买”和“观看 X 的客户也观看了”让您能够快速上手，并降低运营开销。
6. **经常一起购买** `Similar-Items`/`SIMS`：
    1. 关键在于做好准备，在 Personalize 中训练模型的正确数据并选择正确的配方。例如，仅针对购买数据训练 SIMS 模型。如果可能，仅针对客户购买了多个项目和/或跨多个类别购买了项目的购买数据进行训练。这将为模型带来所需的行为并创建多样性推荐（这就是您这个用例想要的结果）。
    2. SIMS 还可以与 Personalized-Ranking 相结合，在将 SIMS 中的推荐呈现给用户之前对推荐进行重新排序。这可以提供经常一起购买的物品的个性化顺序。
    3. 域推荐器“经常一起购买”将使您能够快速上手和减少运营开销。
7. **整体最受欢迎** `Popularity-Count`：
    1. 不是机器学习，只是计算最常交互项目的基线。在推荐热门项目或创建离线指标基线时，此配方非常有用。可将创建的离线指标基线与使用其他具有相同数据集的 user-personalization 配方创建的解决方案版本进行比较。
    2. 对于视频点播和零售用例，域推荐器“最受欢迎”、“观看次数最多”和“畅销品”可让您以更少的运营开销快速上手。
8. **用户细分** `Item-Affinity`/`Item-Attribute-Affinity`：
    1. 根据用户对目录中特定项目的亲和力或对项目属性的亲和力创建用户细分。与营销活动完美匹配，您要寻找的目标用户将对您想推广的特定项目或与现有项目相似的项目感兴趣。

## 绝佳特性：

1. [域数据集组](https://docs.aws.amazon.com/personalize/latest/dg/domain-dataset-groups.html)：视频点播和零售用例的推荐器
    1. *域数据集组*是 Amazon Personalize 容器，用于存储特定于域的预配置资源，包括数据集、推荐器和筛选器。如果您有流视频或电子商务应用程序并希望 Amazon Personalize 为您的推荐器找到最佳配置，请使用域数据集组。
2. 上下文推荐
    1. 允许您将推荐范围限定为随交互而变化的状态，而不是特定于用户或项目。想想用户的当前位置、正在使用的设备/频道、一天中的时间、一周中的某天等。
    2. 有关详细示例，请参阅此博客文章：https://aws.amazon.com/blogs/machine-learning/increasing-the-relevance-of-your-amazon-personalize-recommendations-by-leveraging-contextual-information/
3. 交互和元数据筛选
    1. 根据用户的交互历史，或者项目或当前用户的元数据属性筛选推荐。在几乎所有媒体或零售工作负载中都非常方便。例如，排除最近购买或缺货的项目，或根据类别或类型包括/排除推荐项目。
    2. 有关详细信息，请参阅此博客文章：https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/
4. 批量推理
    1. 非常适合将大量推荐导出到缓存文件、电子邮件活动或只是用于一般探索。
5. 根据活动自动扩展
    1. 如果特定活动被超额订阅，该服务将自动扩展以满足您的流量需求。当流量变少时，它也会缩减到您要求的最小容量。
6. 非结构化文本作为项目元数据
    1. 将产品描述、视频情节概要或文章内容添加为项目元数据字段，并让 Personalize 使用自然语言处理（NLP）从您的文本中提取隐藏的特征，以提高推荐的相关性。
7. 添加事件
    1. 允许应用程序根据用户行为的意图变化实时更新 Personalize。这意味着每个后续请求都可以适应该意图而无需再训练。
8. 添加项目/添加用户
    1. 允许应用程序添加/更新单个或小批量的项目或用户，而无需上载整个项目和用户数据集。
    2. 有关详细信息，请参阅下方的常见问题解答。
9. KMS 集成
    1. 所有数据都可以使用客户管理的密钥进行加密，所有数据始终都会被加密。
10. 无信息共享
    1. 所有客户数据都是完全隔离的，不会被用来改进 Amazon 或任何其他方的推荐。
    2. 模型对客户的 AWS 账户而言是私有的。

## 视频系列：

1. Amazon Personalize 简介：https://www.youtube.com/c/amazonwebservices/videos
2. 使用 Amazon Personalize 了解您的数据：https://www.youtube.com/watch?v=TEioktJD1GE
3. 使用 Amazon Personalize 解决实际使用案例：https://www.youtube.com/watch?v=9N7s_dVVWBE
4. 为您的用户提供 Amazon Personalize 推荐：https://www.youtube.com/watch?v=oeVYCOFNFMI
5. 将您的 Amazon Personalize POC 投入生产：https://www.youtube.com/watch?v=3YawVCO6H14

## 常见问题：

1. 我应该多久进行一次再训练？
    1. 再训练频率由业务需求决定。您需要多长时间全面了解一次您的用户及其对项目的行为？ 您需要多久添加一次新项目？ 这些问题的答案决定了您的训练频率。一般来说，大多数客户每周进行一次再训练。有关更详细的指导，请参见下文。
    2. 如果使用“aws-user-personalization”配方，该服务将每 2 小时在后台自动更新解决方案版本（无需额外费用）。此自动更新过程将引入自上次更新以来添加的新项目，以便开始向用户推荐它们（即冷启动项目）。这可与活动中设置的 exploreWeight 参数协调工作，以控制推荐新项目/冷项目与相关项目（探索/利用）的权重。
    3. 如果 2 小时的自动更新频率不足以引入新项目，您可以手动创建一个新的解决方案版本，使用 trainingMode=UPDATE 并更频繁地更新活动（例如，每小时）。这基本上与自动更新相同，只是采用的是客户定义的频率。但是，手动执行此操作需要花费训练时间。
    4. 无论采用自动还是手动更新模式过程，这都不会完全再训练模型。客户仍然需要偶尔创建一个带有 trainingMode=FULL 的新解决方案版本，以便完全再训练模型。偶尔根据所有数据重新计算模型中的权重很重要，但自动更新过程使得完全再训练的必要性降低。所以，每周指南应运而生。因此，先让自动更新运行一整周，然后每周进行一次全面的再训练。
    5. 更准确地确定再训练频率的另一种方法是监控在线指标。当在线指标开始落后（如，模型漂移）时，则需要再训练。
2. 如何添加新用户？
    1. 如果您使用的是 PutEvents API，那么只要您记录他们的第一个操作，就可以添加该新用户。如果您没有使用该 API，那么只要您再训练了包含交互数据集中用户行为的模型，就会将用户添加到系统中。
    2. 即使您的用户为未知（注册前的新匿名用户），您仍然可以冷启动这些用户。如果您可以立即为他们的用户和 sessionID 分配一个新的 UUID，那么您可以继续上面定义的过程来冷启动用户。
    3. 如果该路径不起作用，您仍然可以为 sessionID 生成一个新的 UUID，调用不含 userID 的 PutEvents，然后在为它们生成的有效 userID 之后继续指定相同的 sessionID。当您再训练时，Personalize 将结合历史数据和 PutEvents 数据，并在发现匹配的 sessionid 时结合用户之前的所有匿名交互和非匿名交互。这将允许您在用户获得有效的内部用户 ID 之前指定历史记录。
    4. 您可以使用 PutUsers API 逐个或小批量添加/更新用户。但是，只有在（重新）训练后或使用 PutEvents API 冷启动时，才会收到个性化推荐。
3. 如何添加新项目？
    1. 将项目添加到项目数据集中有两种方法：1/ 通过使用数据集导入作业上载完整数据集，将新项目添加到项目数据集，或 2/ 使用 PutItems API 逐个或小批量添加项目。
    2. 如果也存在交互（所有配方），或者在更新解决方案后（trainingMode = FULL/UPDATE 仅适用于 aws-user-personalization 和 HRNN-Coldstart）冷启动新的项目推荐（无论是否存在互动），则再训练后系统会将新项目添加到推荐中。
    3. 例如，您可以为新版本放置横幅，将新项目有机流式传输到您的历史数据集中。导致用户与新项目交互以及导致相应操作被记录的任何操作都可以在下一次训练后改进推荐。
4. 如何筛选特定条件的结果？
    1. 对交互（https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/ ）或元数据信息（https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/ ）使用筛选器功能。
    2. 基于交互历史的筛选目前仅考虑再训练时数据集中最近的 100 次实时交互（PutEvents API）和最近的 200 次历史交互。所有事件类型都包含在 100/200 限制中。
5. 我需要根据滚动日期值筛选项目，但筛选器不支持区间运算符的动态值。我有哪些选择？
    1. 区间运算符目前不能与动态值一起使用，因此您必须创建具有固定值的筛选器表达式，然后定期轮换筛选器以更新固定值。[筛选器轮换器](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/filter_rotator)解决方案可用于自动化轮换过程。
6. 为什么我应该使用 Amazon Personalize 而不是自定义解决方案？
    1. 假设您的数据和用例是一致的，那么这种方法可以更快地面向最终用户提供最佳模型。在处理大规模运行推荐系统的操作负担的同时，Personalize 还可以让您腾出时间来改进特征工程、数据收集、用户体验或解决其他问题。
7. 我的用例是这样，客户很少购买或与我目录中的项目进行交互（例如购买汽车）。Personalize 仍然是我的最佳选择吗？
    1. 是的，Personalize 仍然可以有效地用于此类用例。例如，可以根据浏览或购买历史（在线和/或离线）等所有的用户活动训练 SIMS 模型，然后将该模型用于项目详情页面上的类似项目推荐。这使您可以利用所有活跃用户的近期活动向回访用户作出相关推荐。
    2. 实时推荐在这里也很有效，因为 Personalize 能够从用户当前的兴趣中学习并快速调整推荐。例如，最初推荐热门项目，然后在使用 PutEvents API 流式传输一些交互后快速进行个性化推荐。
8. 我应该使用 AutoML 吗？
    1. 不，这些配方可以解决不同的用例。请将时间花在为用例选择最合适的配方上并跳过此功能。
9. 我应该使用 HPO 吗？/使用频率是多少？
    1. 不经常。获取一项 HPO 作业的结果，并在解决方案配置中明确使用它们进行多次再训练。然后再次运行 HPO 并重复。实际调整的参数在训练作业之间不应发生太大变化。这种方法将使您的训练时间和成本低于为所有训练作业运行 HPO，且不会牺牲模型的准确性。
10. 如何预测训练价格？
    1. 很遗憾，确实没有一个很好的方法来预先了解这一点。我们已经在 MovieLens 数据集上进行了一些测试。例如，使用 `User-Personalization` 训练 2500 万次交互大约需要 6 个小时，但训练 10 万次交互需要不到 1 个小时。因为训练是在多个主机上分片的，所以实际小时数为：5000 万需 53.9 小时，10 万需 2.135 小时。计费根据实际时间，而不是人工时间。
11. 什么是 TPS 小时，它与定价/可用性有何关系？
    1. Amazon Personalize 提供专用的计算资源，以满足您预期的最低吞吐量需求（每秒事务数，即 TPS），按分配这些资源的小时数计费，即 TPS-小时。1 TPS-小时是在整个小时内每秒提供 1 条推荐所需的计算容量。
    2. 使用量以 5 分钟为增量进行测量，其中平均请求数的最大值和每个增量中的最小预置吞吐量用作 TPS-小时值。因此，当服务扩展至高于最低预置 TPS 时，客户只需按实际消耗的容量计费。在计费期间将所有 5 分钟增量的 TPS-小时相加，以确定计费计算的总 TPS-小时。
    3. 如果您的流量超过活动的最低预置 TPS，该服务将自动纵向扩展。这一特性的价值已受到许多客户的肯定。容量缓冲区分配高于最低预置 TPS，以允许服务在扩展时吸收增加的请求负载。
    4. 如果您的客户将迎来一个活动高峰，例如限时抢购或促销活动，可以让他们使用一些自动化流程来更新预置容量以满足新需求。如果他们不能等待 5-10 分钟让以服务为他们自动扩展，则稍后对流程进行调节。
    5. Amazon Personalize Monitor 项目为 Personalize 活动提供 CloudWatch 控制面板、自定义指标、利用率警报和成本优化功能：https://github.com/aws-samples/amazon-personalize-monitor
12. 如何判断 Personalize 模型是否提供了高质量的推荐？
    1. Personalize 为每个解决方案版本提供离线指标，用于根据交互数据集提供的留出数据衡量模型预测的准确性。使用这些指标来提供一个解决方案版本相对于其他版本的质量导向。
    2. 在线测试（如，A/B 测试）始终是衡量模型对业务指标影响的最佳标准。
    3. 当您将 Personalize 模型与现有推荐系统进行比较时，所有历史数据最初都偏向于现有方法。通常情况下，离线指标不能反映用户在接触其他事物时可能做了什么（他们怎样做，数据并不能反映出这个）。所以这种效果非常值得注意，基于 Bandit 探索的 Personalize 可以更好地从用户那里学习。因此，建议在真正开始测试**之前**，先进行几周的在线测试以便衡量结果。
    4. 有关详细信息，请参阅此博客文章：https://aws.amazon.com/blogs/machine-learning/using-a-b-testing-to-measure-the-efficacy-of-recommendations-generated-by-amazon-personalize/
13. 如何优化成本？
    1. 不要使用 AUTOML！
    2. 不要从 HPO 开始 – 首先请完成构建工作，最后优化。
    3. 仅根据业务需求进行再训练。有关详细信息，请参阅常见问题。
    4. 将最低预置 TPS 设置为低，以便高度依赖自动扩展，除非它对您的吞吐量/延迟目标产生负面影响。
    5. 当用例与电子邮件营销等下游批处理流程保持一致时，请考虑使用批处理推荐。由于批处理推荐针对解决方案版本运行，因此它们不需要活动。
    6. Amazon Personalize Monitor 项目提供了一些成本优化功能，用于优化活动配置以及提醒和删除空闲/放弃的活动：https://github.com/aws-samples/amazon-personalize-monitor
14. 将缓存与 Amazon Personalize 结合使用的最佳方式是什么？ 我应该如何将 Personalize 与现有的应用程序集成？
    1. 查看 [Personalization API](_https://github.com/aws-samples/personalization-apis_) 解决方案：位于您的应用程序和 Amazon Personalize 等推荐系统之间的实时低延迟 API 框架。提供响应缓存、API Gateway 配置、使用 [Amazon CloudWatch Evidently](_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_) 进行 A/B 测试、推理时间项元数据、自动情境性推荐等的最佳实践实施。
15. 将 Personalize 与现有用户体验或其他推荐系统进行比较的最佳方式是什么？
    1. A/B 测试是针对在线指标评估 Personalize 有效性的最常用技术。[Amazon CloudWatch Evidently]([_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html)) 是 AWS 的 A/B 测试工具，可与 Personalize 一起使用。[Personalization API]([_https://github.com/aws-samples/personalization-apis_](https://github.com/aws-samples/personalization-apis)) 项目提供了可部署的解决方案和参考架构。
16. 增量记录对当前用户的推荐有何影响？
    1. Amazon Personalize 允许您以增量方式导入[交互](https://docs.aws.amazon.com/personalize/latest/dg/importing-interactions.html)、[用户](https://docs.aws.amazon.com/personalize/latest/dg/importing-users.html)和[项目](https://docs.aws.amazon.com/personalize/latest/dg/importing-items.html)。这些可能会以不同的方式影响对当前用户的推荐，具体取决于新的解决方案版本是否已经过训练以及使用了何种类型的 trainingMode：

|增量	|配方	|无需再训练	|Retraining trainingMode=UPDATE	|Retraining trainingMode=FULL	|注释	|
|---	|---	|---	|---	|---	|---	|
|putEvent 与新用户	|用户个性化	|个性化在 1 个事件后开始，但在记录每个事件后的 PutEvents 调用后延迟 1-2 秒后约 2-5 个事件后会更加明显。	|除了“无需再训练”中描述的影响之外，没有其他影响 	|个性化推荐	|流式传输的事件越多，记录就越个性化。当新用户记录包含展示数据时，冷启动项目将发生展示折扣。	|
|putEvent 与新用户	|个性化排名	|个性化在 1 个事件后开始，但在记录每个事件后的 PutEvents 调用后延迟 1-2 秒后约 2-5 个事件后会更加明显。	|-	|个性化推荐	|使用个性化排名时，在许多情况下，当客户提供的精选列表被重新排名后，就很难看到 putEvents 记录的直接影响（与 user-personalization 相比，user-personalization 相比中推荐是根据学习的模型行为/元数据特征和用户交互历史从目录中项目的完整词汇生成的。）	|
|putEvent 与新用户	|SIMS	|-	|-	|包含在模型中，用于生成推荐	|SIMS 并没有真正进行个性化，因此在使用 PutEvents 添加新用户的情况下，新用户的事件仅在再训练后才会在类似的项目记录中被考虑。	|
|putUser	|用户个性化	|-	|-	|个性化推荐	|通过 putUser 添加的用户在下一次完全再训练后，将根据该用户已知的交互历史和 userID 的组合成为暖用户。	|
|putUser	|个性化排名	|-	|-	|个性化推荐	|通过 putUser 添加的用户在下一次完全再训练后，将根据该用户已知的交互历史和 userID 的组合成为暖用户。	|
|putUser	|SIMS	|-	|-	|没有效果	|SIMS 并没有真正进行个性化，因此在使用 PutUsers 添加新用户的情况下，新用户的事件仅在再训练后才会在类似的项目记录中被考虑。	|
|putItem	|用户个性化	|-	|启用探索后，根据探索期限截止值显示为符合条件的冷启动项目。	|个性化推荐	|对于新项目/冷启动项目，根据用户的交互历史和新项目/冷启动项的项目元数据进行个性化推荐。冷启动项目（根据启用探索时的探索年龄截止而符合条件的）将包含在下一次更新内。冷启动项目将根据探索过程中产生的交互展示折扣自动更新。此权重与基于元数据的特征相结合，是非线性的，但冷启动项目有些冷门（通过 putEvents 在展示字段中提供，随着时间的推移获得的探索权重将更少）	|
|putItem	|个性化排名	|-	|-	|仅在一些交互后个性化	|-	|
|putItem	|SIMS	|-	|-	|模型中包含新的交互，以基于共现生成相似的项目推荐	|SIMS 并没有真正进行个性化，因此在使用 PutEvents 添加新用户的情况下，新用户的事件仅在再训练后才会在类似的项目记录中被考虑。	|

## 技术支持链接：

1. 整体样本：https://github.com/aws-samples/amazon-personalize-samples
2. 快速入门：https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started
3. POC in a Box 2.0：https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/workshops/POC_in_a_box
4. 基于用例的笔记本：https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/core_use_cases
5. 数据科学工具：https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/data_science
6. MLOps for Personalize：https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops
7. 监控/警报/成本优化：https://github.com/aws-samples/amazon-personalize-monitor

## 演示/研讨会：

* 媒体与娱乐
    * Unicorn Flix
        * 运行实例：[https://unicornflix.amplify-video.com](https://unicornflix.amplify-video.com/)
* 零售
    * Retail Demo Store
        * 来源：https://github.com/aws-samples/retail-demo-store
        * 研讨会：https://github.com/aws-samples/retail-demo-store#hands-on-workshops
        * 运行实例：[http://retaildemostore.jory.cloud/](http://retaildemostore.jory.cloud/#/)

## 技术合作伙伴：

多个技术合作伙伴为 Personalize 提供补充功能，可以加速客户使用 Personalize 进行生产或提高使用 Personalize 实施个性化的投资回报率。

### 客户数据平台 – 事件收集/激活推荐

**Segment** 是一个[客户数据平台](https://en.wikipedia.org/wiki/Customer_data_platform)。他们是 AWS 高级技术合作伙伴，拥有[数字客户体验](https://aws.amazon.com/advertising-marketing/partner-solutions/)（DCX）和[零售](https://aws.amazon.com/retail/partner-solutions/)能力。

Segment 通过以下方式帮助使用 Personalize 的客户：

* 事件收集 – 这是 Segment 的核心能力。客户使用 Segment 在其 Web 应用程序、移动应用程序和其他集成中收集点击流事件。这些事件被收集、验证并散播到客户配置的下游目的地。其中一个目的地为 Amazon Personalize。
* 客户/用户配置文件身份解析 – 因为 Segment 可以查看所有渠道的客户用户的事件，所以能够创建统一的客户配置文件。此配置文件/身份是能够提供全渠道个性化的关键。
* 跨组织的其他营销工具激活 – 因为 Segment 允许客户创建与其他营销工具的连接，将 Personalize 中的个性化推荐附加到 Segment 中的配置文件，因此可让客户和下游合作伙伴在他们的工具中利用这些推荐。

**资源**

* Segment 首席技术官视频：https://www.youtube.com/watch?v=LQSGz8ryvXU
* 博客文章：https://segment.com/blog/introducing-amazon-personalize/
* AWS/Segment 研讨会
    * 实时个性化事件：https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-5-Real-time-events-Segment.ipynb
    * 客户数据平台和 Personalize：https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.1-Segment.ipynb
    * Segment/Personalize（传统研讨会）：https://github.com/james-jory/segment-personalize-workshop
* 文档：https://segment.com/docs/connections/destinations/catalog/amazon-personalize/

**mParticle** 是一个客户数据平台。他们是 AWS 高级技术合作伙伴，拥有[数字客户体验](https://aws.amazon.com/advertising-marketing/partner-solutions/)（DCX）和[零售](https://aws.amazon.com/retail/partner-solutions/)能力。

mParticle 通过以下方式帮助使用 Personalize 的客户：

* 事件收集 – 这是 mParticle 的核心能力。客户使用 mParticle 在 Web 应用程序、移动应用程序和其他集成中收集点击流事件。这些事件被收集、验证并散播到客户配置的下游目的地。
* 客户/用户配置文件身份解析 – 因为 mParticle 可以查看所有渠道的客户用户的事件，所以能够创建统一的客户配置文件。此配置文件/身份是能够提供全渠道个性化的关键。
* 跨组织的其他营销工具激活 – 因为 mParticle 允许客户创建与其他营销工具的连接，将 Personalize 中的个性化推荐附加到 Segment 中的配置文件，因此可让客户和下游合作伙伴在他们的工具中利用这些推荐。

**资源**

* AWS/mParticle 研讨会
    * 实时个性化事件：https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-6-Real-time-events-mParticle.ipynb
    * 客户数据平台和 Personalize：https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.2-mParticle.ipynb

### 分析/测量/实验

**Amplitude** 是 AWS 高级技术合作伙伴，拥有[数字客户体验](https://aws.amazon.com/advertising-marketing/partner-solutions/)（DCX）能力。
Amplitude 通过以下方式帮助使用 Personalize 的客户：

* 产品洞察 – Amplitude 通过复杂的漏斗分析让客户了解带来转化的事件的类型。这为客户提供了优化事件分类并选择正确的事件和元数据字段以在 Personalize 中训练模型所需的洞察力。
* A/B 测试评估 – Amplitude 提供 A/B 测试的在线测量，可以通过 Personalize 支持的个性化客户体验来表示。

**资源**

* 研讨会：https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.5-Amplitude-Performance-Metrics.ipynb
* 博客文章：https://aws.amazon.com/blogs/apn/measuring-the-effectiveness-of-personalization-with-amplitude-and-amazon-personalize/

**Optimizely** 是市场领先的 A/B 测试平台。他们是 AWS 高级技术合作伙伴，拥有[数字客户体验](https://aws.amazon.com/advertising-marketing/partner-solutions/)（DCX）能力。

Optimizely 通过以下方式帮助使用 Personalize 的客户：

* A/B 测试结果 – Optimizely 的核心产品是测量和报告实验，例如个性化技术。
* 功能标记 – 启用/禁用个性化体验

**资源**

* 研讨会：https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.6-Optimizely-AB-Experiment.ipynb

### 消息收发

**Braze** 是市场领先的消息收发平台（电子邮件、推送、SMS）。他们是 AWS 高级技术合作伙伴，拥有[数字客户体验](https://aws.amazon.com/advertising-marketing/partner-solutions/)（DCX）和[零售](https://aws.amazon.com/retail/partner-solutions/)能力。

Braze 通过以下方式帮助使用 Personalize 的客户：

* 借助实时集成或批量集成，通过正确的沟通渠道向客户提供个性化消息。

**资源**

* Braze 文档：https://www.braze.com/docs/partners/data_augmentation/recommendation/amazon_personalize/
* AWS 机器学习博客文章：https://aws.amazon.com/blogs/machine-learning/optimizing-your-engagement-marketing-with-personalized-recommendations-using-amazon-personalize-and-braze/
* AWS 媒体博客文章：https://aws.amazon.com/blogs/media/speed-relevance-insight-how-streaming-services-can-master-effective-content-discovery-and-engagement/
* 研讨会：https://github.com/aws-samples/retail-demo-store/blob/master/workshop/4-Messaging/4.2-Braze.ipynb

### 直接集成

**Magento 2**：Magento 2 扩展由 Magento 和 AWS 的合作伙伴 Customer Paradigm 开发。该扩展不是由 Adobe Magento 开发的。

该扩展可以轻松安装到任何 Magento 2 店面，无论店面是在本地、其他云提供商还是在 AWS 上运行。Amazon Personalize 可始终通过客户的 AWS 账户访问。

**资源**

* 合作伙伴网站：https://www.customerparadigm.com/amazon-personalize-magento/
* Magento Marketplace：https://marketplace.magento.com/customerparadigm-amazon-personalize-extension.html


**Shopify：**[Obviyo](https://www.obviyo.com/)（旧称 HiConversion）已为 Shopify 店面构建了与 Personalize 的托管集成。这意味着 Obviyo 正在其 AWS 环境中管理 Personalize，Shopify 商家向 Obviyo 支付由 Personalize 提供支持的个性化功能。

**资源**

* 合作伙伴网站：https://www.obviyo.com/

**WooCommerce（Beta 版）：**[WP-Engine](https://wpengine.com/) 已将 Personalize 集成到 AWS for WordPress 插件中，只需单击几下即可将 Personalize 中的产品推荐添加到 WooCommerce 站点。

**资源**

* WP-Engine 资源页面：https://wpengine.com/resources/webinar-amazon-com-personalization-for-your-woocommerce-store/
