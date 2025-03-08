import logging
from app.commands import Command

class Add(Command):
    def execute(self):
        logging.info("Executing Add command.")
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        result = a + b
        print(f"The result is {result}")
        logging.info(f"Addition result: {result}")