import pandas as pd
from .utils import read
from .utils import salarypath
from .utils import expensespath

df_salary = read(salarypath)
df_expenses = read(expensespath)
#turns all dates to datetime
df_salary["date"] = pd.to_datetime(df_salary["date"], format="%m-%Y")
df_expenses["date"] = pd.to_datetime(df_expenses["date"], format="%d-%m-%Y")


def split_date(df, ):
    print()

def show_monthly_expenses():
    if df_expenses.empty:
        print("Empty expenses data!")
        return
    #process date
    monthly_expenses = pd.DataFrame(columns=["date", "Total expenses"])
    monthly_expenses["date"] = df_expenses["date"].dt.strftime("%B %Y")
    monthly_expenses["date"] = monthly_expenses["date"].mask(monthly_expenses["date"].duplicated())
    monthly_expenses["date"] = pd.to_datetime(monthly_expenses["date"], format="%B %Y")
    #process total expenses
    monthly_expenses["Total expenses"] = df_expenses["expense"]

    print(monthly_expenses)