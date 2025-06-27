import importer
import os, datetime

# Configure logging level before starting the application
print("Welcome to financify!")
print("First, let's configure the logging level for this session.\n")

# Set up logging threshold
logging_level = importer.configure_logging_level()

# Use the logger from importer module
logger = importer.logger

logger.info("Logger Initiated")
logger.info("Starting financify")
logger.debug("Importing required modules completed")

print("Welcome to financify:")
logger.debug("Welcome message displayed")

on = True
loopIteration = 0
logger.debug("Entering main loop")
logger.debug(f"Initial loop state - on: {on}, loopIteration: {loopIteration}")

# Use the display functions from importer
def display_menu():
    logger.debug("Displaying main menu")
    importer.print_header()
    menu_options = [
        "Choose an option:",
        "1. Enter a category",
        "2. Enter a transaction", 
        "3. View all categories",
        "4. View all transactions",
        "5. Clear all logs",
        "6. Exit",
        "-" * 30
    ]
    logger.debug(f"Menu options: {menu_options}")
    for option in menu_options:
        print(option)
    logger.debug("Menu displayed successfully")

while on:
    logger.debug(f"Starting loop iteration {loopIteration}")
    display_menu()
    choice = input("Enter your choice: ")
    logger.debug(f"User input received: '{choice}'")
    
    if choice == "1":
        logger.debug("User selected option 1: Enter a category")
        importer.print_header()
        print("CREATE NEW CATEGORY")
        print("-" * 20)
        logger.debug("Category creation header displayed")
        
        name = input("Category name: ")
        logger.debug(f"Category name input: '{name}'")
        description = input("Description: ")
        logger.debug(f"Category description input: '{description}'")
        
        logger.debug("Creating and storing new category")
        category = importer.Category(name, description)
        category.store()
        logger.info(f"Category '{name}' created and stored successfully")
        
        input("\nPress Enter to continue...")
        logger.debug("User pressed Enter to continue")
        
    elif choice == "2":
        logger.debug("User selected option 2: Enter a transaction")
        importer.print_header()
        print("CREATE NEW TRANSACTION")
        print("-" * 22)
        logger.debug("Transaction creation header displayed")
        
        # Name input loop
        logger.debug("Starting transaction name input validation loop")
        while True:
            name = input("Enter the name of the transaction: ")
            logger.debug(f"Transaction name input attempt: '{name}'")
            if not name.strip():
                logger.error("Empty transaction name entered")
                logger.debug("Validation failed: empty name")
                print("Transaction name cannot be empty. Please enter a valid name.")
                continue
            if len(name.strip()) < 2:
                logger.error(f"Transaction name too short: {name}")
                logger.debug(f"Validation failed: name too short (length: {len(name.strip())})")
                print("Transaction name must be at least 2 characters long.")
                continue
            name = name.strip()
            logger.debug(f"Transaction name validated successfully: '{name}'")
            break
        
        # Date input loop
        logger.debug("Starting date input validation loop")
        while True:
            date_str = input("Enter the date of the transaction (YYYY-MM-DD): ")
            logger.debug(f"Date input attempt: '{date_str}'")
            if not date_str.strip():
                logger.error("Empty date entered")
                logger.debug("Validation failed: empty date")
                print("Date cannot be empty. Please enter a valid date.")
                continue
            try:
                logger.debug(f"Attempting to parse date: '{date_str.strip()}'")
                date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
                logger.debug(f"Date parsed successfully: {date}")
                
                today = datetime.date.today()
                logger.debug(f"Today's date: {today}")
                
                # Check if date is not in the future
                if date > today:
                    logger.error(f"Future date entered: {date}")
                    logger.debug(f"Validation failed: date {date} is after today {today}")
                    print("Date cannot be in the future. Please enter a valid date.")
                    continue
                
                # Check if date is not too old (e.g., more than 10 years ago)
                ten_years_ago = today - datetime.timedelta(days=3650)
                logger.debug(f"Ten years ago date: {ten_years_ago}")
                if date < ten_years_ago:
                    logger.error(f"Date too old: {date}")
                    logger.debug(f"Validation failed: date {date} is before {ten_years_ago}")
                    print("Date cannot be more than 10 years ago. Please enter a valid date.")
                    continue
                
                logger.debug(f"Date validated successfully: {date}")
                break
            except ValueError as e:
                logger.error(f"Invalid date format: {date_str}")
                logger.debug(f"Date parsing failed with error: {e}")
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Amount input loop
        logger.debug("Starting amount input validation loop")
        while True:
            amount = input("Enter the amount of the transaction: ")
            logger.debug(f"Amount input attempt: '{amount}'")
            if not amount.strip():
                logger.error("Empty amount entered")
                logger.debug("Validation failed: empty amount")
                print("Amount cannot be empty. Please enter a valid number.")
                continue
            try:
                logger.debug(f"Attempting to parse amount: '{amount.strip()}'")
                amount_float = float(amount.strip())
                logger.debug(f"Amount parsed successfully: {amount_float}")
                
                if amount_float <= 0:
                    logger.error(f"Non-positive amount entered: {amount_float}")
                    logger.debug(f"Validation failed: amount {amount_float} is not positive")
                    raise ValueError("Amount must be positive.")
                
                if amount_float > 1000000:  # Reasonable upper limit
                    logger.error(f"Amount too large: {amount_float}")
                    logger.debug(f"Validation failed: amount {amount_float} exceeds limit of 1000000")
                    print("Amount seems too large. Please enter a reasonable amount.")
                    continue
                
                logger.debug(f"Amount validated successfully: {amount_float}")
                break
            except ValueError as e:
                if "could not convert" in str(e):
                    logger.error(f"Invalid amount format: {amount}")
                    logger.debug(f"Amount parsing failed: could not convert '{amount}' to float")
                    print("Invalid amount format. Please enter a valid number.")
                else:
                    logger.error(f"Error with amount: {e}")
                    logger.debug(f"Amount validation failed with error: {e}")
                    print(f"Error with amount: {e}")
        
        # Description input loop
        logger.debug("Starting description input validation loop")
        while True:
            description = input("Enter a description for the transaction: ")
            logger.debug(f"Description input attempt: '{description}'")
            if not description.strip():
                logger.error("Empty description entered")
                logger.debug("Validation failed: empty description")
                print("Description cannot be empty. Please enter a description.")
                continue
            if len(description.strip()) < 3:
                logger.error(f"Description too short: {description}")
                logger.debug(f"Validation failed: description too short (length: {len(description.strip())})")
                print("Description must be at least 3 characters long.")
                continue
            description = description.strip()
            logger.debug(f"Description validated successfully: '{description}'")
            break
        
        # Reference input loop
        logger.debug("Starting reference input validation loop")
        while True:
            reference = input("Enter a reference for the transaction: ")
            logger.debug(f"Reference input attempt: '{reference}'")
            if not reference.strip():
                logger.error("Empty reference entered")
                logger.debug("Validation failed: empty reference")
                print("Reference cannot be empty. Please enter a reference.")
                continue
            if len(reference.strip()) < 2:
                logger.error(f"Reference too short: {reference}")
                logger.debug(f"Validation failed: reference too short (length: {len(reference.strip())})")
                print("Reference must be at least 2 characters long.")
                continue
            
            # Check for valid reference format (alphanumeric, dashes, underscores)
            cleaned_ref = reference.replace('-', '').replace('_', '').replace(' ', '')
            logger.debug(f"Cleaned reference for validation: '{cleaned_ref}'")
            if not cleaned_ref.isalnum():
                logger.error(f"Invalid reference format: {reference}")
                logger.debug("Validation failed: reference contains invalid characters")
                print("Reference can only contain letters, numbers, spaces, dashes, and underscores.")
                continue
            
            reference = reference.strip()
            logger.debug(f"Reference validated successfully: '{reference}'")
            break
        
        # Category input loop
        logger.debug("Starting category input validation loop")
        while True:
            category_name = input("Enter the category name for the transaction: ")
            logger.debug(f"Category name input attempt: '{category_name}'")
            if not category_name.strip():
                logger.error("Empty category name entered")
                logger.debug("Validation failed: empty category name")
                print("Category name cannot be empty. Please enter a category name.")
                continue
            
            logger.debug(f"Checking if category exists: '{category_name.strip()}'")
            temp_category = importer.Category(category_name.strip(), "")
            category_exists = temp_category.does_exist()
            logger.debug(f"Category existence check result: {category_exists}")
            
            if not category_exists:
                logger.error(f"Non-existent category entered: {category_name}")
                logger.debug("Validation failed: category does not exist")
                print(f"Category '{category_name}' does not exist. Please create it first.")
                continue
            
            logger.debug(f"Category validated successfully: '{category_name.strip()}'")
            break
        
        logger.debug("Creating transaction with validated inputs")
        category = importer.Category(category_name.strip(), "")
        transaction = importer.Transaction(name, date, amount_float, description, reference, category)
        transaction.store()
        logger.info(f"Transaction '{name}' created successfully")
        logger.debug("Transaction creation and storage completed")
        
        input("\nPress Enter to continue...")
        logger.debug("User pressed Enter to continue")
        
    elif choice == "3":
        logger.debug("User selected option 3: View all categories")
        importer.print_header()
        print("ALL CATEGORIES")
        print("-" * 20)
        logger.debug("Categories view header displayed")
        
        try:
            logger.debug("Attempting to read categories.csv")
            with open('data/categories.csv', 'r') as file:
                logger.debug("Successfully opened categories.csv")
                line_count = 0
                for line in file:
                    line_count += 1
                    logger.debug(f"Reading category line {line_count}: {line.strip()}")
                    print(line.strip())
                logger.debug(f"Finished reading {line_count} lines from categories.csv")
        except FileNotFoundError:
            logger.debug("categories.csv not found")
            print("No categories found.")
        except Exception as e:
            logger.error(f"Error reading categories.csv: {e}")
            print(f"Error reading categories: {e}")
        
        input("\nPress Enter to continue...")
        logger.debug("User pressed Enter to continue")
        
    elif choice == "4":
        logger.debug("User selected option 4: View all transactions")
        importer.print_header()
        print("ALL TRANSACTIONS")
        print("-" * 22)
        logger.debug("Transactions view header displayed")
        
        try:
            logger.debug("Attempting to read transactions.csv")
            with open('data/transactions.csv', 'r') as file:
                logger.debug("Successfully opened transactions.csv")
                line_count = 0
                for line in file:
                    line_count += 1
                    logger.debug(f"Reading transaction line {line_count}: {line.strip()}")
                    print(line.strip())
                logger.debug(f"Finished reading {line_count} lines from transactions.csv")
        except FileNotFoundError:
            logger.error("No transactions found")
            logger.debug("transactions.csv not found")
            print("No transactions found.")
        except Exception as e:
            logger.error(f"Error reading transactions.csv: {e}")
            print(f"Error reading transactions: {e}")
        
        input("\nPress Enter to continue...")
        logger.debug("User pressed Enter to continue")

    elif choice == "5":
        logger.debug("User selected option 5: Clear all logs")
        importer.print_header()
        print("CLEAR ALL LOGS")
        print("-" * 20)
        logger.debug("Clear logs header displayed")
        
        confirm = input("Are you sure you want to clear all logs? This cannot be undone. (y/N): ")
        logger.debug(f"User confirmation input: '{confirm}'")
        
        if confirm.lower() in ['y', 'yes']:
            logger.debug("User confirmed log clearing")
            logger.info("User initiated log clearing operation")
            print("Clearing logs...")
            
            if importer.clear_logs():
                print("All logs cleared successfully!")
                logger.info("Logs cleared successfully by user request")
            else:
                print("Failed to clear logs. Please check file permissions.")
                logger.error("Failed to clear logs")
        else:
            logger.debug("User cancelled log clearing")
            print("Log clearing cancelled.")
        
        input("\nPress Enter to continue...")
        logger.debug("User pressed Enter to continue")

    elif choice == "6":
        logger.debug("User selected option 6: Exit")
        logger.debug("Starting cleanup process")
        
        file_paths = ['data/categories.csv', 'data/transactions.csv']
        logger.debug(f"Files to delete: {file_paths}")
        
        for path in file_paths:
            logger.debug(f"Attempting to delete file: {path}")
            try:
                os.remove(path)
                logger.debug(f"Successfully deleted {path}")
                print(f"Deleted {path}")
            except FileNotFoundError:
                logger.warning(f"File {path} not found, cannot delete.")
                logger.debug(f"File {path} was already missing")
            except Exception as e:
                logger.error(f"Error deleting {path}: {e}")
        
        print("Exiting the program. Goodbye!")
        logger.info("User exited the program")
        logger.debug("Setting loop variable to False")
        on = False
    else:
        logger.debug(f"Invalid menu choice entered: '{choice}'")
        logger.warning(f"Invalid menu selection: {choice}")
        print("Invalid choice. Please select a valid option (1-6).")
        input("Press Enter to continue...")
        logger.debug("User pressed Enter after invalid choice")

    if on:  # Only log iteration end if we're continuing
        logger.debug(f"Loop iteration {loopIteration} ended")
        loopIteration += 1
        logger.debug(f"Loop iteration counter incremented to: {loopIteration}")

logger.debug("Main loop exited")
logger.info("Application terminated")
