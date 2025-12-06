from core.salary import InputSalary
from core.salary import ShowSalary
from core.expenses import InputExpenses
from core.expenses import ShowExpenses

while True:
    #main menu
    print("<. ---------------------------. >")
    print("Personal expense tracker")
    print("1. Salary menu")
    print("2. Expenses menu")
    index = input("Input by index (q for quit): ")
    if index.isdigit():
        index = int(index)
        print("<<. -------------------------. >>")
        #sub menu for salary data
        if index == 1:
            print("Salary data menu")
            print("1. Input salary")
            print("2. Show salary")
            while True:
                index = input("Input by index (q for quit): ")
                if index.isdigit():
                    index = int(index)
                    if index == 1:
                        InputSalary()
                        break
                    elif index == 2:
                        ShowSalary()
                        break
                    else:
                        print("-- error: invalid index inputted!")
                elif index.lower() == "q":
                    break
                else:
                    print("-- error: use digits for the index!")
        #sub menu for expenses data
        elif index == 2:
            print("Expenses data menu")
            print("1. Input expenses")
            print("2. Show expenses")
            while True:
                index = input("Input by index (q for quit): ")
                if index.isdigit():
                    index = int(index)
                    if index == 1:
                        InputExpenses()
                        break
                    elif index == 2:
                        ShowExpenses()
                        break
                    else:
                        print("-- error: invalid index inputted!")
                elif index.lower() == "q":
                    break
                else:
                    print("-- error: use digits for the index!")
        else:
            print("-- error: invalid index inputted!")
    elif index.lower() == "q":
        break
    else:
        print("-- error: use digits for the index!")