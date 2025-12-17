import pandas as pd
import matplotlib.pyplot as plt
from .utils import read, salarypath, expensespath, validate_digit

def monthly_salary():
    df = read(salarypath)
    df_date = df["date"].copy()
    if df.empty:
        print("Empty salary data!")
        return
    #format date
    df_date = pd.to_datetime(df_date, format="%m-%Y")
    df_date= df_date.dt.strftime("%Y")
    #getting existing year in the date
    df_date = df_date.mask(df_date.duplicated()).dropna()
    #select which year to show
    list_of_year = df_date.tolist()
    for index, year in enumerate(list_of_year):
        print(f"{index + 1}. {year}")
    #validate inputted year
    while True:
        selected_year = input("Select which year to show (by index): ")
        if validate_digit(selected_year, 1, len(list_of_year)):
            selected_year = list_of_year[int(selected_year) - 1]
            break
    #get dataframe of selected year
    df_selected_year = df[["date", "salary"]].copy()
    df_selected_year["date"] = pd.to_datetime(df_selected_year["date"], format="%m-%Y")
    df_selected_year.sort_values("date", inplace=True)
    df_selected_year = df_selected_year[df_selected_year["date"].dt.year == int(selected_year)]
    df_selected_year["date"] = df_selected_year["date"].dt.strftime("%m")
    #turns year and salary into lists
    date_list = df_selected_year["date"].tolist()
    salary_list = df_selected_year["salary"].astype(int).tolist()
    #show monthly salary plot by selected year
    print(f"x = {date_list}")
    print(f"y = {salary_list}")
    plt.plot(date_list, salary_list)
    plt.xlabel(f"Year {selected_year}")
    plt.ylabel("Salary for each month")
    plt.tight_layout()
    plt.show()