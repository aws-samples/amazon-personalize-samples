# Lambda 示例

这个文件夹从一个基本示例开始：通过使用 Lambda 函数处理来自 S3 的新数据，将 `put_events` 集成到您的 Personalize 活动中。

要从这里开始，首先完成 `getting_started` 笔记本收集，包括创建初始事件跟踪器的第二个笔记本。


## 将事件发送到 S3

在这个文件夹中，您会看到一个笔记本 `Sending_Events_to_S3.ipynb`，它包含用于向 S3 存储桶发送一系列消息的样板代码。

这将是使用 Lambda 函数将它们发送到 Personalize 的关键。

## Lambda 函数

现在，该笔记本将可靠地将文件写入 S3 存储桶，下一个任务是构建要在 S3 触发器上调用的 Lambda 函数。Lambda 的代码已在内部提供 `event_processor.py`


首先访问 Lambda 控制台，然后点击 `Create Function`，给它取任何您喜欢的名字，为运行时选择 Python 3.6。

这个 Lambda 函数需要一个新的 IAM 角色，首先接受一个默认角色。稍后会更新该角色，与 Personalize 和 S3 一起使用。下一步 `Create function`


现在点击 `+ Add trigger`，搜索 S3，选择您的存储桶，选择 `All object create events` 用于演示，然后添加后缀 `.json`。最后在本页点击 `Add`

接下来点击 Lamda 函数图标，当出现以下编辑器时，将 `event_processor.py` 的内容复制到编辑器中并保存。替换所有现有内容。

向下滚动编辑器，输入 `trackingId` 作为 `Environment Variables` 的键，并输入第二个笔记本的跟踪 ID。

已经完成的差不多了，最后的配置位是处理 IAM，向下滚动直到您看到 `Execution role`，在底部您会看到一个链接 `View the ....`，右击该链接并在新标签页中打开。

点击 `Attach policies`，添加 `AmazonS3FullAccess` 和 `AmazonPersonalizeFullAccess`，然后点击 `Attach policy`。这些配置在安全性方面并不理想，但可以阐明这一点。对于生产工作负载，创建明确针对您正在使用的资源的定制策略。

连接后，关闭选项卡并重新访问您离开的 Lambda 控制台页面。点击右上角的 `Save`。

回到顶部，选择 `Monitoring`，然后回到模拟事件的笔记本，再次执行该单元格，以编写新文件并执行 Lambda 函数。

几秒钟后，您可以刷新页面，并看到调用成功。
