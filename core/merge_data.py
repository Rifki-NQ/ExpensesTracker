import pandas as pd
from .utils import read, validate_digit
from .utils import salarypath, expensespath

#helper function for getting available year of salary and expenses
def get_available_years():
    year_salary = read_salary(period="Y")
    year_expenses = read_expenses(period="Y")
    available_year = pd.merge(year_salary, year_expenses, on="date", how="inner")
    available_year = available_year["date"].rename({"date": "available_year"}).copy()
    available_year.index = available_year.index + 1
    return available_year

#helper function for turning date into period then group it
def read_salary(period=""):
    df_salary = read(salarypath)
    if df_salary.empty:
        return None
    df_salary["date"] = pd.to_datetime(df_salary["date"], format="%m-%Y")
    df_salary.sort_values("date", inplace=True)
    #select period to use
    if period == "M":
        df_salary["date"] = df_salary["date"].dt.to_period("M")
    elif period == "Y":
        df_salary["date"] = df_salary["date"].dt.to_period("Y")
    df_salary = df_salary.groupby("date", as_index=False)["salary"].sum()
    return df_salary

#helper function for turning date into period, group it 
def read_expenses(period=""):
    df_expenses = read(expensespath)
    if df_expenses.empty:
        return None
    df_expenses["date"] = pd.to_datetime(df_expenses["date"], format="%d-%m-%Y")
    df_expenses.sort_values("date", inplace=True)
    #select period to use
    if period == "D":
        df_expenses["date"] = df_expenses["date"].dt.to_period("D")
    elif period == "M":
        df_expenses["date"] = df_expenses["date"].dt.to_period("M")
        df_expenses = df_expenses.groupby("date", as_index=False)["expense"].sum()
    elif period == "Y":
        df_expenses["date"] = df_expenses["date"].dt.to_period("Y")
        df_expenses = df_expenses.groupby("date", as_index=False)["expense"].sum()
    return df_expenses

def monthly_summary(net_balance=False):
    #select which year to summary
    print("Select year to show your monthly summary")
    available_years = get_available_years()
    for index, year in enumerate(available_years.tolist()):
        print(f"{index + 1}. {year}")
    while True:
        index = input("Select by index: ")
        if validate_digit(index, 1, len(available_years)):
            selected_year = int(str(available_years.tolist()[int(index) - 1]))
            break
    df_salary = read_salary(period="M")
    df_expenses = read_expenses(period="M")
    #check datasets availability
    if df_salary is None and df_expenses is None:
        return "Empty salary and expenses data!"
    elif df_salary is None:
        return "Empty salary data!"
    elif df_expenses is None:
        return "Empty expenses data!"
    #filter by selected year
    df_salary = df_salary[df_salary["date"].dt.year == selected_year]
    df_expenses = df_expenses[df_expenses["date"].dt.year == selected_year]
    #columns = date, salary and expenses
    summary = pd.merge(df_salary, df_expenses, on="date", how="left")
    summary.rename(columns={"expense": "expenses"}, inplace=True)
    summary[["salary","expenses"]] = summary[["salary","expenses"]].fillna(0).astype(int)
    #add net balance column (optional)
    if net_balance:
        summary["net_balance"] = summary["salary"] - summary["expenses"]
    return summary
    
    
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