'''
This is test calculation
'''
# Import main modules
# pylint: disable=unnecessary-dunder-call, invalid-name
from decimal import Decimal
import pytest
from faker import Faker
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide

# Setup Faker
faker = Faker()

# Generate test data using Faker
def generate_test_data(num_cases=10):
    """
    Generate test data for the calculation operations.
    """
    operations = [add, subtract, multiply, divide]
    test_data = []
    for _ in range(num_cases):
        a = Decimal(faker.random_number(digits=2, fix_len=True))
        b = Decimal(faker.random_number(digits=2, fix_len=True))
        for operation in operations:
            # Avoid division by zero
            if operation == divide and b == 0:
                b = Decimal(faker.random_number(digits=2, fix_len=True, min=1))
            expected = operation(a, b)
            test_data.append((a, b, operation, expected))
    return test_data
# Parametrize the test function with dynamically generated data
@pytest.mark.parametrize("a, b, operation, expected", generate_test_data())
def test_operations(a, b, operation, expected):
    """
    Test calculation operations with dynamically generated test data
    """
    assert operation(a, b) == expected

# Retain fixture for previous test cases with edge case scenarios
@pytest.mark.parametrize("a, b, operation, expected",[])
def test_calculation_operations(a, b, operation, expected):
    """
    Test calculation operations with various scenarios.
    """
    calc = Calculation(a, b, operation)
    assert calc.perform() == expected, f"Failed {operation.__name__} operation with {a} and {b}"

def test_calculation_repr():
    """
    Test the string representation (__repr__) of the Calculation class.
    """
    calc = Calculation(Decimal('10'), Decimal('5'), add)
    expected_repr = "Calculation(10, 5, add)"
    assert calc.__repr__() == expected_repr, "The __repr__ method output does not match the expected string."

def test_divide_by_zero():
    """
    Test division by zero to ensure it raises a ValueError.
    """
    calc = Calculation(Decimal('10'), Decimal('0'), divide)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.perform()
