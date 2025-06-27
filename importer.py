import datetime
import csv
import os.path
import logging
import os
import sys
import time

def setup_logging(log_level=logging.DEBUG):
    # Clear any existing handlers to allow reconfiguration
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data/financify.log')
            # Removed logging.StreamHandler() - this was printing to console
        ],
        force=True  # Force reconfiguration
    )
    
    logger = logging.getLogger(__name__)
    logger.debug("Logging configuration completed")
    logger.info(f"Logging level set to: {logging.getLevelName(log_level)}")
    
    return logger

logger = setup_logging()

def configure_logging_level():
    """Allow user to set logging threshold at startup"""
    print("=" * 50)
    print("         LOGGING CONFIGURATION")
    print("=" * 50)
    print("Choose logging level:")
    print("1. DEBUG (Most verbose - logs everything)")
    print("2. INFO (General information)")
    print("3. WARNING (Only warnings and errors)")
    print("4. ERROR (Only errors)")
    print("5. CRITICAL (Only critical errors)")
    print("-" * 30)
    
    level_map = {
        '1': logging.DEBUG,
        '2': logging.INFO,
        '3': logging.WARNING,
        '4': logging.ERROR,
        '5': logging.CRITICAL
    }
    
    level_names = {
        '1': 'DEBUG',
        '2': 'INFO', 
        '3': 'WARNING',
        '4': 'ERROR',
        '5': 'CRITICAL'
    }
    
    while True:
        choice = input("Enter your choice (1-5): ").strip()
        if choice in level_map:
            selected_level = level_map[choice]
            selected_name = level_names[choice]
            print(f"Logging level set to: {selected_name}")
            print("Starting application...\n")
            
            # Reconfigure the logger with new level
            global logger
            logger = setup_logging(selected_level)
            logger.info(f"User selected logging level: {selected_name}")
            return selected_level
        else:
            print("Invalid choice. Please select 1-5.")

def clear_screen():
    logger.debug("Clearing screen")
    os_name = os.name
    logger.debug(f"Operating system detected: {os_name}")
    command = 'cls' if os_name == 'nt' else 'clear'
    logger.debug(f"Executing command: {command}")
    os.system(command)
    logger.debug("Screen cleared successfully")

def print_header():
    logger.debug("Printing application header")
    clear_screen()
    header_text = "=" * 50 + "\n           FINANCIFY\n" + "=" * 50
    logger.debug(f"Header content: {header_text}")
    print("=" * 50)
    print("           FINANCIFY")
    print("=" * 50)
    print()
    logger.debug("Header printed successfully")

def update_status(message):
    logger.debug(f"Updating status with message: {message}")
    print(f"\r{' ' * 60}", end='')  # Clear line
    print(f"\r{message}", end='', flush=True)
    logger.debug("Status updated and displayed")

class Category:
    def __init__(self, name, description):
        logger.debug(f"Creating Category instance with name='{name}', description='{description}'")
        self.name = name
        self.description = description
        logger.debug(f"Category instance created successfully: {self.name}")

    def store(self):
        logger.debug(f"Starting store operation for category: {self.name}")
        update_status("Checking if categories file exists...")
        time.sleep(0.5)
        
        file_path = 'data/categories.csv'
        logger.debug(f"Checking if file exists: {file_path}")
        file_exists = os.path.isfile(file_path)
        logger.debug(f"File exists check result: {file_exists}")
        
        if file_exists:
            logger.debug("categories.csv exists, appending to it.")
            update_status("Appending to existing categories file...")
            try:
                with open('data/categories.csv', 'a', newline='') as file:
                    logger.debug("Opened categories.csv file for appending")
                    writer = csv.writer(file)
                    logger.debug("CSV writer created")
                    row_data = [self.name, self.description]
                    logger.debug(f"Writing row data: {row_data}")
                    writer.writerow(row_data)
                    logger.debug(f"Category {self.name} stored successfully.")
            except Exception as e:
                logger.error(f"Error appending to categories.csv: {e}")
                raise
        else:
            logger.debug("categories.csv does not exist, creating a new file.")
            update_status("Creating new categories file...")
            try:
                with open('data/categories.csv', 'w', newline='') as file:
                    logger.debug("Created new categories.csv file")
                    start_row = ['name', 'description']
                    logger.debug(f"Header row: {start_row}")
                    writer = csv.writer(file)
                    logger.debug("CSV writer created for new file")
                    writer.writerow(start_row)
                    logger.debug("Header row written")
                    row_data = [self.name, self.description]
                    logger.debug(f"Writing category data: {row_data}")
                    writer.writerow(row_data)
                    logger.debug(f"Category {self.name} stored successfully.")
            except Exception as e:
                logger.error(f"Error creating categories.csv: {e}")
                raise
        
        success_message = f"Category '{self.name}' saved successfully!"
        logger.debug(f"Store operation completed successfully: {success_message}")
        update_status(success_message)
        time.sleep(1)
        print()  # New line after completion
        logger.debug("Category store operation finished")
        
    def does_exist(self):
        logger.debug(f"Checking if category exists: {self.name}")
        update_status("Checking if category exists...")
        time.sleep(0.3)
        
        file_path = 'data/categories.csv'
        logger.debug(f"Checking file: {file_path}")
        file_exists = os.path.isfile(file_path)
        logger.debug(f"File exists: {file_exists}")
        
        if file_exists:
            logger.debug("Opening categories.csv to search for category")
            try:
                with open('data/categories.csv', 'r') as file:
                    logger.debug("File opened successfully for reading")
                    reader = csv.reader(file)
                    logger.debug("CSV reader created")
                    row_count = 0
                    for row in reader:
                        row_count += 1
                        logger.debug(f"Reading row {row_count}: {row}")
                        if len(row) > 0 and row[0] == self.name:
                            logger.debug(f"Category '{self.name}' found in row {row_count}")
                            success_message = f"Category '{self.name}' found!"
                            update_status(success_message)
                            time.sleep(0.5)
                            print()
                            logger.debug("Category exists - returning True")
                            return True
                    logger.debug(f"Finished reading {row_count} rows, category not found")
            except Exception as e:
                logger.error(f"Error reading categories.csv: {e}")
                raise
        
        not_found_message = f"Category '{self.name}' not found!"
        logger.debug(not_found_message)
        update_status(not_found_message)
        time.sleep(0.5)
        print()
        logger.debug("Category does not exist - returning False")
        return False

