# Project Workflow

## Project Initialization (main branch)

### Overview
In this phase, I focused on creating a simple calculator application with the basic four operations of addition, subtraction, multiplication, and division. I developed test files to verify the calculator's functionality and operations. The primary goal was to establish a solid development foundation for Python, ensuring proper implementation of testing frameworks, code quality tools, and coverage analysis.

### Development Environment Setup
I set up a Python virtual environment to isolate project dependencies from the system Python installation. Virtual environments are essential for maintaining clean development environments and preventing package conflicts between different projects. This approach ensures that all developers working on the project have consistent environments.

For dependency management, I used `pip freeze` to generate a `requirements.txt` file This file captures all the project dependencies and their specific versions, making it straightforward for others to replicate the exact environment. The requirements file serves as documentation for the project's dependencies and facilitates easy installation with a simple `pip install -r requirements.txt` command.

### Testing Framework
I integrated pytest as the primary testing framework for the project Pytest offers a clean, intuitive syntax for writing tests and provides powerful features like fixtures, parameterization, and extensive plugin support. The testing structure includes dedicated test files for calculator class behavior and operation verification.

To ensure code quality, I incorporated pylint for static code analysis This tool helps enforce coding standards, identify potential bugs, and maintain a consistent coding style throughout the project. By integrating pylint into the testing workflow, code quality checks become an automatic part of the development process.

For test coverage tracking, I added the coverage tool configured to work with pytest. This allows us to identify untested code paths and ensure comprehensive test coverage across the codebase.

### Testing Commands
```
pytest                     # Runs the tests without pylint or coverage
pytest --pylint            # Runs tests with pylint static code analysis
pytest --pylint --cov      # Runs tests, pylint, and coverage analysis
```

### Version Control Strategy
I established a structured git workflow with proper branching strategies. The development process includes creating feature branches for new functionality, using stash for temporary code storage when switching contexts, and following a clear merge protocol back to the main branch after quality checks pass.

### Continuous Integration
GitHub workflows were configured on the main branch to automate quality checks. These workflows execute the test suite, run pylint analysis, and verify code coverage meets the established thresholds. This automation ensures that code quality is maintained consistently and prevents problematic code from being merged into the main branch.

### Project Structure
The initial project structure follows best practices with separate modules for calculator functionality, clear test organization, and configuration files for development tools. This structure provides a foundation for the application to grow in a maintainable way as new features are added in future phases.


## Enhanced Design Implementation (design branch)

### Overview
This phase focused on restructuring the calculator application using object-oriented programming principles while implementing advanced design methodologies and testing practices. The core objective was to transform the initial implementation into a more robust, maintainable, and extensible codebase through the application of established software design principles.

### Object-Oriented Programming Implementation
I applied the fundamental principles of object-oriented programming to enhance the application structure The implementation leverages abstraction, encapsulation, inheritance, and polymorphism to create a more flexible and maintainable codebase By organizing code around objects rather than actions and logic, the application now better represents the problem domain while providing clearer separation of concerns.

