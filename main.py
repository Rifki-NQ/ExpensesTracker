from core.salary import InputSalary

#main menu
print("Personal expense tracker")
print("1. Input monthly salary")

while True:
    index = input("Input by index (q for quit): ")
    if index.isdigit():
        index = int(index)
        if index == 1:
            InputSalary()
            break
        else:
            print("-- error: invalid index inputted!")
    elif index.lower() == "q":
        break
    else:
        print("-- error: use digits for the index!")