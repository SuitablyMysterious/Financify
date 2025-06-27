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

# Use the display functions from importer
def display_menu():
    importer.print_header()
    print("Choose an option:")
    print("1. Enter a category")
    print("2. Enter a transaction") 
    print("3. View all categories")
    print("4. View all transactions")
    print("5. Exit")
    print("-" * 30)

while on:
    display_menu()
    choice = input("Enter your choice: ")
    
    if choice == "1":
        importer.print_header()
        print("CREATE NEW CATEGORY")
        print("-" * 20)
        name = input("Category name: ")
        description = input("Description: ")
        importer.Category(name, description).store()
        input("\nPress Enter to continue...")
        
    elif choice == "2":
        importer.print_header()
        print("CREATE NEW TRANSACTION")
        print("-" * 22)
        
        # Name input loop
        while True:
            name = input("Enter the name of the transaction: ")
            if not name.strip():
                logger.error("Empty transaction name entered")
                print("Transaction name cannot be empty. Please enter a valid name.")
                continue
            if len(name.strip()) < 2:
                logger.error(f"Transaction name too short: {name}")
                print("Transaction name must be at least 2 characters long.")
                continue
            name = name.strip()
            break
        
        # Date input loop
        while True:
            date_str = input("Enter the date of the transaction (YYYY-MM-DD): ")
            if not date_str.strip():
                logger.error("Empty date entered")
                print("Date cannot be empty. Please enter a valid date.")
                continue
            try:
                date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
                # Check if date is not in the future
                if date > datetime.date.today():
                    logger.error(f"Future date entered: {date}")
                    print("Date cannot be in the future. Please enter a valid date.")
                    continue
                # Check if date is not too old (e.g., more than 10 years ago)
                if date < datetime.date.today() - datetime.timedelta(days=3650):
                    logger.error(f"Date too old: {date}")
                    print("Date cannot be more than 10 years ago. Please enter a valid date.")
                    continue
                break
            except ValueError:
                logger.error(f"Invalid date format: {date_str}")
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Amount input loop
        while True:
            amount = input("Enter the amount of the transaction: ")
            if not amount.strip():
                logger.error("Empty amount entered")
                print("Amount cannot be empty. Please enter a valid number.")
                continue
            try:
                amount_float = float(amount.strip())
                if amount_float <= 0:
                    logger.error(f"Non-positive amount entered: {amount_float}")
                    raise ValueError("Amount must be positive.")
                if amount_float > 1000000:  # Reasonable upper limit
                    logger.error(f"Amount too large: {amount_float}")
                    print("Amount seems too large. Please enter a reasonable amount.")
                    continue
                break
            except ValueError as e:
                if "could not convert" in str(e):
                    logger.error(f"Invalid amount format: {amount}")
                    print("Invalid amount format. Please enter a valid number.")
                else:
                    logger.error(f"Error with amount: {e}")
                    print(f"Error with amount: {e}")
        
        # Description input loop
        while True:
            description = input("Enter a description for the transaction: ")
            if not description.strip():
                logger.error("Empty description entered")
                print("Description cannot be empty. Please enter a description.")
                continue
            if len(description.strip()) < 3:
                logger.error(f"Description too short: {description}")
                print("Description must be at least 3 characters long.")
                continue
            description = description.strip()
            break
        
        # Reference input loop
        while True:
            reference = input("Enter a reference for the transaction: ")
            if not reference.strip():
                logger.error("Empty reference entered")
                print("Reference cannot be empty. Please enter a reference.")
                continue
            if len(reference.strip()) < 2:
                logger.error(f"Reference too short: {reference}")
                print("Reference must be at least 2 characters long.")
                continue
            # Check for valid reference format (alphanumeric, dashes, underscores)
            if not reference.replace('-', '').replace('_', '').replace(' ', '').isalnum():
                logger.error(f"Invalid reference format: {reference}")
                print("Reference can only contain letters, numbers, spaces, dashes, and underscores.")
                continue
            reference = reference.strip()
            break
        
        # Category input loop
        while True:
            category_name = input("Enter the category name for the transaction: ")
            if not category_name.strip():
                logger.error("Empty category name entered")
                print("Category name cannot be empty. Please enter a category name.")
                continue
            temp_category = importer.Category(category_name.strip(), "")
            if not temp_category.does_exist():
                logger.error(f"Non-existent category entered: {category_name}")
                print(f"Category '{category_name}' does not exist. Please create it first.")
                continue
            break
        
        category = importer.Category(category_name.strip(), "")
        importer.Transaction(name, date, amount_float, description, reference, category).store()
        logger.info(f"Transaction '{name}' created successfully")
        input("\nPress Enter to continue...")
        
    elif choice == "3":
        importer.print_header()
        print("ALL CATEGORIES")
        print("-" * 20)
        try:
            with open('data/categories.csv', 'r') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("No categories found.")
        input("\nPress Enter to continue...")
        
    elif choice == "4":
        importer.print_header()
        print("ALL TRANSACTIONS")
        print("-" * 22)
        try:
            with open('data/transactions.csv', 'r') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            logger.error("No transactions found")
            print("No transactions found.")
        input("\nPress Enter to continue...")

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
