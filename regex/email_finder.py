import re

# Regular expression for email
pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+'


# Function to find emails from text
def find_emails(text):
    return re.findall(pattern, text)


# Function to check one email
def check_email(email):
    return re.fullmatch(pattern, email) is not None


# Main program
text = """
Contact details:
Rahul: rahul123@gmail.com
College: student@mitadt.ac.in
Support: help_desk@company.org

Invalid examples:
abc@xyz
hello@
@website.com
"""

print("EMAIL PATTERN FINDER")
print("--------------------")

print("\nGiven Text:")
print(text)

emails = find_emails(text)

print("Emails Found:")
for i, email in enumerate(emails, 1):
    print(i, ".", email)

print("\nTotal Emails Found:", len(emails))


print("\nEmail Validation")
print("----------------")

email = input("Enter an email address: ")

if check_email(email):
    print("Valid Email")
else:
    print("Invalid Email")