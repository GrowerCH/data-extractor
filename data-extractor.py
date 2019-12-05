from drivers.driver_extractor import start_driver_extractor
from leds.led_extractor import start_led_extractor
from modules.module_extractor import start_module_extractor

print("start")

currents = [0.35, 0.5, 0.7, 1.05, 1.4, 1.75, 2.1, 2.8, 3.5]

start_led_extractor()
start_driver_extractor()
start_module_extractor(currents)

print("done")
