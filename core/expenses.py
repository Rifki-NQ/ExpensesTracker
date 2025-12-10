import pandas as pd
from .utils import read
from .utils import show
from .utils import save
from .utils import sort
from .utils import validate_digit
from .utils import expensespath

categories = ["Essentials", "F&B", "Transportation", "Personal", "Saving"]

#helper function input date
def input_date():
    while True:
        date = input("Enter date (ddmmyyyy): ")
        if date.isdigit() and len(date) == 8:
            date = f"{date[:2]}-{date[2:4]}-{date[4:]}"
            #try to format the inputted date to actual date (for checking only)
            try:
                checkdate = pd.to_datetime(date, format="%d-%m-%Y")
                return date
            #return error if the inputted date is invalid
            except:
                print("-- error: invalid date inputted!")
        elif date.isdigit():
            print("-- error: Incorrect date inputted! (e.g. 22062005)")
        else:
            print("-- error: use digits for the date!")

#helper function input expense
def input_expense(date):
    while True:
        expense = input(f"Enter expenses as of {date}: ")
        if expense.isdigit():
            return int(expense)
        else:
            print("-- error: use digits for expense!")

#helper function select category
def select_category(message="Select expense category"):
    print(f"{message}")
    #show list of categories with added index
    for index, i in enumerate(categories, start=1):
        print(f"{index}. {i}")
    while True:
        category = input("Select by index: ")
        if category.isdigit() and 1 <= int(category) <= len(categories):
            category = categories[int(category) - 1]
            return category
        elif category.isdigit():
            print("-- error: incorrect index inputted!")
        else:
            print("-- error: use digits for the index!")

#input function descrpition (optional)
def input_description(skipOption=False, message="Description: "):
    while True:
        #skip option for asking y or n
        if not skipOption:
            option = input("Add description? (y/n): ")
        else:
            option = "y"
        if option.lower() == "y":
            #loop in case user input empty description
            while True:
                description = input(f"{message}")
                if not description == "":
                    return description
                print("-- error: description cannot be empty!")
        elif option.lower() == "n":
            return None
        else:
            print("-- error: invalid option inputted! (y = yes, n = no)")

#input new expenses
def InputExpenses():
    #input all needed data then turns them into variables
    date = input_date()
    expense = input_expense(date)
    category = select_category()
    description = input_description()

    #turns inputted values to dataframe
    NewExpense = pd.DataFrame([{"date": date, "expense": expense, "category": category, "description": description}])
    #add old data with new data
    df = read(expensespath)
    df = pd.concat([df, NewExpense], ignore_index=True)
    #sort the date
    df = sort(df, "date", "DD/MM/YYYY")
    #save back to the file
    save(df, expensespath)
    print("New expenses has been successfully inputted!")

#show expenses
def ShowExpenses():
    print(show(expensespath))

#edit expenses
def EditExpenses():
    df = read(expensespath)
    if df.empty:
        print("Empty data to edit!")
        return
    ShowExpenses()
    #selecting which row of data to be editted
    print("Which data do you want to edit?")
    while True:
        index = input(f"Select by index (1 to {len(df)}): ")
        if validate_digit(index, 1, len(df)):
            index = int(index)
            break
    #selecting which column of data to be editted
    print("1. date\n2. expense\n3. category\n4. description")
    while True:
        index2 = input("What do you want to edit (1 to 4): ")
        if validate_digit(index2, 1, 4):
            index2 = int(index2)
            break
    #edit date
    if index2 == 1:
        date = input_date()
        df.loc[index - 1, "date"] = date
        df = sort(df, "date", "DD/MM/YYYY")
        save(df, expensespath)
        print("date has been edited successfully!")
    #edit expenses
    elif index2 == 2:
        expense = input_expense(df.loc[index - 1, "date"])
        df.loc[index - 1, "expense"] = expense
        save(df, expensespath)
        print("expense has been edited successfully!")
    #edit category
    elif index2 == 3:
        category = select_category("Select new category")
        df.loc[index - 1, "category"] = category
        save(df, expensespath)
        print("category has been edited successfully!")
    #edit description
    elif index2 == 4:
        #case if the description is empty
        if pd.isna(df.loc[index - 1, "description"]):
            description = input_description(skipOption=True, message="add description: ")
            df.loc[index - 1, "description"] = description
            save(df, expensespath)
            print("new description has been added successfully!")
        else:
            description = input_description(skipOption=True, message="enter new description: ")
            df.loc[index - 1, "description"] = description
            save(df, expensespath)
            print("description has been edited successfully!")

#delete expense
def DeleteExpenses():
    df = read(expensespath)
    print(show(expensespath))
    print("Which do you want to delete?")
    while True:
        rowIndex = input(f"Select by index (1 to {len(df)}): ")
        if validate_digit(rowIndex, 1, len(df)):
            rowIndex = int(rowIndex)
            break
    #delete selected row
    df = df.drop(rowIndex - 1)
    save(df, expensespath)
    print("Deleted successfully!")