### Design Principles Application
The codebase was restructured according to SOLID principles, ensuring each class has a single responsibility, remains open for extension but closed for modification, and follows proper interface segregation This approach helps "gather together those things that change for the same reason, and separate those things that change for different reasons". Additional design patterns such as DRY (Don't Repeat Yourself) were applied to further enhance code quality and maintainability Code Modularization
Each functionality and class has been moved to separate files for improved code organization and management. This modular approach creates a cleaner structure that enhances readability and makes future maintenance more straightforward. The separation also allows for better isolation of concerns, making the codebase more testable and easier to debug.

### Calculator Class Enhancement
The Calculator class now features static methods that provide stateless functional operations. This design choice improves the reusability of calculator operations without requiring instance creation, while also making the code more intuitive for simple calculations.

### Calculation Class Development
I implemented instance methods on the Calculation class to encapsulate the behavior related to individual calculations. This object-oriented approach ensures that each calculation maintains its own state and behavior, following proper encapsulation principles.

### History Management System
A calculation history system was introduced to store and manage calculation instances. This feature provides the ability to recall, reuse, and analyze previous calculations, enhancing the application's utility. The history system demonstrates practical application of collection management within an object-oriented framework.

### Calculations Class Implementation
Class methods were added to the Calculations class to provide operations that work at the class level rather than the instance level. These methods facilitate better management of calculation collections and demonstrate the effective use of different method types in Python classes.

### Convenience Methods
The Calculations class now includes convenience methods for history management, such as adding, removing, and retrieving calculations. These methods simplify interaction with the calculation history, demonstrating how well-designed interfaces can improve code usability.

### Advanced Testing Techniques
The testing framework was enhanced with parameterized test data, allowing for more comprehensive verification of functionality across different input scenarios. This approach reduces test code duplication while increasing test coverage and scenario validation.

### Test Fixtures Implementation
I introduced fixtures to establish consistent test data and environments across multiple tests. These fixtures streamline test setup and teardown processes, ensuring test reliability and reducing repetitive code in test implementations.

### Code Analysis Configuration
Modifications were made to the .pylintrc configuration file to customize code analysis rules according to project requirements. The workflow files were also updated to ensure continuous integration processes correctly implement the revised linting standards.


## Faker Implementation (faker branch)

### Overview
In this stage, I extended the functionality of the calculator application by integrating the Faker library to generate synthetic test data. Building on the object-oriented foundation established in the design branch, this implementation focuses on enhancing testing capabilities through dynamic data generation and introducing interactive command-line functionality. These additions transform the application from a purely programmatic calculator into a more versatile tool with both API and command-line interfaces.

### Faker Library Integration
I incorporated the Faker library to generate realistic fake data for robust testing scenarios. This powerful Python package allows for the creation of various types of synthetic data that can be used to thoroughly test the calculator application under diverse conditions. The requirements.txt file was updated to include this dependency, ensuring consistent environment setup across development instances.

### Dynamic Test Data Generation
The implementation now supports generating a configurable number of test records dynamically via command-line arguments. This feature enables scalable testing with variable dataset sizes, allowing for both quick verification tests and more comprehensive stress testing with larger data volumes. By parameterizing the number of records, the testing process becomes more flexible and adaptable to different testing needs.

### Command Line Customization
I enhanced the testing framework to accommodate dynamic record generation through custom command-line options. The addition of the `--num_records` parameter allows testers to specify exactly how many synthetic records should be generated for a particular test run, providing granular control over test data volume. This capability was integrated into the pytest configuration to maintain a seamless testing experience.

### Main Application Entry Point
The introduction of main.py serves as the central entry point for the application, enabling both programmatic and command-line usage This file orchestrates the application's components and provides a clean interface for users interacting with the calculator through the terminal. The main module handles user input validation, operation selection, and result presentation in a user-friendly format.

### Terminal Interaction Capabilities
The application now supports direct terminal usage with custom user inputs, allowing for interactive calculation sessions. Users can input operands and operation types, and receive formatted results or appropriate error messages. The terminal interface includes robust error handling for cases such as:
- Division by zero
- Unknown operations
- Invalid numeric inputs

### Test Case Examples
The implementation includes comprehensive test cases for all operations and error conditions, including:
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Error handling for division by zero
- Validation for unknown operations
- Handling of invalid numeric inputs

### Continuous Integration Enhancements
The GitHub workflow was extended to incorporate the new dynamic testing capabilities. The configuration now includes a dedicated step for running tests with a specified number of synthetic records:
```
name: Run num records
run: |
  pytest --num_records=100
```

## Transition to an Interactive Command-Line Application (plugins branch)

### Overview
This phase marked a major milestone in the project, transforming the calculator application from a simple script into a fully interactive command-line application. The focus was on implementing **REPL (Read, Evaluate, Print, Loop)** principles, enabling continuous user interaction. The application was restructured to incorporate design patterns such as the **Command Pattern** and **Factory Method**, along with a dynamic **plugin architecture** for loading commands. These changes made the application modular, extensible, and production-ready.

### Features Added in This Phase

- **Command Pattern and REPL Implementation**: The application now operates continuously, allowing users to input commands interactively.
- **Interactive Calculator Commands**: Users can perform basic arithmetic operations such as addition, subtraction, multiplication, and division interactively.
- **Interactive Menu Commands**: A menu system was introduced to navigate through the available commands and functionalities.
- **Plugin Architecture**: A dynamic plugin system was implemented, allowing new commands to be added without modifying the core application code. This ensures scalability and flexibility for future enhancements.

### Logging Integration

Logging was introduced as a critical feature to improve debugging, monitoring, and tracking of application behavior. It replaces the use of print statements and provides a structured way to capture application events, errors, and user interactions. Below are the key aspects of the logging implementation:

- **Centralized Logging Configuration**: A single logging setup was implemented in the application's entry point (`main.py`) to ensure consistent logging across all modules. This configuration allows for easy management and customization of logging behavior.

- **Log Levels**: Different log levels were used to categorize messages based on their importance:
  - **DEBUG**: Captures detailed information for debugging purposes.
  - **INFO**: Logs general application events and user interactions.
  - **WARNING**: Logs non-critical issues that require attention.
  - **ERROR**: Logs critical errors that disrupt the application's flow.

- **Log File Storage**: Logs are written to a file, ensuring persistent storage for later analysis. This is particularly useful for debugging issues after the application has been executed.

- **Dynamic Plugin Logging**: Each plugin loaded through the plugin architecture has its own logging configuration. This ensures that operations and errors specific to plugins are logged separately, making it easier to debug and monitor plugin behavior.

- **History and Data Logging**: 
  - All operations performed on the history (e.g., LOAD, SAVE, CLEAR, DELETE) are logged with details about the action and its outcome.
  - The CSV command logs details about file operations, such as reading, sorting, and saving data. Errors during file operations are also logged for debugging purposes.

- **Error Tracking**: The logging system captures and logs all errors, including invalid user inputs, file operation issues, and unexpected application behavior. This ensures that all critical issues are recorded for analysis and resolution.

By integrating logging, the application now provides a robust mechanism for tracking its behavior, improving maintainability, and ensuring a better user experience.

### Testing Enhancements
To ensure the reliability of the new features, extensive test cases were added:
- Test cases for the new commands, including the menu and calculator commands.
- Test cases for the dynamic plugin menu to verify seamless integration of plugins.
- Sub-menu logic testing to validate navigation within the menu system. For example, the calculator menu allows users to perform operations and return to the main menu by selecting "5."

### Testing Commands
The following commands can be used to test the application:
```bash
pytest                     # Run all tests
pytest tests/test_main.py  # Run tests for a specific file
pytest --pylint --cov      # Run tests with linting and coverage analysis
```

---

## Data Operations and Advanced Design Patterns 

### Overview
This phase introduced **data-related operations** and further implemented advanced design patterns to enhance the application's functionality. The focus was on managing historical data and integrating data manipulation capabilities using external libraries like **Pandas** and **NumPy**.

### Features Added in This Phase
- **History Command**: 
  - A new command was added to manage the history of user commands.
  - This feature uses the **Singleton Design Pattern** to ensure only one instance of the history manager exists throughout the application.
  - The history command includes a sub-menu with the following operations:
    - **LOAD**: Load previously saved history from a CSV file.
    - **CLEAR**: Clear the current history.
    - **SAVE**: Save the current history to a CSV file.
    - **DELETE**: Delete a specific command from the history.
  - All history operations are recorded in a CSV file using **Pandas**, ensuring persistent storage and easy retrieval.

- **CSV Command**:
  - A new command was introduced to perform data operations on CSV files.
  - This feature demonstrates the use of data structures and libraries like **Pandas** and **NumPy**.
  - The CSV command allows users to:
    - Read data from a CSV file.
    - Sort the data based on specific criteria (e.g., population).
    - Save the sorted data to a new CSV file.
  - For example, the application processes data from US states, sorts it by population in ascending order, and generates a new file.

### Testing Enhancements
The testing framework was updated to include test cases for the new commands and functionalities:
- Test cases for the history command and its sub-menu operations.
- Test cases for the CSV command to validate data reading, sorting, and saving.
- Test cases for the integration of **Pandas** and **NumPy** in the application.

### Testing Commands
The following commands can be used to test the application:
```bash
pytest                     # Run all tests
pytest tests/test_main.py  # Run tests for a specific file
pytest --pylint --cov      # Run tests with linting and coverage analysis
```

---

## Running the Application
The application can be run interactively using the following command:
```bash
python main.py
```

---

## Summary
These phases represent a significant evolution of the calculator application, transforming it into a **production-ready, interactive command-line tool** with advanced features. By incorporating design patterns, dynamic plugin architecture, data operations, and DevOps practices, the application is now modular, extensible, and capable of handling real-world use cases.