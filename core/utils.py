import pandas as pd

#variables for data files path
salarypath = "data/salary.csv"
expensespath = "data/expenses.csv"

#read the file
def read(pathname):
    try:
        df = pd.read_csv(pathname)
        return df
    #create new headers if the file is completely empty
    except:
        #new headers for the file salary
        if pathname == salarypath:
            df = pd.DataFrame(columns=["date", "salary"])
        #new headers for the file expenses
        elif pathname == expensespath:
            df = pd.DataFrame(columns=["date", "expense", "category", "description"])
        else:
            raise FileNotFoundError
        save(df, pathname)
        return df

#show the data
def show(pathname):
    df = read(pathname)
    df.index = df.index + 1
    if df.empty:
        print("Empty data!")
    else:
        return df

#save the file
def save(df, pathname, sort=None):
    #sort the data first (optional)
    if sort is not None:
        df = df.sort_values(sort)
    #save back the data
    df.to_csv(pathname, index=False)

#date sorting based on the format
def sort(df, date, format):
    if format == "DD/MM/YYYY":
        df[date] = pd.to_datetime(df[date], format="%d-%m-%Y")
        df = df.sort_values(date)
        df[date] = df[date].dt.strftime("%d-%m-%Y")
        return df
    elif format == "MM/YYYY":
        df[date] = pd.to_datetime(df[date], format="%m-%Y")
        df = df.sort_values(date)
        df[date] = df[date].dt.strftime("%m-%Y")
        return df

#validation for digit and range of digit
def validate_digit(value, min_value, max_value):
    if value.isdigit() and min_value <= int(value) <= max_value:
        return True
    elif value.isdigit():
        print("-- error: invalid inputted index!")
        return False
    else:
        print("-- error: use digit for the index!")
        return False