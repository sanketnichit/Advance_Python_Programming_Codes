class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True

    def __str__(self):
        status = "Available" if self.available else "Issued"
        return f"{self.title} by {self.author} - {status}"


class Patron:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        self.borrowed_books.remove(book)

    def display_books(self):
        if not self.borrowed_books:
            print("No books borrowed.")
        else:
            print("Borrowed Books:")
            for book in self.borrowed_books:
                print("-", book.title)


class Library:
    def __init__(self):
        self.books = []
        self.patrons = []

    def add_book(self, title, author):
        self.books.append(Book(title, author))
        print("Book added successfully.")

    def register_patron(self, name):
        self.patrons.append(Patron(name))
        print("Patron registered successfully.")

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_patron(self, name):
        for patron in self.patrons:
            if patron.name.lower() == name.lower():
                return patron
        return None

    def issue_book(self, title, patron_name):
        book = self.find_book(title)
        patron = self.find_patron(patron_name)

        if book is None:
            print("Book not found.")
            return

        if patron is None:
            print("Patron not found.")
            return

        if not book.available:
            print("Book is already issued.")
            return

        book.available = False
        patron.borrow_book(book)
        print("Book issued successfully.")

    def return_book(self, title, patron_name):
        book = self.find_book(title)
        patron = self.find_patron(patron_name)

        if book is None or patron is None:
            print("Invalid details.")
            return

        if book in patron.borrowed_books:
            patron.return_book(book)
            book.available = True
            print("Book returned successfully.")
        else:
            print("This patron did not borrow the book.")

    def display_books(self):
        if not self.books:
            print("No books in library.")
        else:
            print("\nLibrary Books:")
            for book in self.books:
                print(book)

    def display_patrons(self):
        if not self.patrons:
            print("No patrons registered.")
        else:
            print("\nPatrons:")
            for patron in self.patrons:
                print("Name:", patron.name)
                patron.display_books()
                print()


library = Library()

while True:
    print("\n===== Library Management System =====")
    print("1. Add Book")
    print("2. Register Patron")
    print("3. Issue Book")
    print("4. Return Book")
    print("5. Display Books")
    print("6. Display Patrons")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter Book Title: ")
        author = input("Enter Author Name: ")
        library.add_book(title, author)

    elif choice == "2":
        name = input("Enter Patron Name: ")
        library.register_patron(name)

    elif choice == "3":
        title = input("Enter Book Title: ")
        name = input("Enter Patron Name: ")
        library.issue_book(title, name)

    elif choice == "4":
        title = input("Enter Book Title: ")
        name = input("Enter Patron Name: ")
        library.return_book(title, name)

    elif choice == "5":
        library.display_books()

    elif choice == "6":
        library.display_patrons()

    elif choice == "7":
        print("Thank you for using Library Management System.")
        break

    else:
        print("Invalid choice. Please try again.")