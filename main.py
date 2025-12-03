from core.salary import InputSalary
from core.salary import ShowSalary

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
                    elif index == 2:
                        ShowSalary()
                    else:
                        print("-- error: invalid index inputted!")
                elif index.lower() == "q":
                    break
                else:
                    print("-- error: use digits for the index!")
        #sub menu for expenses data
        elif index == 2:
            print("Expenses data menu")
            while True:
                index = input("Input by index (q for quit): ")
                if index.isdigit():
                    index = int(index)
                    break
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