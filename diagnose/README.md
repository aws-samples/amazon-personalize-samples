Diagnostic / data visualization tools
===
Please use [diagnose.py](diagnose.py) to probe the dataset for any obvious issues such as missing data or item features.
Some examples about how to use diagnose.py are provided in [example_ml_100k.ipynb](example_ml_100k.ipynb), [example_ml_1m.ipynb](example_ml_1m.ipynb), [example_ml_20m.ipynb](example_ml_20m.ipynb).

We explain some example outputs from the interactions table. The tool also examines users and items tables in similar manners.

Interactions table, original shape=(20000263, 4)
---

First, we check for missing data and duplications in the interactions table. We expect large number of interactions and insignificant (<10%) missing data in all fields. Duplications in all of (USER_ID, ITEM_ID, TIMESTAMP) are dropped by the system.
```
missing rate in fields ['USER_ID', 'ITEM_ID', 'TIMESTAMP'] 0.0
dropna shape (20000263, 4)
duplication rate 0.0
drop_duplicates shape (20000263, 4)
```
We also check for repeated user-item activities throughout user histories. High repeat rates (>50%) usually indicate long user histories and it may be beneficial to consider either retaining only the last interactions (dropping all others) or using hierarchical models (TODO).
```
user item repeat rate 0.0
```

Describe interactions table
---

For every data column, we report a description of the key statistics.
For numerical variables, sufficient diversity/independence is usually a good sign that the variable may be a cause factor that we can utilize in the model, rather than an effect factor that is less informative of our learning tasks.

For categorical columns, such as ITEM_ID, we additionally fit a power-law function on the count distribution of the unique categories.
We plot count thresholds against the number of categories that have values greater than or equal to the thresholds.
A straight line in the log-log plot implies that a relative change in the threshold should result in a proportional relative change in the number of categories above the threshold.

![power-law.png](imgs/power-law.png "Example power-law plot.")

We fit the proportion coefficient, in this case, -2.48, and the root mean square error (rmse) for goodness of fit in the log-log space.
The coefficient must be negative.

   A large-magnitude coefficient (<-2) indicates that the distribution is head-heavy, i.e., activities are skewed towards very few categories.
   In this case, we should pay attention to the coverage of the categories. For example, the ITEM_ID count may be skewed toward a few categories when the existing system has a non-personalized layout and the top few are often clicked due to positional bias.
   Including the positional contexts in the models may diversify the results, leading to better personalization.

   A small-magnitude coefficient (>-0.5) implies a heavy-tail distribution, i.e., the counts are rather uniform.
   A uniform ITEM_ID distribution may still be a good case, because it is not considering the correlation between activities.
   We may expect that through user/item-based recommendation, the past item(s) may narrow down the number of ITEM_IDs to recommend in the future.

All of these corrections through personalization can work up to a limit.
We post warning guidelines to indicate a very general estimate of the limits of modeling capability.
They could be wrong in a specific use case. Please use with caution.

Temporal shift analysis
---

Recommendation happens in a dynamic world where new content is rapidly created and old content outdated.
This creates two challenges: the recommender must frequently be retrained with new information and it must hard-threshold or reweigh old examples with recency_mask.

The following retrain frequency analysis aims to predict the marginal item popularity distribution in each period of time using bootstrap popularity from the same period and popularity from the last period, respectively.
Every data point is the weighted average over all periods at the specified frequency.
When the lagged popularity causes significantly larger loss than the same-period bootstrap, a retraining should happen.
In this plot, the optimal retrain frequency is at least once every month (movielens is a survey dataset so the content is slow-moving).

![retrain-freq.png](imgs/retrain-freq.png "Retrain frequency plot")

Similarly, the following temporal shift analysis aims to predict the marginal item distribution in the next periods of time using rolling history of past X periods.
The analysis computes weighted averages by the activity density but only presents the last 100 points for clarity.
The optimal configuration should be set as the hard threshold of historical data or the half-life of recency-weighting (TODO).
In the example, the optimal history retention is from the last 50 days.
However, the Personalize solutions already have built-in recency_mask and, when in doubts, it is beneficial to retain longer user histories.

![temporal-drift.png](imgs/temporal-drift.png "Example temporal-drift plot.")

The primary loss we consider is Total Variation (TV) loss, though we also include percentage of traffic loss due to out-sample items, which partially explains large TV loss.
For customers with large amounts of TV loss, please consider our [COLD-START recipe](../personalize_temporal_holdout/personalize_coldstart_demo.ipynb).


session time delta describe
---

For users with long histories, it is often useful to group user histories into short sessions, within each of which the users tend to keep similar interests.
We use time-delta to decide the begin-of-session (BoS) signals.
Our research paper [1] shows that these signals significantly improve recommendation quality.
The following plot shows the power-law distribution of the time-deltas between all pairs of adjacent activities.

![time-delta.png](imgs/time-delta.png "Example time-delta plot.")

From the plot, we may read that less than 10% of all time-deltas have more than 1-minute intervals and less than 1% have more than 1-month intervals.
If we set a session threshold at 1-minute, we are left with 10% of BoS signals at the inter-session level.
Combining with USER_ID power-law plot, this indicates that users have an average of 10 sessions throughput their activity histories.

As a side note, the movielens dataset has an rather short session threshold because it is from a movie survey website.
Other types of datasets usually have larger and more spread-out BoS thresholds, where we may additional define multiple session hierarchies (TODO).

#### References
[1] Yifei Ma, Balakrishnan (Murali) Narayanaswamy. Hierarchical Temporal-Contextual Recommenders. NIPS 2018 Workshop on Modeling and Decision-Making in Spatiotemporal Domains. [link](https://openreview.net/forum?id=ByzxsrrkJ4)
