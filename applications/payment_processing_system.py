from abc import ABC, abstractmethod
from datetime import datetime
import functools
import uuid


# ----------------------- Decorator -----------------------
def log_transaction(func):
    @functools.wraps(func)
    def wrapper(self, amount):
        print("\n-------------------------------------")
        print(f"Processing payment of ₹{amount}")
        result = func(self, amount)
        print("Transaction Completed")
        print("-------------------------------------")
        return result
    return wrapper


# ----------------------- Receipt -----------------------
class Receipt:
    def __init__(self, amount, method, status):
        self.transaction_id = str(uuid.uuid4())[:8]
        self.amount = amount
        self.method = method
        self.status = status
        self.time = datetime.now()

    def __str__(self):
        return (
            f"\nReceipt"
            f"\nTransaction ID : {self.transaction_id}"
            f"\nMethod         : {self.method}"
            f"\nAmount         : ₹{self.amount}"
            f"\nStatus         : {self.status}"
            f"\nTime           : {self.time.strftime('%d-%m-%Y %H:%M:%S')}"
        )


# ----------------------- Strategy -----------------------
class PaymentStrategy(ABC):

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def pay(self, amount):
        pass


# ----------------------- Credit Card -----------------------
class CreditCard(PaymentStrategy):

    def __init__(self, card, cvv):
        self.card = card
        self.cvv = cvv

    def validate(self):
        return len(self.card) == 16 and self.card.isdigit() and len(self.cvv) == 3

    def pay(self, amount):
        if self.validate():
            print("Credit Card payment successful.")
            return Receipt(amount, "Credit Card", "SUCCESS")
        return Receipt(amount, "Credit Card", "FAILED")


# ----------------------- PayPal -----------------------
class PayPal(PaymentStrategy):

    def __init__(self, email):
        self.email = email

    def validate(self):
        return "@" in self.email

    def pay(self, amount):
        if self.validate():
            print("PayPal payment successful.")
            return Receipt(amount, "PayPal", "SUCCESS")
        return Receipt(amount, "PayPal", "FAILED")


# ----------------------- UPI -----------------------
class UPI(PaymentStrategy):

    def __init__(self, upi):
        self.upi = upi

    def validate(self):
        return "@" in self.upi

    def pay(self, amount):
        if self.validate():
            print("UPI payment successful.")
            return Receipt(amount, "UPI", "SUCCESS")
        return Receipt(amount, "UPI", "FAILED")


# ----------------------- Net Banking -----------------------
class NetBanking(PaymentStrategy):

    def __init__(self, account):
        self.account = account

    def validate(self):
        return self.account.isdigit() and len(self.account) >= 9

    def pay(self, amount):
        if self.validate():
            print("Net Banking payment successful.")
            return Receipt(amount, "Net Banking", "SUCCESS")
        return Receipt(amount, "Net Banking", "FAILED")


# ----------------------- Context -----------------------
class PaymentProcessor:

    methods = {}

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy
        print("Payment method changed.")

    @classmethod
    def register_method(cls, name, strategy):
        cls.methods[name] = strategy

    @classmethod
    def create(cls, name, **kwargs):
        if name not in cls.methods:
            raise ValueError("Payment method not available")
        return cls(cls.methods[name](**kwargs))

    @log_transaction
    def process(self, amount):
        return self.strategy.pay(amount)


# ----------------------- Driver Program -----------------------

PaymentProcessor.register_method("card", CreditCard)
PaymentProcessor.register_method("paypal", PayPal)
PaymentProcessor.register_method("upi", UPI)
PaymentProcessor.register_method("netbanking", NetBanking)

processor = PaymentProcessor.create("upi", upi="sanky@okaxis")
print(processor.process(1200))

processor.set_strategy(CreditCard("1234567812345678", "123"))
print(processor.process(2500))

processor.set_strategy(PayPal("wrongemail"))
print(processor.process(500))

processor.set_strategy(NetBanking("987654321"))
print(processor.process(3000))