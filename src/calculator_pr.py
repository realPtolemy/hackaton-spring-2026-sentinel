PI = 3.14  # Constant for the mathematical value of Pi.

class CalcEngine:
    """
    A class providing basic mathematical calculation functionalities.
    """

    def add(self, x: float, y: float) -> float:
        """
        Adds two numbers together.

        Args:
            x: The first number.
            y: The second number.

        Returns:
            The sum of x and y.
        """
        return x + y

    def calculate_area(self, radius: float) -> float:
        """
        Calculates the area of a circle given its radius.

        Args:
            radius: The radius of the circle.

        Returns:
            The calculated area of the circle.
        """
        return PI * radius * radius

    def dangerous_op(self) -> None:
        """
        Performs an operation that is known to cause a ZeroDivisionError.
        The error is caught and handled silently to prevent program termination.
        """
        try:
            x = 1 / 0
        except ZeroDivisionError:
            # This specific exception is caught to prevent program termination
            # in a scenario where division by zero might occur due to external factors.
            pass