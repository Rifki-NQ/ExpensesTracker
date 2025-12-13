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
        print("Empty expenses data!")
        return
    monthly_expenses = pd.DataFrame(columns=["date", "Total expenses"])
    #add values from expenses data
    monthly_expenses["date"] = df_expenses["date"].dt.strftime("%B %Y")
    monthly_expenses["Total expenses"] = df_expenses["expense"]
    #group by duplicated month then sum the expenses
    monthly_expenses = monthly_expenses.groupby("date", as_index=False)["Total expenses"].sum()
    #sort the date
    monthly_expenses["date"] = pd.to_datetime(monthly_expenses["date"], format="%B %Y")
    monthly_expenses = monthly_expenses.sort_values("date")
    monthly_expenses ["date"]= monthly_expenses["date"].dt.strftime("%B %Y")
    #reset the index
    monthly_expenses.reset_index(drop=True, inplace=True)
    monthly_expenses.index = monthly_expenses.index + 1
    return monthly_expenses

def monthly_expenses_and_salary():
    expenses = monthly_expenses()
    expenses_and_salary = pd.DataFrame(columns=["date", "monthly expenses", "salary", "balance"])
    #copy the values from monthly expenses
    expenses_and_salary[["date", "monthly expenses"]] = expenses[["date", "Total expenses"]]
    #process the salary
    salary = df_salary
    salary["date"] = pd.to_datetime(salary["date"], format="%m-%Y")
    salary["date"] = salary["date"].dt.strftime("%B %Y")
    expenses_and_salary = pd.merge(expenses_and_salary, salary, on="salary", how="inner")
    print(salary)

    return expenses_and_salary
