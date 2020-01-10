from drivers.driver_extractor import start_driver_extractor
from leds.led_extractor import start_led_extractor
from modules.module_extractor import start_module_extractor
from prices.price_extractor import start_price_extractor
from utils.extract_utils import save_data_to_file, load_json_from_file

print("start")

selected_leds = ["LM301B", "LM561C"]

module_data = start_module_extractor(selected_leds)
save_data_to_file(module_data, "module_data.json")

module_data = load_json_from_file("module_data.json")  # reload

led_data = start_led_extractor(module_data)
save_data_to_file(led_data, "led_data.json")

module_data = start_price_extractor(module_data)
save_data_to_file(module_data, "module_data.json")

driver_data = start_driver_extractor()
save_data_to_file(driver_data, "driver_data.json")

print("done")
