Amazon Personalize Trending-Now Recipe
---

The sample notebook (trending_now_example.ipynb) will walk you through an example of using Trending Now recipe in [Amazon Personalize](https://aws.amazon.com/personalize)

User interests can change based on a variety of factors, such as external events or the interests of other users. It is critical for websites and apps to tailor their recommendations to these changing interests to improve user engagement. With [Trending-Now](https://docs.aws.amazon.com/personalize/latest/dg/native-recipe-trending-now.html), you can surface items from your catalogue that are rising in popularity faster with higher velocity than other items, such as trending news, popular social content or newly released movies. Amazon Personalize looks for items that are rising in popularity at a faster rate than other catalogue items to help users discover items that are engaging their peers. 

Amazon Personalize also allows customers to define the time periods over which trends are calculated depending on their unique business context, with options for every 30 mins, 1 hour, 3 hours or 1 day, based on the most recent interactions data from users. This notebook will demonstrate how the new recipe aws-trending-now (or aws-vod-trending-now for recommenders) can help recommend the top trending items from the interactions dataset.

## Sample

The [trending_now_example.ipynb](trending_now_example.ipynb)

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.



