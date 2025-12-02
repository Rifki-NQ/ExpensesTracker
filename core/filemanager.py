import pandas as pd

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