def decorator(function):
    def wrapper():
        print("==========")
        function()
        print("==========")
    return wrapper


@decorator
def display():
    print("Hello Students")

@decorator
def show():
    print("Hello Teachers")

display()
show()