class Transaction:
    def __init__(self, name:str, date:datetime.date, amount:float, description:str, reference:str, category:Category):
        logger.debug(f"Creating Transaction instance with parameters:")
        logger.debug(f"  name: {name}")
        logger.debug(f"  date: {date}")
        logger.debug(f"  amount: {amount}")
        logger.debug(f"  description: {description}")
        logger.debug(f"  reference: {reference}")
        logger.debug(f"  category: {category.name}")
        
        self.name = name
        self.date = date
        self.amount = amount
        self.description = description
        self.reference = reference
        self.category = category
        logger.debug(f"Transaction created: {self.date}, {self.amount}, {self.description}, {self.reference}, {self.category.name}")

    def store(self):
        logger.debug(f"Starting store operation for transaction: {self.name}")
        update_status("Preparing to save transaction...")
        time.sleep(0.5)
        
        file_path = 'data/transactions.csv'
        logger.debug(f"Checking if file exists: {file_path}")
        file_exists = os.path.isfile(file_path)
        logger.debug(f"File exists check result: {file_exists}")
        
        row_data = [self.reference, self.date, self.amount, self.description, self.category.name]
        logger.debug(f"Transaction row data prepared: {row_data}")
        
        if file_exists:
            logger.debug("transactions.csv exists, appending to it.")
            update_status("Appending to existing transactions file...")
            try:
                with open('data/transactions.csv', 'a', newline='') as file:
                    logger.debug("Opened transactions.csv for appending")
                    writer = csv.writer(file)
                    logger.debug("CSV writer created")
                    writer.writerow(row_data)
                    logger.debug("Transaction data written to file")
            except Exception as e:
                logger.error(f"Error appending to transactions.csv: {e}")
                raise
        else:
            logger.debug("transactions.csv does not exist, creating a new one.")
            update_status("Creating new transactions file...")
            try:
                with open('data/transactions.csv', 'w', newline='') as file:
                    logger.debug("Created new transactions.csv file")
                    start_row = ['reference', 'date', 'amount', 'description', 'category']
                    logger.debug(f"Header row: {start_row}")
                    writer = csv.writer(file)
                    logger.debug("CSV writer created for new file")
                    writer.writerow(start_row)
                    logger.debug("Header row written")
                    writer.writerow(row_data)
                    logger.debug("Transaction data written to new file")
            except Exception as e:
                logger.error(f"Error creating transactions.csv: {e}")
                raise
        
        success_message = f"Transaction '{self.name}' saved successfully!"
        logger.debug(f"Store operation completed: {success_message}")
        update_status(success_message)
        time.sleep(1)
        print()  # New line after completion
        logger.debug("Transaction store operation finished")

def clear_logs():
    """Clear all logs from the log file"""
    global logger
    current_level = logger.level
    logger.debug("Starting log clearing operation")
    log_file_path = 'data/financify.log'
    logger.debug(f"Log file path: {log_file_path}")
    
    try:
        # Close current handlers to release file lock
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
        
        # Clear the log file
        with open(log_file_path, 'w') as file:
            file.write('')
        
        # Reinitialize logging with the same level
        logger = setup_logging(current_level)
        logger.info("Log file cleared successfully")
        logger.debug("Logging reinitialized after clearing")
        
        return True
    except Exception as e:
        print(f"Error clearing logs: {e}")
        # Try to reinitialize logging even if clearing failed
        try:
            logger = setup_logging(current_level)
            logger.error(f"Failed to clear logs: {e}")
        except:
            pass
        return False