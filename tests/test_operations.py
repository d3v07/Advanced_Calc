'''My Calculator Test'''
from calculator.operations import add, multiply, subtract, divide

def test_addition():
    '''Test that addition function works '''    
    assert add(1,1) == 2

def test_subtraction():
    '''Test that addition function works '''    
    assert subtract(1,1) == 0

def test_multiplication():
    '''Test that multiply works'''
    assert multiply(1,1) == 1

def test_division():
    '''Test division'''
    assert divide(1,1) == 1
