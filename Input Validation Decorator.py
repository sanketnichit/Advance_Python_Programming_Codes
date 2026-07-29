def validate_positive(func):
    def wrapper(*args):
        for i in args:
            if not isinstance(i, int) or i <= 0:
                print("Error: All arguments must be positive integers.")
                return
        return func(*args)
    return wrapper


@validate_positive
def add(a, b):
    print("Sum =", a + b)


add(10, 20)
add(10, -5)