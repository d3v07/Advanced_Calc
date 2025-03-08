import logging
from app.commands import Command

class GoodbyeCommand(Command):
    def execute(self):
        logging.info("Executing GoodbyeCommand.")  
        print("Goodbye")  
        logging.info("GoodbyeCommand executed successfully.")  