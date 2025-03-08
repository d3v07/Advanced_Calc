import sys
import logging
from app.commands import Command, CommandHandler

class MenuCommand(Command):
    def __init__(self, command_handler: CommandHandler):
        self.command_handler = command_handler

    def execute(self):
        commands = list(self.command_handler.commands.keys())
        # Print the menu dynamically based on registered commands
        print("\nMain Menu:")
        for index, command_name in enumerate(commands, start=1):
            print(f"{index}. {command_name.capitalize()}")
        print("Enter the number of the command to execute, or '0' to exit.")

        logging.info("Displaying main menu to user.")  

        try:
            selection = int(input("Selection: "))
            if selection == 0:
                logging.info("User selected to exit the program.")  
                sys.exit("Exiting program.")  
            command_name = commands[selection - 1]  
            logging.info(f"User selected command: {command_name}")  
            self.command_handler.execute_command(command_name)
        except (ValueError, IndexError):
            logging.warning("User made an invalid selection.")  
            print("Invalid selection. Please enter a valid number.")  
        except KeyError:
            logging.error("Attempted to execute a non-existent command.") 
            print("Selected command could not be executed.")  