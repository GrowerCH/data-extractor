class Module:
    def __init__(self, model, seller, led, parallel_count, series_count, dimensions, versions):
        self.model = model
        self.seller = seller
        self.led = led
        self.parallel_count = parallel_count
        self.series_count = series_count
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
