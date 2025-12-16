import pandas as pd
from .utils import read
from .utils import salarypath
from .utils import expensespath

df_salary = read(salarypath)
df_expenses = read(expensespath)
#turns all dates to datetime
df_salary["date"] = pd.to_datetime(df_salary["date"], format="%m-%Y")
df_expenses["date"] = pd.to_datetime(df_expenses["date"], format="%d-%m-%Y")

def monthly_expenses():
    if df_expenses.empty:
        return "Empty expenses data!"
    monthly_expenses = df_expenses[["date", "expense"]].copy()
    monthly_expenses["date"] = pd.to_datetime(monthly_expenses["date"], format="%d-%m-%Y")
    monthly_expenses["date"] = monthly_expenses["date"].dt.to_period("M")
    monthly_expenses = monthly_expenses.groupby("date", sort=True,as_index=False)["expense"].sum().sort_values("date")
    #format the date then reset the index
    monthly_expenses["date"] = monthly_expenses["date"].dt.to_timestamp()
    monthly_expenses["date"] = monthly_expenses["date"].dt.strftime("%B %Y")
    monthly_expenses.index = monthly_expenses.index + 1
    return monthly_expenses

def monthly_expenses_and_salary():
    if df_salary.empty:
        return "Empty salary data!"
    elif df_expenses.empty:
        return "Empty expenses data!"
    expenses = monthly_expenses()
    salary = df_salary[["date", "salary"]].copy()
    #format salary date
    salary["date"] = pd.to_datetime(salary["date"], format="%m-%Y")
    salary["date"] = salary["date"].dt.strftime("%B %Y")
    #merge the expenses and salary
    expenses_and_salary = expenses.merge(salary, on="date", how="left")
    expenses_and_salary = expenses_and_salary.fillna(0)
    #add net balance
    expenses_and_salary["net balance"] = expenses_and_salary["salary"] - expenses_and_salary["expense"]
    expenses_and_salary[["expense" ,"salary", "net balance"]] = expenses_and_salary[["expense" ,"salary", "net balance"]].astype("int64")
    expenses_and_salary.index = expenses_and_salary.index + 1
    return expenses_and_salary

def expenses_by_category():
    if df_expenses.empty:
        return "Empty expenses data!"
    expenses_category = df_expenses
    expenses_category = expenses_category.groupby("category", as_index=False).agg(
        total_category=("category", "size"),
        category_expenses=("expense", "sum")
    )
    #creates percentage of category then add it to main dataframe
    category_percentage = df_expenses.groupby("category", as_index=False).size()
    category_percentage["size"] = category_percentage["size"] / category_percentage["size"].sum() * 100
    category_percentage["size"] = category_percentage["size"].round(1)
    expenses_category.insert(2, "category_percentage", category_percentage["size"])
    #sort by highest category percentage then format it
    expenses_category = expenses_category.sort_values("category_percentage", ascending=False)
    expenses_category["category_percentage"] = expenses_category["category_percentage"].astype(str) + "%"
    expenses_category.reset_index(drop=True, inplace=True)
    expenses_category.index = expenses_category.index + 1
    return expenses_category

def yearly_summary():
    if df_salary.empty:
        return "Empty salary data!"
    elif df_expenses.empty:
        return "Empty expenses data!"
    expenses = df_expenses[["date", "expense"]].rename(columns={"date": "year", "expense": "yearly_expenses"}).copy()
    salary = df_salary.rename(columns={"date": "year", "salary": "yearly_salary"}).copy()
    #format date of both datasets
    expenses["year"] = pd.to_datetime(expenses["year"], format="%d-%m-%Y")
    salary["year"] = pd.to_datetime(salary["year"], format="%m-%Y")
    expenses["year"] = expenses["year"].dt.strftime("%Y")
    salary["year"] = salary["year"].dt.strftime("%Y")
    #group by year
    expenses = expenses.groupby("year", as_index=False)["yearly_expenses"].sum()
    salary = salary.groupby("year", as_index=False)["yearly_salary"].sum()
    #merge by year
    summary = pd.merge(expenses, salary, on="year", how="outer")
    summary.index = summary.index + 1
    return summary