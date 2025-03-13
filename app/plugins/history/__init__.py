import logging
from app.commands import Command, CommandHistoryManager

class HistoryCommand(Command):
    def __init__(self):
        self.history_manager = CommandHistoryManager()
        self.operations = {
            "1": ("Load History", self.load_history),
            "2": ("Save History", self.save_history),
            "3": ("Clear History", self.clear_history),
            "4": ("Delete History Record", self.delete_history_record)
        }

    def execute(self):
        while True:
            print("\nCommand History Operations:")
            for key, (name, _) in self.operations.items():
                print(f"{key}. {name}")
            print("5. Back")

            choice = input("Select an operation: ")
            if choice == '5':
                logging.info("User selected to go back from HistoryCommand.")
                break  # Exit to the main menu

            operation = self.operations.get(choice)
            if operation:
                _, operation_func = operation
                logging.info(f"Executing history operation: {operation[0]}")
                operation_func()
            else:
                logging.warning("Invalid selection in HistoryCommand.")
                print("Invalid selection. Please try again.")

    def load_history(self):
        history = self.history_manager.get_history()
        if history:
            print("Command History:")
            for index, command_name in enumerate(history, start=1):
                print(f"{index}. {command_name}")
        else:
            print("No history found.")

    def save_history(self):
        self.history_manager.save_history()
        print("History saved successfully.")

    def clear_history(self):
        self.history_manager.clear_history()
        print("History cleared successfully.")

    def delete_history_record(self):
        history = self.history_manager.get_history()
        if history:
            for index, command_name in enumerate(history, start=1):
                print(f"{index}. {command_name}")
            try:
                choice = int(input("Select a record to delete: "))
                # Adjust for zero-based index
                del_index = choice - 1
                if 0 <= del_index < len(history):
                    self.history_manager.history.drop(self.history_manager.history.index[del_index], inplace=True)
                    self.history_manager.save_history()
                    print("Record deleted successfully.")
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("No history to delete.")