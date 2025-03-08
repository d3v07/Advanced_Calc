import os
import pkgutil
import importlib
from app.commands import CommandHandler, Command
from app.plugins.menu import MenuCommand
import logging

class App:
    def __init__(self):  # Constructor
        os.makedirs('logs', exist_ok=True)  # Ensure the logs directory exists
        self.configure_logging()
        self.command_handler = CommandHandler()

    def configure_logging(self):
        log_file_path = 'logs/app.log'
        logging.basicConfig(filename=log_file_path, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
        logging.info("Logging configured.")

    def load_plugins(self):
        plugins_package = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            logging.info(f"Found plugin: {plugin_name}")  # Log for debugging/record-keeping
            if is_pkg and plugin_name != "menu":  # Ensure it's a package
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    for item_name in dir(plugin_module):
                        item = getattr(plugin_module, item_name)
                        try:
                            if isinstance(item, type) and issubclass(item, Command) and item is not Command:
                                self.command_handler.register_command(plugin_name, item())
                                logging.info(f"Registered command: {plugin_name}")  # Logging
                        except TypeError as e:
                            # Check the exception message to determine if it's the specific TypeError we want to ignore
                            if str(e) == "issubclass() arg 1 must be a class":
                                continue  # Ignore this specific TypeError
                            else:
                                raise  # Move on to the next item without logging this specific error
                except Exception as e:
                    logging.error(f"Error loading plugin {plugin_name}: {e}")  # Logging errors
        # Since menu command would need a separate argument - which is list of all registered commands, we have to manually register it.
        self.command_handler.register_command("menu", MenuCommand(self.command_handler))


    def print_main_menu(self):
        print("\nAvailable commands:")  # Retained for user interaction
        self.command_handler.list_commands()
        print("Type the number of the command to execute, or type 'exit' to exit.")

    def start(self):
        self.load_plugins()
        logging.info("Application starting...")  # Log application start
        self.print_main_menu()
        while True:
            user_input = input(">>> ").strip()
            if user_input.lower() == 'exit':
                logging.info("Exiting application.")  # Log exiting application
                print("Exiting application.")  # User feedback
                break
            try:
                index = int(user_input) - 1
                if index < 0:  # Refresh the main menu if '0' or an invalid negative number is entered
                    self.print_main_menu()
                    continue
                command_name = self.command_handler.get_command_by_index(index)
                if command_name:
                    self.command_handler.execute_command(command_name)
                    self.print_main_menu()  # Print the main menu again after command execution for user
                else:
                    logging.warning("Invalid selection. Please enter a valid number.")  # Logging warning
                    print("Invalid selection. Please enter a valid number.")  # User feedback
            except ValueError:
                logging.error("Only numbers are allowed, wrong input.")  # Logging error
                print("Only numbers are allowed, wrong input.")  # User feedback

if __name__ == "__main__":
    app = App()
    app.start()