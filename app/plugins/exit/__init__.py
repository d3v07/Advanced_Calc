import sys
import logging
from app.commands import Command

class ExitCommand(Command):
    def execute(self):
        logging.info("Executing ExitCommand - Application exiting...")  
        print("Exiting...") 
        sys.exit(0)  