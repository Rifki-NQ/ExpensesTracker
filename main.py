from core.salary import InputSalary
from core.salary import ShowSalary

#main menu
print("Personal expense tracker")
print("1. Input monthly salary")
print("2. Show salary data")

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