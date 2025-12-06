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
            #try to format the inputted date to actual date (for checking only)
            try:
                actualdate = pd.DataFrame([{"date": date}])
                actualdate["date"] = pd.to_datetime(actualdate["date"], format="%d-%m-%Y")
                break
            #return error if the inputted date is invalid
            except:
                print("-- error: invalid date inputted!")
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

    #select category
    print(f"Select expense category")
    #show list of categories with added index
    for index, i in enumerate(categories, start=1):
        print(f"{index}. {i}")
    while True:
        category = input("Select by index: ")
        if category.isdigit() and 1 <= int(category) <= len(categories):
            category = categories[int(category) - 1]
            break
        elif category.isdigit():
            print("-- error: incorrect index inputted!")
        else:
            print("-- error: use digits for the index!")

    #input descrpition (optional)
    while True:
        option = input("Add description? (y/n): ")
        if option.lower() == "y":
            description = input("Description: ")
            break
        elif option.lower() == "n":
            description = ""
            break
        else:
            print("-- error: invalid option inputted! (y = yes, n = no)")

    #turns inputted values to dataframe
    NewExpense = pd.DataFrame([{"date": date, "expense": expense, "category": category, "description": description}])
    #add old data with new data
    df = read(expensespath)
    df = pd.concat([df, NewExpense], ignore_index=True)
    #format all dates to actual date then sort it
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df = df.sort_values("date")
    df["date"] = df["date"].dt.strftime("%d-%m-%Y")
    #save back to the file
    save(df, expensespath)
    print("New expenses has been successfully inputted!")

#show expenses
def ShowExpenses():
    print(show(expensespath))