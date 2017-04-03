import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

pd.options.mode.chained_assignment = None


################################################################
# Import CSV Data into Pandas DataFrames                       #
################################################################
training_df = pd.read_csv("data/train.csv")
store_df = pd.read_csv("data/store.csv")
test_df = pd.read_csv("data/test.csv")

# print(training_df.info())
# print(store_df.info())
# print(test_df.info())


################################################################
# Process Data                                                 #
################################################################

def is_nan(val):
    return val != val

############################################
# training_df                              #
############################################

# Create "Year" & "Month" columns
training_df["Year"] = training_df["Date"].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d").year)
training_df["Month"] = training_df["Date"].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d").month)

# Create "YearMonth" column
training_df["YearMonth"] = training_df["Date"].apply(lambda x: str(dt.datetime.strptime(x, "%Y-%m-%d").year) + "-" + str(dt.datetime.strptime(x, "%Y-%m-%d").month))

# "StateHoliday" has values "0" & 0
training_df["StateHoliday"].loc[training_df["StateHoliday"] == 0] = "0"

# Create "StateHolidayBinary" column
training_df["StateHolidayBinary"] = training_df["StateHoliday"].map({0: 0, "0": 0, "a": 1, "b": 1, "c": 1})

############################################
# store_df                                 #
############################################

# Add "AvgSales" & "AvgCustomers" columns to store_df
avg_sales_customers = training_df.groupby("Store")[["Sales", "Customers"]].mean()
avg_sales_customers_df = DataFrame({"Store": avg_sales_customers.index, "AvgSales": avg_sales_customers["Sales"], "AvgCustomers": avg_sales_customers["Customers"]}, columns=["Store", "AvgSales", "AvgCustomers"])
store_df = pd.merge(avg_sales_customers_df, store_df, on="Store")

# Fill NaN values in store_df for "CompetitionDistance" with the median value
store_df["CompetitionDistance"].fillna(store_df["CompetitionDistance"].median())


################################################################
# Plot Data                                                    #
################################################################

############################################
# "Open" Data Field                        #
############################################

# Generate plot for No. of Open or Closed Stores (by Day Of Week)
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
sns.countplot(x="Open", hue="DayOfWeek", data=training_df, palette="husl", ax=axis1)
fig.tight_layout()
fig.savefig("plots/No. of Open or Closed Stores (by Day Of Week).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted No. of Open or Closed Stores (by Day Of Week)")


############################################
# "Date" Data Field & Derivatives          #
############################################

# Generate plots for Avg. Sales & Percentage Change (by Year-Month)
average_sales = training_df.groupby("YearMonth")["Sales"].mean()
pct_change_sales = training_df.groupby("YearMonth")["Sales"].sum().pct_change()
fig, (axis1, axis2) = plt.subplots(2, 1, sharex=True, figsize=(15, 16))
ax1 = average_sales.plot(legend=True, ax=axis1, marker="o", title="Average Sales")
ax1.set_xticks(range(len(average_sales)))
ax1.set_xticklabels(average_sales.index.tolist(), rotation=90)
ax2 = pct_change_sales.plot(legend=True, ax=axis2, marker="o", rot=90, colormap="summer", title="Sales Percent Change")
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Percentage Change (by Year-Month).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Percentage Change (by Year-Month)")

# Generate plots for Avg. Sales & Customers (by Year)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="Year", y="Sales", data=training_df, ax=axis1)
sns.barplot(x="Year", y="Customers", data=training_df, ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by Year).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by Year)")

# Generate plots for Avg. Sales & Customers (by Month)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="Month", y="Sales", data=training_df, ax=axis1)
sns.barplot(x="Month", y="Customers", data=training_df, ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by Month).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by Month)")


############################################
# "DayOfWeek" Data Field                   #
############################################

# Generate plots for Avg. Sales & Customers (by Day of Week)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="DayOfWeek", y="Sales", data=training_df, order=[1, 2, 3, 4, 5, 6, 7], ax=axis1)
sns.barplot(x="DayOfWeek", y="Customers", data=training_df, order=[1, 2, 3, 4, 5, 6, 7], ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by Day of Week).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by Day of Week)")


############################################
# "Promo" Data Field                       #
############################################

# Generate plots for Avg. Sales & Customers (by Promo)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="Promo", y="Sales", data=training_df, ax=axis1)
sns.barplot(x="Promo", y="Customers", data=training_df, ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by Promo).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by Promo)")


############################################
# "StateHoliday" Data Field & Derivatives  #
############################################

# Generate plot for No. of State Holidays
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
sns.countplot(x="StateHoliday", data=training_df)
fig.tight_layout()
fig.savefig("plots/No. of State Holidays.png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted No. of State Holidays")

# Generate plots for Avg. Sales & Customers (by State Holiday Binary)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="StateHolidayBinary", y="Sales", data=training_df, ax=axis1)
sns.barplot(x="StateHolidayBinary", y="Customers", data=training_df, ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by State Holiday Binary).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by State Holiday Binary)")

# Generate plots for Avg. Sales & Customers (by State Holiday)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="StateHoliday", y="Sales", data=training_df, ax=axis1)
mask = (training_df["StateHoliday"] != "0") & (training_df["Sales"] > 0)
sns.barplot(x="StateHoliday", y="Sales", data=training_df[mask], ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by State Holiday).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by State Holiday)")


