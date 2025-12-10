import pandas as pd
from .utils import read
from .utils import show
from .utils import save
from .utils import sort
from .utils import validate_digit
from .utils import salarypath

#helper function input date
def input_date(message="Input date of your salary (MM/YYYY): "):
    while True:
        date = input(message)
        if date.isdigit() and len(date) < 7:
            date = f"{date[:2]}-{date[2:]}"
            #try turning inputted date to actual date format
            try:
                date = pd.to_datetime(date, format="%m-%Y")
                return date
            except:
                print("-- error: invalid inputted date! (MM/YYYY)")
        elif date.isdigit():
            print("-- error: inputted date must be 6 long digits! (e.g. 062005)")
        else:
            print("-- error: use digits for the date!")

#helper function input salary
def input_salary(message="Input your salary: "):
    while True:
        salary = input(message)
        if salary.isdigit():
            salary = int(salary)
            return salary
        else:
            print("-- error: Salary must be in digits!")

#input salary
def InputSalary():
    #input all needed data then turns them into variables
    date = input_date()
    salary = input_salary()

    df = read(salarypath)
    #create dataframe of inputted variables
    newdata = pd.DataFrame([{"date": date, "salary": salary}])
    #merge the old data with new one
    df = pd.concat([df, newdata], ignore_index=True)
    #sort the date
    df = sort(df, "date", "MM/YYYY")
    save(df, salarypath)
    print("Your new salary has succefully inputted!")

#show salary
def ShowSalary():
    print(show(salarypath))

#edit salary
def EditSalary():
    df = read(salarypath)
    #check if the file is empty
    if df.empty:
        print("Empty data to edit!")
        return
    ShowSalary()
    #selecting which row of data to be editted
    print("Which do you want to edit?")
    while True:
        rowIndex = input(f"Select by index (1 to {len(df)}): ")
        if validate_digit(rowIndex, 1, len(df)):
            rowIndex = int(rowIndex)
            break
    #selecting which column of data to be editted
    print("1. Date\n2. Salary")
    print("What do you want to edit?")
    while True:
        columnIndex = input("Select by index (1 or 2): ")
        if validate_digit(columnIndex, 1, 2):
            columnIndex = int(columnIndex)
            break
    #edit date
    if columnIndex == 1:
        date = input_date("Input new date of your salary (MM/YYYY): " )
        df.loc[rowIndex - 1, "date"] = date
        df = sort(df, "date", "MM/YYYY")
        save(df, salarypath)
        print("date has been edited successfully!")
    #edit salary
    elif columnIndex == 2:
        salary = input_salary("Input your new salary: ")
        df.loc[rowIndex - 1, "salary"] = salary
        save(df, salarypath)
        print("salary has been edited successfully!")

#delete salary
def DeleteSalary():
    df = read(salarypath)
    print(show(salarypath))
    print("Which do you want to delete?")
    while True:
        rowIndex = input(f"Select by index (1 to {len(df)}): ")
        if validate_digit(rowIndex, 1, len(df)):
            rowIndex = int(rowIndex)
            break
    #delete selected row
    df = df.drop(rowIndex - 1)
    save(df, salarypath)
    print("Deleted successfully!")
