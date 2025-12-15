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
    expenses_category.rename(columns={"expense": "category expenses"}, inplace=True)
    #create category percentage
    percentage = expenses_category.groupby("category", as_index=False).size()
    percentage["size"] = percentage["size"] / percentage["size"].sum() * 100
    percentage["size"] = percentage["size"].round(1)
    #group by category then add all the values
    expenses_category = expenses_category.groupby("category", as_index=False)["category expenses"].sum()
    expenses_category.insert(1, "category percentage", percentage["size"])
    #add total category column
    total_category = df_expenses.groupby("category", as_index=False).size()
    expenses_category.insert(1, "total category", total_category["size"])
    #sort by highest category percentage then reset the index
    expenses_category = expenses_category.sort_values("category percentage", ascending=False)
    expenses_category["category percentage"] = expenses_category["category percentage"].astype(str) + "%"
    expenses_category.reset_index(drop=True, inplace=True)
    expenses_category.index = expenses_category.index + 1
    return expenses_category