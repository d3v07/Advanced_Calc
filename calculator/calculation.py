# Import modules
from decimal import Decimal
from typing import Callable
from calculator.operations import add, subtract, multiply, divide

# Definition of the Calculation class with type annotations for improved readability and safety
class Calculation:
    # Constructor
    def __init__(self, a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        self.a = a
        self.b = b
        self.operation = operation
    
    @staticmethod    
    def create(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        return Calculation(a, b, operation)

    def perform(self) -> Decimal:
        """Perform the stored calculation and return the result."""
        return self.operation(self.a, self.b)

    def __repr__(self):
        """Return a simplified string representation of the calculation."""
        return f"Calculation({self.a}, {self.b}, {self.operation.__name__})"