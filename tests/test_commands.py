"""Test cases for the commands module."""
import logging
import sys
from unittest.mock import MagicMock,patch,mock_open
import os
import pandas as pd
import pytest
from app import App
from app.commands import Command, CommandHandler,CommandHistoryManager
from app.plugins.calculator import CalculatorCommand
from app.plugins.csv import CsvCommand
from app.plugins.history import HistoryCommand
from app.plugins.menu import MenuCommand
from app.plugins.exit import ExitCommand

def test_app_greet_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'greet' command and its logging."""
    inputs = iter(['5', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output
        captured = capfd.readouterr()
        assert "Hello, World!" in captured.out

        # Now, check the log messages
        assert "Executing GreetCommand." in caplog.text
        assert "GreetCommand executed successfully." in caplog.text




def test_app_menu_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'menu' command and its logging."""
    inputs = iter(['7','0','exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        try:
            app.start()  # Start the application without expecting SystemExit

            # Capture and assert the expected output
            captured = capfd.readouterr()
            assert "Available commands:" in captured.out
            # Assert that the menu display was logged
            assert "Displaying main menu to user." in caplog.text

            # Since the user selects 'exit', which is simulated by input, check the log for exit confirmation
            assert "User selected to exit the program." in caplog.text
        except SystemExit as e:
            assert str(e) == "Exiting program."

# Mock operation classes
class MockAddCommand(Command):
    """Mock command for addition."""
    def execute(self):
        logging.info("Performing addition")

class MockSubtractCommand(Command):
    """Mock command for subtraction."""
    def execute(self):
        logging.info("Performing subtraction")

@pytest.fixture
def mock_operations(monkeypatch):
    """Fixture to mock the operations loaded by the CalculatorCommand."""
    def mock_load_operations(self):
        return {'1': MockAddCommand(), '2': MockSubtractCommand()}
    monkeypatch.setattr(CalculatorCommand, "load_operations", mock_load_operations)

def test_calculator_display_operations_and_exit(capfd, monkeypatch, mock_operations):
    """Test the CalculatorCommand display and exit functionality."""
    monkeypatch.setattr('builtins.input', lambda _: '5')
    calculator_cmd = CalculatorCommand()
    calculator_cmd.execute()
    captured = capfd.readouterr()
    assert "\nCalculator Operations:" in captured.out
    assert "1. MockAddCommand" in captured.out
    assert "2. MockSubtractCommand" in captured.out
    assert "5. Back" in captured.out

# inputs = iter(['1', '0'])
# monkeypatch.setattr('builtins.input', lambda _: next(inputs, 'default_value'))

def test_calculator_execute_operation(capfd, monkeypatch):
    """Test the CalculatorCommand execute operation functionality."""
    inputs = ['1', '2', '3', '5']
    input_generator = (input for input in inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))
    calculator_cmd = CalculatorCommand()
    calculator_cmd.execute()
    captured = capfd.readouterr()
    assert "The result is 5.0" in captured.out

class MockCommand(Command):
    """Mock command for testing."""
    def execute(self):
        """Mock command execution."""
        print("Mock command executed.")

@pytest.fixture
def command_handler_with_commands():
    """Fixture to return a CommandHandler with registered commands."""
    handler = CommandHandler()
    handler.register_command('test', MockCommand())
    handler.register_command('help', MockCommand())
    return handler

def test_menu_command_display_and_exit(capfd, monkeypatch, command_handler_with_commands):
    """Test the MenuCommand display and exit functionality."""
    monkeypatch.setattr('builtins.input', lambda _: '0')
    # Mock sys.exit to prevent the test from exiting
    mock_exit = MagicMock()
    monkeypatch.setattr(sys, 'exit', mock_exit)
    menu_cmd = MenuCommand(command_handler_with_commands)
    menu_cmd.execute()

    captured = capfd.readouterr()
    assert "\nMain Menu:" in captured.out
    assert "1. Test" in captured.out
    assert "2. Help" in captured.out
    assert "Enter the number of the command to execute, or '0' to exit." in captured.out
    mock_exit.assert_called_once_with("Exiting program.")  # Verify sys.exit was called

def test_menu_command_invalid_selection(capfd, monkeypatch, command_handler_with_commands):
    """Test the MenuCommand invalid selection handling."""
    inputs = iter(['999', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Mock sys.exit to prevent the test from exiting
    monkeypatch.setattr(sys, 'exit', MagicMock())

    menu_cmd = MenuCommand(command_handler_with_commands)
    menu_cmd.execute()

    captured = capfd.readouterr()
    assert "Invalid selection. Please enter a valid number." in captured.out

def test_csv_command(capfd, tmpdir, caplog):
    """Test that the CsvCommand correctly handles reading, sorting, and reducing a CSV file."""
    with patch('os.path.exists', return_value=False), patch('os.makedirs'):
         # your test code here
         # Setup a temporary directory and CSV file for the test
        data_dir = tmpdir.mkdir("data")
        input_file_path = data_dir.join("gpt_states.csv")
        output_file_path = data_dir.join("sorted_states.csv")

        # Sample data to write to the input CSV file
        sample_data = {
             "State Abbreviation": [
                 "CA", "NJ", "TX", "FL", "IL", "NY", "PA", "OH", "MI", "GA", 
                 "NC", "VA", "WA", "MA", "AZ", "MN", "MO", "CO", "WI", "OR"
             ],
             "State Name": [
                 "California", "New Jersey", "Texas", "Florida", "Illinois", "New York", "Pennsylvania", 
                 "Ohio", "Michigan", "Georgia", "North Carolina", "Virginia", "Washington", "Massachusetts", 
                 "Arizona", "Minnesota", "Missouri", "Colorado", "Wisconsin", "Oregon"
             ],
             "Population": [
                 39538223, 8882190, 29145505, 21538187, 12671821, 20201249, 12801989,
                 11799448, 10077331, 10711908, 10488084, 8631393, 7693612, 7029917,
                 7151502, 5700671, 6154913, 5773714, 5893718, 4237256
             ],
             "Capital": [
                 "Sacramento", "Trenton", "Austin", "Tallahassee", "Springfield", "Albany", "Harrisburg", 
                 "Columbus", "Lansing", "Atlanta", "Raleigh", "Richmond", "Olympia", "Boston", 
                 "Phoenix", "St. Paul", "Jefferson City", "Denver", "Madison", "Salem"
             ],
             "GDP": [
                 "3.1T", "0.6T", "1.9T", "1.1T", "0.9T", "1.7T", "0.8T", "0.7T", "0.5T", "0.6T", 
                 "0.6T", "0.5T", "0.6T", "0.8T", "0.4T", "0.4T", "0.3T", "0.4T", "0.3T", "0.3T"
             ]
         }

        df = pd.DataFrame(sample_data)
        df.to_csv(input_file_path, index=False)

         # Mock the CsvCommand to use the temporary directory and files
        csv_command = CsvCommand()
        csv_command._CsvCommand__data_dir = str(data_dir)  # Override private attributes
        csv_command._CsvCommand__input_file_path = str(input_file_path)
        csv_command._CsvCommand__output_file_path = str(output_file_path)
        csv_command._CsvCommand__sort_by = 'Population'
        csv_command._CsvCommand__columns_to_keep = ['State Abbreviation', 'State Name', 'Population']
        with caplog.at_level(logging.INFO):
            csv_command.execute()

        # Capture and assert the expected output
        captured = capfd.readouterr()
        assert "Processed data saved to" in captured.out
        assert "States from CSV, sorted by Population" in captured.out
        assert "CA: California" in captured.out  # Check for a sorted entry

        # Now, check the log messages
        assert "The directory" in caplog.text
        assert "Processed data saved to" in caplog.text
        assert "Record 0: OR: Oregon" in caplog.text

        # Clean up
        data_dir.remove()

def test_app_calculator_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'calculator' command and its logging."""
    # Added more inputs to handle all calculator interactions
    inputs = iter(['1', '1', '1', '2', '5', '0', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output for calculator
        captured = capfd.readouterr()
        assert "Calculator Operations:" in captured.out

        # Check the log messages for successful execution
        assert "Executing calculator operation: Add" in caplog.text

def test_app_csv_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'csv' command and its logging."""
    # Updated to ensure CSV command is properly selected
    inputs = iter(['2', '0', 'exit'])  # Simplified for basic CSV command testing
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output for CSV
        captured = capfd.readouterr()
        # Match a more general string that would appear in the CSV command output
        assert "CSV" in captured.out or "csv" in captured.out.lower()

        # Check for a more general log message related to CSV
        assert "csv" in caplog.text.lower()

def test_app_goodbye_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'goodbye' command and its logging."""
    inputs = iter(['4', 'exit'])  # Adjust '4' if the position of GoodbyeCommand differs
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output for goodbye
        captured = capfd.readouterr()
        assert "Goodbye" in captured.out

        # Check the log messages for the execution of the GoodbyeCommand
        assert "Executing GoodbyeCommand." in caplog.text

def test_app_greet_commands(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'greet' command and its logging."""
    inputs = iter(['5', 'exit'])  # Adjust '5' if the position of GreetCommand differs
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output for greet
        captured = capfd.readouterr()
        assert "Hello, World!" in captured.out

        # Check the log messages for the execution of the GreetCommand
        assert "Executing GreetCommand." in caplog.text

@pytest.fixture
def mock_command_history_manager():
    """Mock history manager fixture"""
    with patch('app.commands.CommandHistoryManager', autospec=True) as mock:
        # Setup mock to return a predefined history
        mock_instance = mock.return_value
        mock_instance.get_history.return_value = ['history', 'menu', 'history']
        yield mock

def test_app_history_command_operations(mock_command_history_manager, capfd, caplog):
    """Test history command in REPL"""
    # Setup inputs to test all operations
    inputs = iter(['1', '2', '3', '4', '5'])

    with patch('builtins.input', lambda _: next(inputs)):
        with caplog.at_level(logging.INFO):
            history_command = HistoryCommand()
            history_command.execute()

    # Verify output contains expected content
    captured = capfd.readouterr()

    # Check menu headers are displayed
    assert "Command History Operations:" in captured.out

    # Check operations are listed
    assert "1. Load History" in captured.out
    assert "2. Save History" in captured.out
    assert "3. Clear History" in captured.out
    assert "4. Delete History Record" in captured.out
    assert "5. Back" in captured.out

    # Check operation outputs
    assert "Command History:" in captured.out
    assert "History saved successfully." in captured.out
    assert "History cleared successfully." in captured.out
    assert "No history to delete." in captured.out

def test_calculator_divide_operation(capfd, monkeypatch, caplog):
    """Test the calculator's divide operation."""
    # Simulate user selecting calculator(1), divide(2), entering numbers, then back(5), then exit
    inputs = iter(['1', '2', '10', '2', '5', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Check output
        captured = capfd.readouterr()
        assert "Calculator Operations:" in captured.out
        assert "The result is 5.0" in captured.out

        # Check logs
        assert "Executing Divide command." in caplog.text
        assert "Division result: 5.0" in caplog.text

def test_calculator_divide_by_zero(capfd, monkeypatch, caplog):
    """Test the calculator's divide operation with division by zero."""
    inputs = iter(['1', '2', '10', '0', '5', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.WARNING):
        app = App()
        app.start()

        # Check output
        captured = capfd.readouterr()
        assert "Cannot divide by zero" in captured.out

        # Check logs
        assert "Attempted division by zero" in caplog.text

def test_calculator_multiply_operation(capfd, monkeypatch, caplog):
    """Test the calculator's multiply operation."""
    inputs = iter(['1', '3', '4', '5', '5', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Check output
        captured = capfd.readouterr()
        assert "Calculator Operations:" in captured.out
        assert "The result is 20.0" in captured.out

        # Check logs
        assert "Executing Multiply command." in caplog.text
        assert "Multiplication result: 20.0" in caplog.text

def test_calculator_subtract_operation(capfd, monkeypatch, caplog):
    """Test the calculator's subtract operation."""
    inputs = iter(['1', '4', '8', '3', '5', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Check output
        captured = capfd.readouterr()
        assert "Calculator Operations:" in captured.out
        assert "The result is 5.0" in captured.out

        # Check logs
        assert "Executing Subtract command." in caplog.text
        assert "Subtraction result: 5.0" in caplog.text

def test_exit_command(capfd, caplog):
    """Test that the ExitCommand logs a message, prints exit text, and calls sys.exit(0)."""

    # Setup logging capture
    caplog.set_level(logging.INFO)

    # Patch sys.exit to prevent actual program termination
    with patch('sys.exit') as mock_exit:
        # Execute the command
        exit_command = ExitCommand()
        exit_command.execute()

        # Check printed output
        captured = capfd.readouterr()
        assert "Exiting..." in captured.out

        # Check logs
        assert "Executing ExitCommand - Application exiting..." in caplog.text

        # Verify sys.exit was called with argument 0
        mock_exit.assert_called_once_with(0)

def test_calculator_invalid_selection(capfd, caplog):
    """Test handling of invalid selection in CalculatorCommand."""
    # Mock operations and user input
    with patch.object(CalculatorCommand, 'load_operations', return_value={'1': MagicMock()}):
        with patch('builtins.input', side_effect=['invalid', '5']):
            with caplog.at_level(logging.WARNING):
                # Execute calculator command
                calculator = CalculatorCommand()
                calculator.execute()

                # Check output
                captured = capfd.readouterr()
                assert "Invalid selection. Please try again." in captured.out

                # Check logging
                assert "Invalid selection in CalculatorCommand" in caplog.text

def test_calculator_load_plugin_type_error(capfd, caplog):
    """Test handling of TypeError during plugin loading."""
    # Create a mock module with attributes that will cause TypeError
    mock_module = MagicMock()

    # This will make getattr return a non-class object that will trigger TypeError
    # when issubclass() is called on it
    def mock_getattr(obj, name):
        if name == "NonClassAttribute":
            return "string_not_a_class"  # This will cause TypeError in issubclass
        return MagicMock()

    with patch('importlib.import_module', return_value=mock_module):
        with patch('pkgutil.iter_modules', return_value=[(None, 'test_plugin', False)]):
            with patch('builtins.dir', return_value=["NonClassAttribute"]):
                with patch('builtins.getattr', mock_getattr):
                    # This should continue without raising exception due to TypeError handling
                    calculator = CalculatorCommand()
                    # Verify operations dictionary was created
                    assert isinstance(calculator.operations, dict)

def test_calculator_skip_subpackage():
    """Test that subpackages are skipped during plugin loading."""
    # Mock a subpackage (ispkg=True) in the iterator
    mock_finder = MagicMock()
    mock_plugins = [(mock_finder, "subpackage", True)]  # ispkg=True makes this a subpackage

    with patch('pkgutil.iter_modules', return_value=mock_plugins):
        calculator = CalculatorCommand()
        # Since the only item is a subpackage and should be skipped,
        # operations should be empty
        assert len(calculator.operations) == 0

def test_calculator_skip_specific_type_error(capfd, caplog):
    """Test that specific 'issubclass() arg 1 must be a class' TypeError is handled properly."""
    test_plugin_name = "test_plugin"

    # Create a mock module and mock finder
    mock_module = MagicMock()
    mock_finder = MagicMock()

    with patch('pkgutil.iter_modules', return_value=[(mock_finder, test_plugin_name, False)]):
        with patch('importlib.import_module', return_value=mock_module):
            # Make getattr return a non-class object that will cause the specific TypeError
            def mock_getattr_function(obj, name):
                if obj == mock_module and name == "TestAttribute":
                    return "not_a_class"  # This will cause TypeError in issubclass
                return MagicMock()  # Default case

            with patch('builtins.dir', return_value=["TestAttribute"]):
                with patch('builtins.getattr', side_effect=mock_getattr_function):
                    # Specific TypeError should be caught and handled without raising
                    calculator = CalculatorCommand()

                    # Verify calculator was instantiated and operations dict exists
                    assert isinstance(calculator.operations, dict)

                    # Verify no error was logged (the specific TypeError is silently ignored)
                    assert "Error loading calculator plugin" not in caplog.text
def test_history_invalid_selection(capfd, caplog):
    """Test handling of invalid selection in HistoryCommand."""
    with patch('builtins.input', side_effect=['invalid', '5']):
        with caplog.at_level(logging.WARNING):
            history_command = HistoryCommand()
            history_command.execute()

            # Check output
            captured = capfd.readouterr()
            assert "Invalid selection. Please try again." in captured.out

            # Check logs
            assert "Invalid selection in HistoryCommand." in caplog.text

def test_history_empty_history_load(capfd):
    """Test load_history method with empty history."""
    # Create mock with empty history
    mock_manager = MagicMock()
    mock_manager.get_history.return_value = []

    history_command = HistoryCommand()
    history_command.history_manager = mock_manager

    # Test load_history with empty history
    history_command.load_history()

    # Check output
    captured = capfd.readouterr()
    assert "No history found." in captured.out

def test_history_delete_empty_history(capfd):
    """Test delete_history_record with empty history."""
    # Create mock with empty history
    mock_manager = MagicMock()
    mock_manager.get_history.return_value = []

    history_command = HistoryCommand()
    history_command.history_manager = mock_manager

    # Test delete with empty history
    history_command.delete_history_record()

    # Check output
    captured = capfd.readouterr()
    assert "No history to delete." in captured.out

def test_history_delete_valid_record(capfd):
    """Test deleting a valid history record."""
    # Create mock with sample history
    mock_manager = MagicMock()
    mock_manager.get_history.return_value = ['cmd1', 'cmd2', 'cmd3']

    # Create a mock DataFrame for history
    mock_df = MagicMock()
    # Setup index to handle the lookup correctly
    mock_df.index = pd.RangeIndex(0, 3)
    mock_manager.history = mock_df

    with patch('builtins.input', return_value='2'):  # Select record #2
        history_command = HistoryCommand()
        history_command.history_manager = mock_manager
        history_command.delete_history_record()

        # Check that drop was called with index 1 (2-1)
        mock_df.drop.assert_called_once()
        # First argument should be index 1
        assert mock_df.drop.call_args[0][0] == 1
        mock_manager.save_history.assert_called_once()

        # Check output
        captured = capfd.readouterr()
        assert "Record deleted successfully." in captured.out

def test_history_delete_invalid_index(capfd):
    """Test delete_history_record with invalid index selection."""
    # Create mock with sample history
    mock_manager = MagicMock()
    mock_manager.get_history.return_value = ['cmd1', 'cmd2']

    # Setup a MagicMock for DataFrame that has a valid index property
    mock_df = MagicMock()
    # Make index behave like it has only 2 items
    mock_df.index = pd.RangeIndex(0, 2)
    mock_manager.history = mock_df

    with patch('builtins.input', return_value='10'):  # Select invalid record #10
        history_command = HistoryCommand()
        history_command.history_manager = mock_manager
        history_command.delete_history_record()

        # Check output
        captured = capfd.readouterr()
        assert "Invalid selection. Please try again." in captured.out
        # Verify drop wasn't called
        mock_df.drop.assert_not_called()

def test_history_delete_non_numeric(capfd):
    """Test delete_history_record with non-numeric input."""
    # Create mock with sample history
    mock_manager = MagicMock()
    mock_manager.get_history.return_value = ['cmd1', 'cmd2']

    with patch('builtins.input', return_value='abc'):  # Non-numeric input
        history_command = HistoryCommand()
        history_command.history_manager = mock_manager
        history_command.delete_history_record()

        # Check output
        captured = capfd.readouterr()
        assert "Please enter a valid number." in captured.out

def test_read_sort_and_reduce_exception_handling(caplog):
    """Test exception handling in read_sort_and_reduce method (lines 25-27)"""
    csv_command = CsvCommand()

    # Patch pd.read_csv to raise an exception
    with patch('pandas.read_csv', side_effect=Exception("Test exception")):
        with caplog.at_level(logging.ERROR):
            result = csv_command.read_sort_and_reduce()

            # Verify error is logged and None is returned
            assert "Error processing the file: Test exception" in caplog.text
            assert result is None

def test_execute_non_writable_directory(caplog):
    """Test handling of non-writable data directory (lines 37-38)"""
    csv_command = CsvCommand()

    # Patch os.path.exists to return True and os.access to return False
    with patch('os.path.exists', return_value=True):
        with patch('os.access', return_value=False):
            with caplog.at_level(logging.ERROR):
                csv_command.execute()

                # Verify error is logged
                assert "The directory './data' is not writable." in caplog.text

def test_execute_with_none_dataframe(tmp_path, caplog):
    """Test execute when read_sort_and_reduce returns None (line 41)"""
    csv_command = CsvCommand()

    # Create a mock CSV file that can be read after the None branch
    mock_csv_data = "State Abbreviation,State Name,Population\nCA,California,39538223"
    mock_file = tmp_path / "sorted_states.csv"
    mock_file.write_text(mock_csv_data)

    with patch.object(csv_command, '_CsvCommand__output_file_path', str(mock_file)):
        # Patch read_sort_and_reduce to return None
        with patch.object(csv_command, 'read_sort_and_reduce', return_value=None):
            # Ensure directory exists and is writable
            with patch('os.path.exists', return_value=True):
                with patch('os.access', return_value=True):
                    # Execute the command
                    csv_command.execute()
