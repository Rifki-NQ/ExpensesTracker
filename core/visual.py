import matplotlib.pyplot as plt
from .merge_data import monthly_summary

def monthly_salary_visual():
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
    
def monthly_expenses_visual():
    imported_data = monthly_summary()
    if isinstance(imported_data, str):
        print(imported_data)
        return
    expenses_date = imported_data["date"].astype(str).tolist()
    expenses_data = imported_data["expenses"].tolist()
    formmatted_expenses_date = [stripped[5:] for stripped in expenses_date]
    print(formmatted_expenses_date)
    print(expenses_data)
    plt.plot(formmatted_expenses_date, expenses_data)
    plt.xlabel(f"Year {expenses_date[0][:4]}")
    plt.ylabel("Expenses")
    plt.tight_layout()
    plt.show()