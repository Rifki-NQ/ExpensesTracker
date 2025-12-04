import pandas as pd
from .filemanager import read
from .filemanager import show
from .filemanager import save
from .filemanager import expensespath

categories = ["Essentials", "F&B", "Transportation", "Personal", "Saving"]

#input new expenses
def InputExpenses():
    #input date
    while True:
        date = input("Enter date (ddmmyyyy): ")
        if date.isdigit() and len(date) == 8:
            date = f"{date[:2]}-{date[2:4]}-{date[4:]}"
            break
        elif date.isdigit():
            print("-- error: Incorrect date inputted! (e.g. 22062005)")
        else:
            print("-- error: use digits for the date!")
    #input expense
    while True:
        expense = input(f"Enter expenses as of {date}: ")
        if expense.isdigit():
            break
        else:
            print("-- error: use digits for expense!")
    #select category of inputted expense
    print(f"Select expense category")
    #show list of categories with added index
    for index, i in enumerate(categories, start=1):
        print(f"{index}. {i}")
    while True:
        category = input("Select by index: ")
        if category.isdigit() and 1 <= int(category) <= len(categories):
            print("success")
            break
        elif category.isdigit():
            print("-- error: incorrect index inputted!")
        else:
            print("-- error: use digits for the index!")