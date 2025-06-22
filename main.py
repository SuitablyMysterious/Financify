import importer
import os

print("Welcome to financify:")

on = True

while on:
    choice = input("""To enter a category, enter 1;
To enter a transaction, enter 2;
To view all categories, enter 3;
To view all transactions, enter 4;
To exit, enter 5. 
""")

    if choice == "1":
        name = input("What is the name of the category: ")
        description = input("Enter a description here: ")
        importer.Category(name, description).store()
    elif choice == "2":
        date = input("Enter the date of the transaction (YYYY-MM-DD): ")
        amount = input("Enter the amount of the transaction: ")
        description = input("Enter a description for the transaction: ")
        reference = input("Enter a reference for the transaction: ")
        category = input("Enter the category name for the transaction: ")
        importer.Transaction(date, amount, description, reference, category).store()
    elif choice == "3":
        try:
            with open('data/categories.csv', 'r') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("No categories found.")
    elif choice == "4":
        try:
            with open('data/transactions.csv', 'r') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("No transactions found.")
    elif choice == "5":
        for path in ['data/categories.csv', 'data/transactions.csv']:
            try:
                os.remove(path)
                print(f"Deleted {path}")
            except FileNotFoundError:
                pass
        print("Exiting the program. Goodbye!")
        on = False