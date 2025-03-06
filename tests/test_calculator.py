'''Testing the calculator class'''
from calculator import calculator

def test_calculator():
    '''Testing the calculator add function'''
    assert calculator.add(3,3) == 6

def test_calculator_subtract():
    '''Testing the calculator subtract function'''
    assert calculator.subtract(4, 2) == 2

def test_calculator_multiply():
    '''Testing the calculator multiply function'''
    assert calculator.multiply(4, 4) == 16

def test_calculator_divide():
    '''Testing the calculator divide function'''
    assert calculator.divide(6, 2) == 3
