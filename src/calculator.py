import math
import logging

logging.basicConfig(level=logging.ERROR)


class CalcEngine:
    """
    A simple calculator engine class.
    """

    def Add(self, x, y):
        """Adds two numbers.

        Args:
            x: The first number.
            y: The second number.

        Returns:
            The sum of x and y.
        """
        return x + y

    def calculate_area(self, r):
        """Calculates the area of a circle.

        Args:
            r: The radius of the circle.

        Returns:
            The area of the circle.
        """
        return math.pi * r * r

    def dangerous_op(self):
        """
        Performs a potentially dangerous operation (division by zero).
        Logs the error if it occurs and continues.
        """
        try:
            x = 1 / 0
        except ZeroDivisionError as e:
            logging.error("Division by zero error occurred: %s", e)