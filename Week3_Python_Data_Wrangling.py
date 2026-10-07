# Week 3: Python & Data Wrangling - Skill Nexis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

FILE = "Skill_Nexis_Week1_Sales_Performance_Project.xlsx"
df = pd.read_excel(FILE, sheet_name="Cleaned Data")

print("Original shape:", df.shape)
print("\nMissing values before cleaning:")
print(df.isna().sum().sort_values(ascending=False).head(10))

data = df.copy()
duplicate_rows = data.duplicated().sum()
data = data.drop_duplicates()

data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
data["Ship Date"] = pd.to_datetime(data["Ship Date"], errors="coerce")

for col in ["Sales", "Quantity", "Discount", "Profit", "Shipping Cost", "Postal Code"]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

missing_postal = data["Postal Code"].isna().sum()
data["Postal Code"] = data["Postal Code"].fillna(0)

data["Year"] = data["Order Date"].dt.year
data["Sales_Per_Unit"] = data["Sales"] / data["Quantity"].replace(0, np.nan)
data["Profit_Margin_%"] = np.where(data["Sales"] != 0, data["Profit"] / data["Sales"] * 100, 0)
data["Sales_Level"] = np.where(data["Sales"] >= 1000, "High",
                        np.where(data["Sales"] >= 500, "Medium", "Low"))

print("\nDuplicate rows removed:", duplicate_rows)
print("Missing Postal Code values handled:", missing_postal)
print("Rows after cleaning:", len(data))

high_sales = data.loc[data["Sales"] >= 1000,
                      ["Order ID", "Customer Name", "Category", "Sales", "Profit"]]
print("\nFirst 10 high-sales records:")
print(high_sales.sort_values("Sales", ascending=False).head(10))

sales_by_category = data.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
sales_by_year = data.groupby("Year", as_index=False)["Sales"].sum().sort_values("Year")

print("\nSales by Category:")
print(sales_by_category)
print("\nSales by Year:")
print(sales_by_year)

customer_sales = data.groupby("Customer ID", as_index=False).agg(
    Total_Sales=("Sales", "sum"), Order_Count=("Order ID", "nunique")
)
customer_info = data[["Customer ID", "Customer Name", "Segment"]].drop_duplicates("Customer ID")
merged_customers = customer_info.merge(customer_sales, on="Customer ID", how="left")

top_customers = data.groupby("Customer Name", as_index=False).agg(
    Total_Sales=("Sales", "sum"),
    Orders=("Order ID", "nunique"),
    Avg_Order_Value=("Sales", "mean")
).sort_values("Total_Sales", ascending=False).head(10)

print("\nTop 10 Customers:")
print(top_customers)

plt.figure(figsize=(8,5))
plt.bar(sales_by_category["Category"], sales_by_category["Sales"])
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(sales_by_year["Year"], sales_by_year["Sales"], marker="o")
plt.title("Yearly Sales Trend")
plt.xlabel("Year")
plt.ylabel("Sales")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(data=data, x="Category", y="Sales")
plt.title("Sales Distribution by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()
