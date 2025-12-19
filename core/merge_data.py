import pandas as pd
from .utils import read
from .utils import salarypath, expensespath

#helper function for read, sort and format date of salary
def read_salary(date_format=None):
    df_salary = read(salarypath)
    if df_salary.empty:
        return df_salary
    df_salary["date"] = pd.to_datetime(df_salary["date"], format="%m-%Y")
    df_salary.sort_values("date", inplace=True)
    if date_format == "%m-%Y":
        df_salary["date"] = df_salary["date"].dt.strftime("%m-%Y")
        return df_salary
    elif date_format == "%B %Y":
        df_salary["date"] = df_salary["date"].dt.strftime("%B %Y")
        return df_salary
    else:
        return df_salary

def monthly_summary(inlcude="all"):
    df_salary = read_salary(date_format="%B %Y")
    
    
def expenses_by_category():
    df_expenses = read(expensespath)
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
    #add expenses percentage
    expenses_percentage = df_expenses.groupby("category", as_index=False)["expense"].sum()
    expenses_percentage["expenses_percentage"] = expenses_percentage["expense"] / expenses_percentage["expense"].sum() * 100
    expenses_percentage["expenses_percentage"] = expenses_percentage["expenses_percentage"].round(1).astype("str") + "%"
    expenses_category = pd.merge(expenses_category, expenses_percentage, on="category", how="inner")
    expenses_category.drop(columns=["expense"], inplace=True)
    expenses_category.index = expenses_category.index + 1
    return expenses_category

def yearly_summary():
    df_salary = read(salarypath)
    df_expenses = read(expensespath)
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