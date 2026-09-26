logged_in = True

def login_required(func):
    def wrapper():
        if logged_in:
            func()
        else:
            print("Access Denied! Please login first.")
    return wrapper


@login_required
def dashboard():
    print("Welcome to the Dashboard")


dashboard()