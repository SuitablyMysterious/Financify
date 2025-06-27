import importer
import os, datetime

# Use the logger from importer module
logger = importer.logger

logger.info("Logger Initiated")
logger.info("Starting financify")

print("Welcome to financify:")

on = True
loopIteration = 0
logger.debug("Entering main loop")

while on:
    logger.debug(f"Loop iteration {loopIteration} started")
    choice = input("""To enter a category, enter 1;
To enter a transaction, enter 2;
To view all categories, enter 3;
To view all transactions, enter 4;
To exit, enter 5. 
""")
    logger.debug(f"User choice: {choice}")
    if choice == "1":
        name = input("What is the name of the category: ")
        description = input("Enter a description here: ")
        importer.Category(name, description).store()
    elif choice == "2":
        name = input("Enter the name of the transaction: ")
        
        # Date input loop
        while True:
            date_str = input("Enter the date of the transaction (YYYY-MM-DD): ")
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                break  # Exit the date input loop if successful
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                # Continue the date input loop, don't break
        
        # Amount input loop
        while True:
            amount = input("Enter the amount of the transaction: ")
            if not amount.strip():  # Check for empty input
                print("Amount cannot be empty. Please enter a valid number.")
                continue  # Continue the amount input loop
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    raise ValueError("Amount must be positive.")
                break  # Exit the amount input loop if successful
            except ValueError as e:
                if "could not convert" in str(e):
                    logger.error("Invalid amount format")
                    print("Invalid amount format. Please enter a valid number.")
                else:
                    logger.error(f"Error with amount: {e}")
                    print(f"Error with amount: {e}")
                # Continue the amount input loop, don't break
        
        description = str(input("Enter a description for the transaction: "))
        reference = str(input("Enter a reference for the transaction: "))
        
        # Category input loop
        while True:
            category_name = input("Enter the category name for the transaction: ")
            temp_category = importer.Category(category_name, "")
            if not temp_category.does_exist():
                print(f"Category '{category_name}' does not exist. Please create it first.")
                continue  # Continue the category input loop
            break  # Exit the category input loop if successful
        
        category = importer.Category(category_name, "")
        importer.Transaction(name, date, amount_float, description, reference, category).store()
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
            logger.error("No transactions found")
            print("No transactions found.")

    logger.debug(f"Loop iteration {loopIteration} ended")
    loopIteration += 1
    if choice == "5":
        for path in ['data/categories.csv', 'data/transactions.csv']:
            try:
                os.remove(path)
                print(f"Deleted {path}")
            except FileNotFoundError:
                logger.warning(f"File {path} not found, cannot delete.")
                pass
        print("Exiting the program. Goodbye!")
        logger.info("User exited the program")
        on = False
