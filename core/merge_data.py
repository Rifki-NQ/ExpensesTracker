import pandas as pd
from .utils import read
from .utils import salarypath
from .utils import expensespath

df_salary = read(salarypath)
df_expenses = read(expensespath)
#turns all dates to datetime
df_salary["date"] = pd.to_datetime(df_salary["date"], format="%m-%Y")
df_expenses["date"] = pd.to_datetime(df_expenses["date"], format="%d-%m-%Y")

def show_monthly_expenses():
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

    print(monthly_expenses)