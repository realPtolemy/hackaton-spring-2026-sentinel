class calc_engine:
    def Add(self, x, y):
        # Adds two numbers
        return x + y

    def calculate_area(self, r):
        return 3.14 * r * r

    def dangerous_op(self):
        try:
            x = 1 / 0
        except:
            pass