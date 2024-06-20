# 入门指南

本教程将指导您如何开始使用 Amazon Personalize：

1. 构建一个工作环境（参见下述步骤）
2. 构建您的第一个视频点播和电子商务用例优化推荐
3. 构建您的第一个自定义数据集、模型和推荐活动

## 环境先决条件

仅当您使用 CloudFormation 模板部署时适用，否则请咨询特定任务所需的 IAM 权限。

1. AWS 账户
2. 拥有 AWS 账户管理员权限的用户

## 构建您的环境

第一步是部署一个 CloudFormation 模板，它将为您执行大部分初始设置。在另一个浏览器窗口登录您的 AWS 账户。完成之后，在新标签页中打开下面的链接，开始通过 CloudFormation 部署所需项目。

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=PersonalizeDemo&templateURL=https://amazon-personalize-github-samples.s3.amazonaws.com/PersonalizeDemo.yaml)

如果您对这些步骤有任何问题，请按照截图进行操作。

<details>
  <summary>点击展开说明</summary>
  
### 要开启 CloudFormation Wizard，

请点击底部的 `Next`（下一步），如图所示：![StackWizard](static/imgs/img1.png)

在下一个页面中，您需要提供一个唯一的 S3 存储桶名称，用于您的文件存储，推荐将您的姓和名添加到默认选项的末尾，如下所示，更新之后再次点击 `Next`（下一步）。![StackWizard2](static/imgs/img3.png)

这个页面有点长，所以滚动到底部，点击 `Next`（下一步）。![StackWizard3](static/imgs/img4.png)

再次滚动到底部，选中复选框，允许模板创建新的 IAM 资源，然后点击 `Create Stack`（创建堆栈）。![StackWizard4](static/imgs/img5.png)

几分钟后，CloudFormation 会以您的名义创建上述资源，在进行预置时，页面如下所示：![StackWizard5](static/imgs/img6.png)

完成后，您会看到下面的绿色文本，表明这项工作已经完成：![StackWizard5](static/imgs/img7.png)

现在您已经创建了环境，您需要保存 S3 存储桶的名称以备将来使用，您可以点击 `Outputs`（输出）选项卡，然后查找资源`S3Bucket`，找到后，暂时复制并粘贴到一个文本文件。


</details>


## 利用笔记本

首先导航到 Amazon SageMaker 登录[页面](https://console.aws.amazon.com/sagemaker/home)。从服务页面点击最左边菜单栏上的 `Notebook Instances` 链接。

![StackWizard5](static/imgs/img10.png)

如需前往 Jupyter 界面，只需点击笔记本实例旁最右边的 `Open JupyterLab`。

![StackWizard5](static/imgs/img11.png)

点击打开的链接后，需要几秒钟时间将您重定向到 Jupyter 系统，但进入该系统后，您应该会看到左手边有一个文件集合。

若要开始使用[域数据集组和用例优化推荐器](https://docs.aws.amazon.com/personalize/latest/dg/create-domain-dataset-group.html)

`amazon-personalize-samples/getting_started/notebooks/Building_Your_First_Recommender_Video_On_Demand.ipynb`

`amazon-personalize-samples/getting_started/notebooks/Building_Your_First_Recommender_Ecommerce.ipynb`

或使用[自定义数据集组](https://docs.aws.amazon.com/personalize/latest/dg/custom-dataset-groups.html)导航至第一个笔记本：

`amazon-personalize-samples/getting_started/notebooks/1.Building_Your_First_Campaign.ipynb`

实验的其余部分将通过 Jupyter 笔记本进行，只需在执行前读取每个块并进入下一个块。如果您有任何关于如何使用笔记本的问题，请询问您的导师，或者如果您独立操作，这里有一个很好的入门视频：

https://www.youtube.com/watch?v=Gzun8PpyBCo

## 笔记本工作完成后

完成了笔记本上的所有工作以及清理步骤后，最后要做的就是删除您用 CloudFormation 创建的堆栈。为此，在 AWS 控制台中再次点击顶部 `Services` 链接，这次进入 `CloudFormation` 并点击链接。

![StackWizard5](static/imgs/img9.png)

点击您创建的演示堆栈上的 `Delete` 按钮：

![StackWizard5](static/imgs/img13.png)

最后点击弹出窗口中的 `Delete Stack` 按钮：

![StackWizard5](static/imgs/img14.png)

现在您会注意到正在删除堆栈。看到 `Delete Completed`，即说明所有的东西已经全部删除，并且您已经 100% 完成了这个实验。


