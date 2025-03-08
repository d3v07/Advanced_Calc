import logging
from app.commands import Command

class Divide(Command):
    def execute(self):
        logging.info("Executing Divide command.")
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        
        if b == 0:
            logging.warning("Attempted division by zero.")
            print("Cannot divide by zero. Please enter a valid second number.")
        else:
            result = a / b
            print(f"The result is {result}")
            logging.info(f"Division result: {result}")