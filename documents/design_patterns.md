# Design Patterns Implemented in the Project

## Command Pattern:
The Command Pattern is particularly effective in a REPL (Read-Eval-Print Loop) application for several reasons:

- **Modularity**: Each command is encapsulated within its own class, resulting in a clean and organized application structure.
- **Extensibility**: Adding new commands is simple and does not require modifying existing code, making updates and maintenance more efficient.
- **Undo Operations**: By maintaining a history of executed commands, the pattern supports undo functionality, allowing users to easily revert actions.
- **Separation of Concerns**: The pattern decouples input parsing from command execution, simplifying the main loop and improving code clarity.
- **Improved Testability**: Commands can be tested independently, enhancing the reliability and maintainability of the application.

The Command Pattern is instrumental in ensuring that REPL-based applications remain scalable, maintainable, and user-friendly. It provides a robust framework for managing commands, enabling flexibility and ease of use while adhering to clean design principles.
Sample code from the project: 
```
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command_instance: Command):
        self.commands[command_name] = command_instance

    def execute_command(self, command_name: str):
        # Easier to Ask for Forgiveness than Permission (EAFP)
        try:
            self.commands[command_name].execute()
        except KeyError: # Catch the exception if the operation fails
            print(f"No such command: {command_name}") # Exception caught and handled gracefully

    def list_commands(self):
        for index, command_name in enumerate(self.commands, start=1):
            print(f"{index}. {command_name}")

    def get_command_by_index(self, index: int):
        try:
            command_name = list(self.commands.keys())[index]
            return command_name
        except IndexError:
            return None
```
## Singleton Pattern

The **Singleton Pattern** is a creational design pattern that ensures a class has only one instance while providing a global access point to it. This pattern is particularly useful in scenarios where centralized control or shared resources are required, making it a common solution for managing stateful information in software systems.

### Key Benefits of the Singleton Pattern:
- **Controlled Access**: The Singleton Pattern ensures that only one instance of a class exists, providing controlled access to this instance. This is critical for coordinating actions across the system and avoiding conflicts caused by multiple instances.
- **Resource Management**: It is ideal for managing shared resources or configurations, such as database connections, logging systems, or application settings. By sharing a single instance, the pattern ensures efficient use of resources.
- **Consistency**: Since all parts of the application access the same instance, the Singleton Pattern guarantees that stateful information remains consistent throughout the system.

### Usage in the Project:
In this project, the Singleton Pattern is used to manage the **history of commands**. The history manager is implemented as a Singleton to ensure that:
- There is only one instance of the history manager throughout the application.
- All components of the application access the same history state, ensuring consistency.
- The history manager acts as a global access point for storing, retrieving, and managing command history.

The Singleton Pattern plays a crucial role in maintaining centralized control and ensuring the reliability of shared resources, making it an essential part of the project's architecture.

```
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class CommandHistoryManager(metaclass=Singleton):
    TOTAL_RECORDS = 50  #  last 50 commands

    def __init__(self):
        self.history_file = 'data/command_history.csv'
        if os.path.exists(self.history_file):
            self.history = pd.read_csv(self.history_file)
            # Ensure that only the latest TOTAL_RECORDS are loaded
            self.history = self.history.tail(self.TOTAL_RECORDS)
        else:
            self.history = pd.DataFrame(columns=['Timestamp', 'Command'])
```
## Factory Method:
The Factory Method pattern defines an interface for creating an object but lets subclasses alter the type of objects that will be created. It is beneficial for:

- Flexibility: Allows the class to defer instantiation to subclasses, providing flexibility in determining what objects are created.
- Extensibility: Supports adding new types of products without changing the existing factory's code, enhancing extensibility.
- Decoupling: Reduces the dependency between the application and concrete classes, promoting loose coupling.

Sample code from the project
```
self.command_handler.register_command("menu", MenuCommand(self.command_handler))

```
## Memento Pattern

The **Memento Pattern** is a behavioral design pattern that captures and externalizes an object's internal state, enabling the object to be restored to that state later. This pattern provides a way to implement state management without violating encapsulation principles Key Advantages:

- **Undo Functionality**: The pattern facilitates implementing undo mechanisms in applications by allowing objects to be rolled back to previous states. This is particularly valuable in interactive applications where users may need to reverse their actions.

- **State Preservation**: It enables saving and restoring object states without exposing implementation details This encapsulation ensures that the internal representation remains protected while still allowing state management.

- **Snapshot Handling**: The Memento Pattern is useful for taking snapshots of application states that can be restored later. These snapshots serve as checkpoints that capture the complete state of an object at specific points in time.

### Application in the Project:

In this project, the functionality of the **CommandHistoryManager** bears a strong resemblance to the Memento Pattern. It effectively serves as a mechanism for capturing and storing command states so they can be retrieved or restored later. This implementation allows the application to maintain a history of commands and potentially implement features like undo/redo operations.

The pattern is particularly valuable in this context because it provides a structured approach to managing state history while maintaining clean separation between the objects being tracked and the history-tracking mechanism itself.

```
def get_history(self):
        # Return a list of command names for backward compatibility
        return self.history['Command'].tolist()

    def clear_history(self):
        self.history = pd.DataFrame(columns=['Timestamp', 'Command'])
        self.save_history()

    def save_history(self):
        """Saves the current command history to a CSV file."""
        self.history.to_csv(self.history_file, index=False)

    def load_history(self):
        """Loads the command history from a CSV file into a DataFrame."""
        if os.path.exists(self.history_file):
            return pd.read_csv(self.history_file)
        return pd.DataFrame(columns=['Timestamp', 'Command'])
```