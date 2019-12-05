class Driver:
    def __init__(self, model, performances):
        self.model = model
        self.performances = performances


class Performance:
    def __init__(self, current, min_voltage, max_voltage):
        self.current = current
        self.min_voltage = min_voltage
        self.max_voltage = max_voltage
