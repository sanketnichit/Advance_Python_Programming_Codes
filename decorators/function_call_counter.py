def counter(func):
    count = 0

    def wrapper():
        nonlocal count
        count += 1
        print("Function called", count, "time(s)")
        func()

    return wrapper


@counter
def display():
    print("Welcome Students")


display()
display()
display()