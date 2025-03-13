# MIDTERM IS601 - ADVANCED CALCULATOR

## Project Introduction
Welcome to the Advanced Python Calculator Application, a demonstration of modern software engineering practices applied to a calculator system. This project showcases clean code architecture, design pattern implementation, and extensible functionality in a practical application. Below you'll find a video demonstration of the application in action, which highlights the key features and user interface.

[video link (video to be made yet)] - Watch the calculator application in action to see how it handles calculations, manages history, and leverages its plugin architecture through an intuitive command-line interface.

## Project Summary
This project implements a sophisticated Python-based calculator with a focus on software engineering best practices. It features a command-line interface, extensible plugin architecture, comprehensive logging, and robust data handling capabilities. To see my project workflow [click here](documents/project_flow.md).

### Key Functionalities:

1) Command-Line Interface (REPL)
- Interactive Read-Eval-Print Loop for direct user engagement
- Support for basic arithmetic operations (addition, subtraction, multiplication, division)
- History management with load, save, clear, and delete operations
- OpenAI plugin framework for future AI integration
- "Menu" command to discover available functionalities

2) Plugin System Architecture
- Dynamic loading of plugins without core code modification
- Extensible design allowing seamless feature additions
- Command discovery and integration through a unified interface

3) Data Management with Pandas
- Efficient calculation history tracking
- CSV file operations for persistent storage
- Structured data manipulation capabilities

4) Professional Development Practices
- Comprehensive logging with configurable severity levels (INFO, WARNING, ERROR)
- Environment variable configuration for flexible deployment
- Adherence to PEP 8 standards and clean code principles

### Design Pattern Implementation:

The application incorporates several design patterns to address specific architectural challenges:

1) Command Pattern
- Structured command handling within the REPL interface
- Encapsulated operations with consistent execution flow

2) Singleton Pattern
- Implemented in the `CommandHistoryManager` to ensure single instance
- Provides global access point for history management

3) Factory Method
- Used in the Menu command to generate available commands
- Dynamically discovers and loads plugin commands

4) Memento Pattern
- History management functionality captures and restores calculation states
- Enables undo/redo capabilities through state externalization

To see how I implemented it in project[click here](documents/design_patterns.md)

### Quality Assurance

1) Testing Framework
- 90% test coverage achieved using Pytest
- Comprehensive unit and integration tests

2) Code Quality
- Verified compliance with PEP 8 standards via Pylint
- Logical commit history demonstrating clear development progression

3) Documentation
- Comprehensive documentation of commands, design patterns, and architecture
- Clear explanation of implementation decisions and technical approaches

### Conclusion

This calculator application demonstrates the application of advanced software engineering principles in a seemingly simple domain. Through careful architecture, design pattern implementation, and quality assurance practices, it serves as an exemplar of professional Python development techniques.