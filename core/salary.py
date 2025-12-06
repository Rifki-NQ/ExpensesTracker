import pandas as pd
from .filemanager import read
from .filemanager import show
from .filemanager import save
from .filemanager import salarypath

#input salary
def InputSalary():
    #input date
    while True:
        date = input("Input date of your salary (MM/YYYY): ")
        if date.isdigit() and len(date) < 5:
            break
        elif date.isdigit():
            print("-- error: inputted date must be 6 long digits! (e.g. 062005)")
        else:
            print("-- error: use digits for the date!")
    #input salary
    while True:
        salary = input("- Input your salary: ")
        if salary.isdigit():
            break
        else:
            print("-- error: Salary must be in digits!")
    df = read(salarypath)
    #create dataframe of inputted variables
    newdata = pd.DataFrame([{"date": date, "salary": salary}])
    #merge the old data with new one
    df = pd.concat([df, newdata], ignore_index=True)
    save(df, salarypath, "date")
    print("Your new salary has succefully inputted!")

#Show salary
def ShowSalary():
    print(show(salarypath))