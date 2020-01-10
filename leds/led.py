class LED:
    def __init__(self, name, max_current, versions):
        self.name = name
        self.max_current = max_current
        self.versions = versions


class Version:
    def __init__(self, cct, cri, voltage, flux, par_conversion, performance):
        self.cct = cct
        self.cri = cri
        self.voltage = voltage
        self.flux = flux
        self.par_conversion = par_conversion
        self.performance = performance
