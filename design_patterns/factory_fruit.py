class Apple:
    def show(self):
        print("This is Apple")


class Mango:
    def show(self):
        print("This is Mango")


class Orange:
    def show(self):
        print("This is Orange")


class FruitFactory:

    def get_fruit(self, fruit):

        if fruit.lower() == "apple":
            return Apple()

        elif fruit.lower() == "mango":
            return Mango()

        elif fruit.lower() == "orange":
            return Orange()

        else:
            return None


factory = FruitFactory()

fruit = factory.get_fruit("Apple")
fruit.show()

fruit = factory.get_fruit("Mango")
fruit.show()

fruit = factory.get_fruit("Orange")
fruit.show()