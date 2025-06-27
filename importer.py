import datetime
import csv
import os.path
import logging
import os
import sys
import time

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('data/financify.log')
            # Removed logging.StreamHandler() - this was printing to console
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 50)
    print("           FINANCIFY")
    print("=" * 50)
    print()

def update_status(message):
    print(f"\r{' ' * 60}", end='')  # Clear line
    print(f"\r{message}", end='', flush=True)

class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def store(self):
        update_status("Checking if categories file exists...")
        time.sleep(0.5)
        
        if os.path.isfile('data/categories.csv'):
            logger.debug("categories.csv exists, appending to it.")
            update_status("Appending to existing categories file...")
            with open('data/categories.csv', 'a', newline='') as file:
                logger.debug("Appending to existing categories.csv file.")
                writer = csv.writer(file)
                writer.writerow([self.name, self.description])
                logger.debug(f"Category {self.name} stored successfully.")
        else:
            update_status("Creating new categories file...")
            with open('data/categories.csv', 'w', newline='') as file:
                logger.debug("categories.csv does not exist, creating a new file.")
                start_row = ['name', 'description']
                writer = csv.writer(file)
                writer.writerow(start_row)
                writer.writerow([self.name, self.description])
                logger.debug(f"Category {self.name} stored successfully.")
        
        update_status(f"Category '{self.name}' saved successfully!")
        time.sleep(1)
        print()  # New line after completion
        
    def does_exist(self):
        update_status("Checking if category exists...")
        time.sleep(0.3)
        
        if os.path.isfile('data/categories.csv'):
            with open('data/categories.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == self.name:
                        update_status(f"Category '{self.name}' found!")
                        time.sleep(0.5)
                        print()
                        return True
        
        update_status(f"Category '{self.name}' not found!")
        time.sleep(0.5)
        print()
        return False

class Transaction:
    def __init__(self, name:str, date:datetime.date, amount:float, description:str, reference:str, category:Category):
        self.name = name
        self.date = date
        self.amount = amount
        self.description = description
        self.reference = reference
        self.category = category
        logger.debug(f"Transaction created: {self.date}, {self.amount}, {self.description}, {self.reference}, {self.category.name}")

    def store(self):
        update_status("Preparing to save transaction...")
        time.sleep(0.5)
        
        if os.path.isfile('data/transactions.csv'):
            logger.debug("transactions.csv exists, appending to it.")
            update_status("Appending to existing transactions file...")
            with open('data/transactions.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.reference, self.date, self.amount, self.description, self.category.name])
        else:
            logger.debug("transactions.csv does not exist, creating a new one.")
            update_status("Creating new transactions file...")
            with open('data/transactions.csv', 'w', newline='') as file:
                start_row = ['reference', 'date', 'amount', 'description', 'category']
                writer = csv.writer(file)
                writer.writerow(start_row)
                writer.writerow([self.reference, self.date, self.amount, self.description, self.category.name])
        
        update_status(f"Transaction '{self.name}' saved successfully!")
        time.sleep(1)
        print()  # New line after completion