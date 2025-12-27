import pandas as pd
import matplotlib.pyplot as plt
from .utils import read, salarypath, expensespath, validate_digit
from .merge_data import monthly_summary

def monthly_salary():
    imported_data = monthly_summary()
    if isinstance(imported_data, str):
        print(imported_data)
        return
    salary_date = imported_data["date"].astype(str).tolist()
    salary_data = imported_data["salary"].tolist()
    formmatted_salary_date = [stripped[5:] for stripped in salary_date]
    print(formmatted_salary_date)
    print(salary_data)
    plt.plot(formmatted_salary_date, salary_data)
    plt.xlabel(f"Year {salary_date[0][:4]}")
    plt.ylabel("Salary")
    plt.tight_layout()
    plt.show()