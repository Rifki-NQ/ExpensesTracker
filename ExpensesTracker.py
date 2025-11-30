import pandas as pd
import os

#read the file
def read():
    try:
        df = pd.read_csv("datas.csv")
        return df
    #create new headers if the file is completely empty
    except:
        df = pd.DataFrame(columns=["month", "year", "salary"])
        df.to_csv("datas.csv", index=False)
        df = pd.read_csv("datas.csv")
        return df

#show the data
def show():
    df = read()
    if df.empty:
        print("Empty data!")
    else:
        print(df)

#main menu
print("Personal expense tracker")
print("1. Input monthly salary")

while True:
    index = input("Input by index: ")
    if index.isdigit():
        index = int(index)
        if index == 1:
            read()
            break
        else:
            print("-- error: invalid index inputted!")
    else:
        print("-- error: use digits for the index!")