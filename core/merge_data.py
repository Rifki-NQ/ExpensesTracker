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

#helper function for getting available quarter of year from salary and expenses
def get_available_quarters(include=""):
    salary_q = read_salary("Q")
    expenses_q = read_expenses("Q")
    if include == "all":
        available_quarters = pd.merge(salary_q, expenses_q, on="date", how="inner")
        available_quarters = available_quarters["date"]
    elif include == "salary":
        available_quarters = salary_q["date"]
    elif include == "expenses":
        available_quarters = expenses_q["date"]
    available_quarters.index = available_quarters.index + 1
    return available_quarters

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
    elif period == "Q":
        df_salary["date"] = df_salary["date"].dt.to_period("Q")
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
    elif period == "Q":
        df_expenses["date"] = df_expenses["date"].dt.to_period("Q")
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
    
def yearly_summary(net_balance=False):
    df_salary = read_salary("Y")
    df_expenses = read_expenses("Y")
    #check datasets availability
    if df_salary is None and df_expenses is None:
        return "Empty salary and expenses data!"
    elif df_salary is None:
        return "Empty salary data!"
    elif df_expenses is None:
        return "Empty expenses data!"
    summary = pd.merge(df_salary, df_expenses, on="date", how="outer")
    summary.rename(columns={"salary": "yearly_salary", "expense": "yearly_expenses"}, inplace=True)
    if net_balance:
        summary["net_balance"] = summary["yearly_salary"] - summary["yearly_expenses"]
    return summary
    
def expenses_weekly_summary():
    df_expenses = read_expenses()
    available_quarters = get_available_quarters(include="expenses")
    print(available_quarters.to_string())
    while True:
        selected_period = input("Select which period to show (by index): ")
        if validate_digit(selected_period, 1, len(available_quarters)):
            selected_period = str(available_quarters.tolist()[int(selected_period) - 1])
            break
    df_expenses["date"] = df_expenses["date"].dt.to_period("Q")
    df_expenses = df_expenses[df_expenses["date"] == selected_period]
    #getting expenses of the selected period
    weekly_expenses = read_expenses()
    weekly_expenses["date"] = weekly_expenses["date"].dt.to_period("W")
    weekly_expenses = weekly_expenses.groupby("date", as_index=False)["expense"].sum()
 
    #add weekly date
    weekly_date = read_expenses()
    weekly_date = weekly_date["date"].rename("weekly_date").dt.to_period("W")
    start_of_week = weekly_date.dt.start_time.dt.strftime("%d %B")
    end_of_week = weekly_date.dt.end_time.dt.strftime("%d %B %Y")
    weekly_date = start_of_week + " to " + end_of_week
    summary = weekly_expenses.join(weekly_date)
    #raname columns and reorder them
    
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