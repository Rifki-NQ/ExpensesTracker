import pandas as pd
import os

#read the file
def read(pathname):
    try:
        df = pd.read_csv(pathname)
        return df
    #create new headers if the file is completely empty
    except:
        #new headers for the file salary
        if pathname == "salary.csv":
            df = pd.DataFrame(columns=["date", "salary"])
        #new headers for the file expenses
        elif pathname == "expenses.csv":
            df = pd.DataFrame(columns=["date", "expense", "category", "description"])
        else:
            raise FileNotFoundError
        df.to_csv(pathname, index=False)
        save(df, pathname)
        return df

#show the data
def show(pathname):
    df = read(pathname)
    if df.empty:
        print("Empty data!")
    else:
        print(df)

#save the file
def save(df, pathname, sort=None):
    #sort the data first (optional)
    if sort is not None:
        df.sort_values(sort, inplace=True)
    #save back the data
    df.to_csv(pathname, index=False)

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


#main menu
print("Personal expense tracker")
print("1. Input monthly salary")

while True:
    index = input("Input by index: ")
    if index.isdigit():
        index = int(index)
        if index == 1:
            InputSalary()
            break
        else:
            print("-- error: invalid index inputted!")
    else:
        print("-- error: use digits for the index!")