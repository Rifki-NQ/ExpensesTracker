from core.salary import InputSalary
from core.salary import ShowSalary
from core.salary import EditSalary
from core.salary import DeleteSalary
from core.salary import ResetSalary
from core.expenses import InputExpenses
from core.expenses import ShowExpenses
from core.expenses import EditExpenses
from core.expenses import DeleteExpenses
from core.expenses import ResetExpenses
from core.merge_data import monthly_expenses
from core.merge_data import monthly_expenses_and_salary

while True:
    #main menu
    print("<. ---------------------------. >")
    print("Personal expense tracker")
    print("1. Salary menu")
    print("2. Expenses menu")
    print("3. Data menu")
    index = input("Input by index (q for quit): ")
    if index.isdigit():
        index = int(index)
        print("<<. -------------------------. >>")
        #sub menu for salary data
        if index == 1:
            print("Salary data menu")
            print("1. Input salary")
            print("2. Show salary")
            print("3. Edit salary")
            print("4. Delete salary")
            print("5. Reset salary")
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
                    elif index == 3:
                        EditSalary()
                        break
                    elif index == 4:
                        DeleteSalary()
                        break
                    elif index == 5:
                        ResetSalary()
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
            print("1. Input expense")
            print("2. Show expenses")
            print("3. Edit expense")
            print("4. Delete expense")
            print("5. Reset expenses")
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
                    elif index == 3:
                        EditExpenses()
                        break
                    elif index == 4:
                        DeleteExpenses()
                        break
                    elif index == 5:
                        ResetExpenses()
                        break
                    else:
                        print("-- error: invalid index inputted!")
                elif index.lower() == "q":
                    break
                else:
                    print("-- error: use digits for the index!")
        #sub menu for data analyzing
        elif index == 3:
            print("1. Shows expenses by month")
            print("2. Shows expenses for each month of salary")
            while True:
                index = input("Input by index (q for quit): ")
                if index.isdigit():
                    index = int(index)
                    if index == 1:
                        print(monthly_expenses())
                        break
                    elif index == 2:
                        print(monthly_expenses_and_salary())
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