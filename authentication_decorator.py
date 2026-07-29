logged_in = True

def login_required(func):
    def wrapper():
        if logged_in:
            func()
        else:
            print("Please Login First")
    return wrapper


@login_required
def profile():
    print("Welcome to Your Profile")


profile()