class CalculationEngine:
    """
    A class that performs calculations.
    """

    PI_VALUE = 3.14
    """Constant representing Pi."""

    def add(self, x: float, y: float) -> float:
        """
        Adds two numbers together.

        Args:
            x: The first number.
            y: The second number.

        Returns:
            The sum of the two numbers.
        """
        return x + y

    def circle_area(self, radius: float) -> float:
        """
        Calculates the area of a circle.

        Args:
            radius: The radius of the circle.

        Returns:
            The area of the circle.
        """
        # Using a constant for pi to improve readability and maintainability.
        return self.PI_VALUE * radius * radius

    def risky_operation(self) -> None:
        """
        Demonstrates exception handling for a risky operation.
        """
        try:
            # Intentionally attempting division by zero to demonstrate exception handling.
            ONE = 1
            ZERO = 0
            ONE / ZERO
        except ZeroDivisionError as e:
            # Catching the specific exception to handle it gracefully.
            print(f"Caught ZeroDivisionError: {e}")

    def area(self, radius: float) -> float:
        """
        Calculates the area of a circle.

        Args:
            radius: The radius of the circle.

        Returns:
            The area of the circle.
        """
        # Using a constant for pi to improve readability and maintainability.
        return self.PI_VALUE * radius * radius