class Printer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating Printer...")
            cls._instance = super().__new__(cls)
        return cls._instance

    def print_document(self, document):
        print("Printing:", document)


# Multiple users
user1 = Printer()
user2 = Printer()

user1.print_document("Assignment.pdf")
user2.print_document("Project Report.pdf")

# Verify only one object exists
print(user1 is user2)