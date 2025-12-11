import pandas as pd

#variables for data files path
salarypath = "data/salary.csv"
expensespath = "data/expenses.csv"
#lists for headers of each data files
salary_headers = ["date", "salary"]
expenses_headers = ["date", "expense", "category", "description"]

#read the file
def read(pathname):
    #check if the file exist
    try:
        df = pd.read_csv(pathname)
    #create new file with headers if the file does not exist
    except FileNotFoundError:
        if pathname == salarypath:
            df = pd.DataFrame(columns=salary_headers)
        elif pathname == expensespath:
            df = pd.DataFrame(columns=expenses_headers)
        save(df, pathname)
        return df
    #check if the headers are valid
    if pathname == salarypath and df.columns.tolist() == salary_headers:
        return df
    elif pathname == expensespath and df.columns.tolist() == expenses_headers:
        return df
    elif pathname == salarypath:
        df = pd.DataFrame(columns=salary_headers)
        save(df, salarypath)
        return df
    elif pathname == expensespath:
        df = pd.DataFrame(columns=expenses_headers)
        save(df, expensespath)
        return df

#show the data
def show(pathname):
    df = read(pathname)
    df.index = df.index + 1
    if df.empty:
        print("Empty data!")
    else:
        print(df)

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