import time

def logger(func):
    def wrapper():
        print("Function Name:", func.__name__)
        print("Called At:", time.ctime())
        func()
    return wrapper


@logger
def greet():
    print("Hello Student!")


greet()