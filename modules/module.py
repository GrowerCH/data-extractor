class Module:
    def __init__(self, model, led, parallel_number, series_number, dimensions, versions):
        self.model = model
        self.led = led
        self.parallel_number = parallel_number
        self.series_number = series_number
        self.dimensions = dimensions
        self.versions = versions


class Version:
    def __init__(self, product_code, cct, cri, price, performances):
        self.product_code = product_code
        self.cct = cct
        self.cri = cri
        if price:
            self.price = price
        self.performances = performances


class Performance:
    def __init__(self, current, voltage, flux):
        self.current = current
        self.voltage = voltage
        self.flux = flux


class Dimensions:
    def __init__(self, length, width):
        self.length = length
        self.width = width
