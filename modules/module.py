class Module:
    def __init__(self, model, seller, led, parallel_number, series_number, max_current, dimensions, versions):
        self.model = model
        self.seller = seller
        self.led = led
        self.parallel_number = parallel_number
        self.series_number = series_number
        self.max_current = max_current
        self.dimensions = dimensions
        self.versions = versions


class Version:
    def __init__(self, product_code, cct, cri):
        self.product_code = product_code
        self.cct = cct
        self.cri = cri


class Dimensions:
    def __init__(self, length, width):
        self.length = length
        self.width = width
