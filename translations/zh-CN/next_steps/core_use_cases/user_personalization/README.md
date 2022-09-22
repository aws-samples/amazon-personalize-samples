Amazon Personalize 用户个性化
---

aws-user-personalization 配方将基于 HRNN 的关联算法与自动探索新项目/冷项目推荐相结合，为构建用户个性化用例提供了最大的灵活性。虽然“交互”数据集是唯一需要的数据集，但若有提供，该配方会利用所有三种数据集类型（交互、项目、用户）。此外，该配方还可以根据交互数据集提供的展示数据，在使用事件跟踪器实时事件流时进行建模。

虽然我们为后来人提供了 HRNN-* 配方的示例笔记本，但还是建议您从 user-personalization 配方开始。
## 示例

### User-Personalization 

[user-personalization-with-exploration.ipynb](user-personalization-with-exploration.ipynb) 演示了如何使用交互和项目数据集来创建解决方案和活动，以平衡基于相关性（利用）和探索推荐新项目/冷项目。也可以使用用户数据集，但本示例中并不涉及。这个示例还演示了如何将展示数据添加到交互数据集和 PutEvents API 调用中。

### 上下文推荐 + 事件跟踪器

在本例中，我们将讨论如何利用元数据和上下文，以用户位置作为用户元数据，根据多个客舱类型的历史评级为用户推荐最佳航空公司

[user-personalization-with-contextual-recommendations.ipynb](user-personalization-with-contextual-recommendations.ipynb) 展示了如何将这些有用的信息上载到我们的系统以帮助提供推荐。需要注意的是，元数据配方的改进取决于可以从提供的元数据中提取多少信息。


*请注意，User-Personalization 配方的项目冷启动功能比传统的 HRNN-Coldstart 配方更受欢迎。因此，推荐您在冷启动项目场景中使用 User-Personalization 配方。*

## 许可汇总

这个示例代码在修改后的 MIT 许可下可用。参见“许可”文件。
