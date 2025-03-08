import logging
from app.commands import Command

class GreetCommand(Command):
    def execute(self):
        logging.info("Executing GreetCommand.")  # Log the execution of the GreetCommand
        print("Hello, World!")  # Keep this for user interaction
        logging.info("GreetCommand executed successfully.")  # Optionally log successful execution