############################################
# "SchoolHoliday" Data Field               #
############################################

# Generate plot for No. of School Holidays
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
sns.countplot(x="SchoolHoliday", data=training_df)
fig.tight_layout()
fig.savefig("plots/No. of School Holidays.png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted No. of School Holidays")

# Generate plots for Avg. Sales & Customers (by School Holiday)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="SchoolHoliday", y="Sales", data=training_df, ax=axis1)
sns.barplot(x="SchoolHoliday", y="Customers", data=training_df, ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by School Holiday).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by School Holiday)")


############################################
# "Sales" Data Field                       #
############################################

# Generate plot for Frequency of Sales Values
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
training_df["Sales"].plot(kind="hist", bins=70, xlim=(0, 20000), ax=axis1)
fig.tight_layout()
fig.savefig("plots/Frequency of Sales Values.png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Frequency of Sales Values")


############################################
# "Customers" Data Field                   #
############################################

# Generate plot for Frequency of Customers Values
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
training_df["Sales"].plot(kind="hist", bins=70, xlim=(0, 9000), ax=axis1)
fig.tight_layout()
fig.savefig("plots/Frequency of Customers Values.png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Frequency of Customers Values")


############################################
# "StoreType" Data Field                   #
############################################

# Generate plot for No. Of Stores (by Store Type)
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
sns.countplot(x="StoreType", data=store_df, order=["a", "b", "c", "d"])
fig.tight_layout()
fig.savefig("plots/No. Of Stores (by Store Type).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted No. Of Stores (by Store Type)")

# Generate plot for Avg. Sales & Customers (by Store Type)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="StoreType", y="AvgSales", data=store_df, order=["a", "b", "c", "d"], ax=axis1)
sns.barplot(x="StoreType", y="AvgCustomers", data=store_df, order=["a", "b", "c", "d"], ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by Store Type).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by Store Type)")


############################################
# "Assortment" Data Field                  #
############################################

# Generate plot for No. Of Stores (by Assortment)
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
sns.countplot(x="Assortment", data=store_df, order=["a", "b", "c"])
fig.tight_layout()
fig.savefig("plots/No. Of Stores (by Assortment).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted No. Of Stores (by Assortment)")

# Generate plot for Avg. Sales & Customers (by Assortment)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="Assortment", y="AvgSales", data=store_df, order=["a", "b", "c"], ax=axis1)
sns.barplot(x="Assortment", y="AvgCustomers", data=store_df, order=["a", "b", "c"], ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by Assortment).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by Assortment)")


############################################
# "Promo2" Data Field                      #
############################################

# Generate plot for No. Of Stores (by Promo2)
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
sns.countplot(x="Promo2", data=store_df)
fig.tight_layout()
fig.savefig("plots/No. Of Stores (by Promo2).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted No. Of Stores (by Promo2)")

# Generate plot for Avg. Sales & Customers (by Promo2)
fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(15, 8))
sns.barplot(x="Promo2", y="AvgSales", data=store_df, ax=axis1)
sns.barplot(x="Promo2", y="AvgCustomers", data=store_df, ax=axis2)
fig.tight_layout()
fig.savefig("plots/Avg. Sales & Customers (by Promo2).png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Avg. Sales & Customers (by Promo2)")


############################################
# "CompetitionDistance" Data Field         #
############################################

# Generate plot for CompetitionDistance vs. Sales
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
store_df.plot(kind="scatter", x="CompetitionDistance", y="AvgSales", ax=axis1)
fig.tight_layout()
fig.savefig("plots/Competition Distance vs. Sales.png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Competition Distance vs. Sales")


############################################
# "CompetitionSince[X]" Data Field         #
############################################

store_id = 6
store_data = training_df[training_df["Store"] == store_id]
average_store_sales = store_data.groupby("YearMonth")["Sales"].mean()

y = store_df["CompetitionOpenSinceYear"].loc[store_df["Store"] == store_id].values[0]
m = store_df["CompetitionOpenSinceMonth"].loc[store_df["Store"] == store_id].values[0]

# Generate plot for Sales for Store <store_id>
fig, (axis1) = plt.subplots(1, 1, figsize=(15, 8))
ax = average_store_sales.plot(legend=True, marker="o", ax=axis1)
ax.set_xticks(range(len(average_store_sales)))
ax.set_xticklabels(average_store_sales.index.tolist(), rotation=90)

# Add vertical line where competition started
if y >= 2013 and y == y and m == m:
    plt.axvline(x=((y - 2013) * 12) + (m - 1), linewidth=3, color="grey")

fig.tight_layout()
fig.savefig("plots/Effect of Competition.png", dpi=fig.dpi)
fig.clf()
plt.close(fig)
print("Plotted Effect of Competition")


############################################
# Correlation                              #
############################################

# One-hot encoding of "DayOfWeek" & "StateHoliday" columns
training_df = pd.get_dummies(training_df, columns=["DayOfWeek", "StateHoliday"])

# Generate Correlation Matrix for training_df
corr = training_df.corr()
fig, (axis1) = plt.subplots(figsize=(15, 15))
sns.heatmap(corr, square=True, ax=axis1)
plt.yticks(rotation=0)
plt.xticks(rotation=90)
fig.tight_layout()
fig.savefig("plots/Correlation Matrix.png")
fig.clf()
plt.close(fig)
print("Plotted Correlation Matrix")