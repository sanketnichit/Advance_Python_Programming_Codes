class DisplayDevice:

    def update(self, temperature):
        print("Temperature Updated:", temperature, "°C")


class WeatherStation:

    def __init__(self):
        self.devices = []

    def register(self, device):
        self.devices.append(device)

    def notify(self, temperature):

        for device in self.devices:
            device.update(temperature)


station = WeatherStation()

display1 = DisplayDevice()
display2 = DisplayDevice()

station.register(display1)
station.register(display2)

station.notify(30)
station.notify(35)