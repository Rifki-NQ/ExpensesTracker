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