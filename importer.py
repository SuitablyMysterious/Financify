import datetime
import csv
import os.path

class Category:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def store(self):
        if os.path.isfile('data/categories.csv'):
            with open('data/categories.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.name, self.description])
        else:
            with open('data/categories.csv', 'w', newline='') as file:
                start_row = ['name', 'description']
                writer = csv.writer(file)
                writer.writerow(start_row)
                writer.writerow([self.name, self.description])
    def does_exist(self):
        if os.path.isfile('data/categories.csv'):
            with open('data/categories.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == self.name:
                        return True
        else:
            return False

class Transaction:
    def __init__(self, date:datetime.date, amount:float, description:str, reference:str, categorty:Category):
        self.date = date
        self.amount = amount
        self.description = description
        self.reference = reference
        self.category = categorty

    def store(self):
        if os.path.isfile('data/transactions.csv'):
            with open('data/transactions.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.reference, self.date, self.amount, self.description, self.category.name])
        else:
            with open('data/transactions.csv', 'w', newline='') as file:
                start_row = ['reference', 'date', 'amount', 'description', 'category']
                writer = csv.writer(file)
                writer.writerow(start_row)
                writer.writerow([self.reference, self.date, self.amount, self.description, self.category.name])