"""
Private Score: 0.11904, Public Score: 0.10527
"""

import pandas as pd

"""
This model simply ensembles two xgboost models by taking the weighted average.
"""

xgboostregressor6_df = pd.read_csv("predictions/xgboostregressor6.csv")
xgboostregressorlog_df = pd.read_csv("predictions/xgboostregressor-log.csv")

sales_xgboostregressor6 = xgboostregressor6_df["Sales"]
sales_xgboostregressorlog = xgboostregressorlog_df["Sales"]

sales = (sales_xgboostregressor6 * 0.5 + sales_xgboostregressorlog * 0.5) * 0.970

result = pd.DataFrame({"Id": xgboostregressorlog_df["Id"], "Sales": sales})

result.to_csv("predictions/xgboostensemble2.csv", index=False)