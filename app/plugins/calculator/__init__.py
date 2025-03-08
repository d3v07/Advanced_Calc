import pkgutil
import importlib
import logging
from app.commands import Command

class CalculatorCommand(Command):
    def __init__(self, plugins_package='app.plugins.calculator'):
        self.plugins_package = plugins_package
        self.operations = self.load_operations()

    def load_operations(self):
        operations = {}
        plugin_paths = [self.plugins_package.replace('.', '/')]
        found_plugins = pkgutil.iter_modules(plugin_paths)
        # Sort plugins by name to ensure consistent order
        sorted_plugins = sorted(found_plugins, key=lambda x: x[1])
        for index, (finder, name, ispkg) in enumerate(sorted_plugins, start=1):
            if ispkg:
                continue  # Skip sub-packages
            try:
                plugin_module = importlib.import_module(f"{self.plugins_package}.{name}")
                for attribute_name in dir(plugin_module):
                    attribute = getattr(plugin_module, attribute_name)
                    if issubclass(attribute, Command) and attribute is not Command:
                        # Use numeric keys for operations based on their sorted order
                        operations[str(index)] = attribute()
                logging.info(f"Loaded calculator plugin: {name}")
            except (ImportError, TypeError) as e:
                if str(e) == "issubclass() arg 1 must be a class":
                    continue  # Ignore this specific TypeError
                else:
                    logging.error(f"Error loading calculator plugin {name}: {e}")
                    print(f"Error loading plugin {name}: {e}")  # Retain print for user feedback
                    raise
        return operations

    def execute(self):
        while True:
            print("\nCalculator Operations:")
            for key in sorted(self.operations.keys(), key=int):
                print(f"{key}. {self.operations[key].__class__.__name__}")
            print("0. Back")

            choice = input("Select an operation: ")
            if choice == '0':
                logging.info("User selected to go back from CalculatorCommand.")
                break  # Exit to the main menu

            operation = self.operations.get(choice)
            if operation:
                logging.info(f"Executing calculator operation: {operation.__class__.__name__}")
                operation.execute()
            else:
                logging.warning("Invalid selection in CalculatorCommand.")
                print("Invalid selection. Please try again.")