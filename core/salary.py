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
        if date.isdigit() and len(date) < 7:
            date = f"{date[:2]}-{date[2:]}"
            #try turning inputted date to actual date format
            try:
                date = pd.to_datetime(date, format="%m-%Y")
                break
            except:
                print("-- error: invalid inputted date! (MM/YYYY)")
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
    #turns all dates to actual date then sort it
    df["date"] = pd.to_datetime(df["date"], format="%m-%Y")
    df = df.sort_values("date")
    df["date"] = df["date"].dt.strftime("%m-%Y")
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
    print("Which do you want to edit?")
    while True:
        #selecting which row of data to edit
        index = input(f"Select by index (1 to {len(df)}): ")
        if index.isdigit() and 1 <= int(index) <= len(df):
            print("What do you want to edit?")
            print("1. date\n2. salary")
            #selecting which column of data to edit
            while True:
                index2 = input("Select by index (1 or 2): ")
                #edit the date
                if index2.isdigit() and int(index2) == 1:
                    #validate the inputted date
                    while True:
                        date = input("Input new date of your salary (MM/YYYY): ")
                        if date.isdigit() and len(date) < 7:
                            date = f"{date[:2]}-{date[2:]}"
                            #try turning inputted date to actual date format
                            try:
                                date = pd.to_datetime(date, format="%m-%Y")
                                #change old date to new inputted value
                                
                                print("new date has been edited successfully!")
                                break
                            except:
                                print("-- error: invalid inputted date! (MM/YYYY)")
                        elif date.isdigit():
                            print("-- error: inputted date must be 6 long digits! (e.g. 062005)")
                        else:
                            print("-- error: use digits for the date!")
                    break
                #edit the salary
                elif index2.isdigit() and int(index2) == 2:
                    break
                elif index2.isdigit():
                    print("-- error: invalid inputted index!")
                else:
                    print("-- error: use digit for the index!")
            break
        elif index.isdigit():
            print("-- error: invalid inputted index!")
        else:
            print("-- error: use digit for the index!")