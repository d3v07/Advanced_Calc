"""
This file contains the fixtures and hooks for the calculator test"""
from decimal import Decimal
from faker import Faker
from calculator.operations import add, subtract, multiply, divide

fake = Faker()

def generate_test_data(num_records):
    """crearing test data"""
    operations = [add, subtract, multiply, divide]
    for _ in range(num_records):
        a = Decimal(fake.random_number(digits=2))
        b = Decimal(fake.random_number(digits=2)) if _ % 4 != 3 else Decimal(fake.random_number(digits=1, fix_len=True))
        operation = fake.random_element(elements=operations)

        # Ensure b is not zero if operation is divide
        if operation is divide:
            b = Decimal(fake.random_number(digits=2, fix_len=True)) if b == 0 else b # pragma: no cover

        # Calculate the expected result based on the operation, include try-except for divide
        try:
            expected = operation(a, b)
        except ZeroDivisionError: # pragma: no cover
            continue  # Skip this iteration and generate a new set of data

        yield a, b, operation, expected


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption("--num_records", action="store", default=5, type=int, help="Number of test records to generate")

def pytest_generate_tests(metafunc):
    """Generate test data for the test_calculation_operations test function"""
    if "a" in metafunc.fixturenames and \
       "b" in metafunc.fixturenames and \
       "operation" in metafunc.fixturenames and \
       "expected" in metafunc.fixturenames:
        num_records = metafunc.config.getoption("num_records")
        metafunc.parametrize("a,b,operation,expected", list(generate_test_data(num_records)))
