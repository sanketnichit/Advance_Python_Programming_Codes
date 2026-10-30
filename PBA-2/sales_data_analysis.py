import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv("sales.csv")

# Display data
print(df)

# Total and average sales
print("Total Sales:", df["Sales"].sum())
print("Average Sales:", df["Sales"].mean())

# Month with highest sales
monthly = df.groupby("Month", sort=False)["Sales"].sum()
print("Highest Sales Month:", monthly.idxmax())

# Group sales by category
category = df.groupby("Product_Category")["Sales"].sum()
print(category)

# Bar chart
category.plot(kind="bar", title="Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.show()

# Line chart
monthly.plot(kind="line", marker="o", title="Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

# Pie chart
category.plot(kind="pie", autopct="%1.1f%%", title="Category Contribution")
plt.ylabel("")
plt.show()
