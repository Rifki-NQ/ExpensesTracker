import pandas as pd
from filemanager import read
from filemanager import show
from filemanager import save

#input salary
def InputSalary():
    #input year
    while True:
        year = input("- Year of your salary (e.g. 2024): ")
        #check validity of inputted year
        if year.isdigit():
            #check length of year, must be 4 long digits
            if len(year) == 4:
                break
            else:
                print("-- error: invalid year inputted!")
        else:
            print("-- error: use digits for the year!")
    #input month
    while True:
        month = input("- Month of your salary (1 - 12): ")
        #check validity of inputted month
        if month.isdigit():
            #inputted month must two digits long and in range of 1 to 12
            if len(month) == 2 and int(month) > 0 and int(month) < 13:
                break
            else:
                print("-- error: invalid month inputted!")
        else:
            print("-- error: Use digits for the month! (1 to 12)")
    #formats the inputted date
    date = f"{year}-{month}"
    #input salary
    while True:
        salary = input("- Input your salary: ")
        if salary.isdigit():
            break
        else:
            print("-- error: Salary must be in digits!")
    df = read("salary.csv")
    #create dataframe of inputted variables
    newdata = pd.DataFrame([{"date": date, "salary": salary}])
    #merge the old data with new one
    df = pd.concat([df, newdata], ignore_index=False)
    save(df, "salary.csv", "date")
    print("Your new salary has succefully inputted!")